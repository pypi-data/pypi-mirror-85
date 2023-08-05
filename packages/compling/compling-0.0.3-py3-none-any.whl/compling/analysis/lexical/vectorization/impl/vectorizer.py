from compling.analysis.lexical.vectorization import vectorization
from tqdm import tqdm
import copy
import math
from typing import *
from collections import defaultdict


class Vectorizer(vectorization.Vectorization):
    """
    The process of converting text into vector is called vectorization.
    The set of corpus documents vectorized corpus makes up the Vector Space Model, which can have a sparse or
    dense representation.

    A Vectorizer object allows you to create vectors grouping tokens for arbitrary fields.

    Grouping tokens by:

       * _doc_id_: you 're creating document vectors;
       * _sent_id_: you 're creating sentence vectors;
       * _author_: you're creating author vectors (each token must have an 'author' field);
       ...

    You can group by multiple fields.

    You can also choose the text field the tokens will be grouped by too. (e.g. lemma, text, stem, ...)

    It offers several functions to set the vector components values, such as:

       * **One-hot encoding** (binary values 0/1);
       * **Tf** (Term Frequency);
       * **TfIdf** (Term Frequency Inverse Document Frequency);
       * **MI** (Mutual Information)

    You can specify the vectorization representation format: Term x Document matrix, Postings list.
    """

    def postings2docterm(self, postings: Dict[str, dict]) -> Iterable[dict]:
        """
        Converts a postings list to docterm matrix.

        Args:
            postings (Dict[str, dict]): Postings list.

                    Example:
                    >> print(postings)
                    {
                     "token1":
                           {
                             "doc1": frequency1,
                             ...
                           },
                     ...
                     }

        Returns:
            Iterable[dict]: Docterm matrix.

                    Example:
                    >> print(next(postings2docterm(postings)))
                    {
                     "doc": "doc1",
                     "bow":
                           {
                            token1: frequency1,
                            ...
                            }
                     }
        """

        docterm = defaultdict(dict)
        for token in postings:
            for doc, relevance in postings[token].items():
                docterm[doc].update({token: relevance})

        for doc in docterm:
            yield {self.group_by_field_key: doc, 'bow': docterm[doc]}

    def docterm2postings(self, docterm: Iterable[dict]) -> Dict[str, dict]:
        """
        Converts a docterm matrix to a postings list.

        Args:
            docterm (Iterator[dict]): Docterm matrix.

                    Example:
                    >> print(next(docterm))
                    {
                     "doc": "doc1",
                     "bow":
                           {
                            token1: frequency1,
                            ...
                            }
                     }
                     # bow: Bag of Words
        Returns:
            Dict[str, dict]: Postings list.

                    Example:
                    >> print(docterm2postings(docterm))
                    {
                     "token1":
                           {
                             "doc1": frequency1,
                             ...
                           },
                     ...
                     }
        """

        postings = defaultdict(dict)
        for record in docterm:
            for token, relevance in record['bow'].items():
                postings[token].update({record[self.group_by_field_key]: relevance})

        return postings

    def tf(self, tokens: Iterable[dict], pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
           dep: Tuple[str, ...] = None, lang: str = None, min_len: int = 0,
           min_count: int = 0, format_: str = "docterm-matrix", boolean=False) -> Union[Dict[str, dict], Iterable[dict]]:
        """
        Calculates Term Frequency.

        Args:
            tokens (Iterable[dict]): Stream of token records produced during the Tokenization stage.

                    Example:
                    >>> token = next(tokens)
                    >>> print(token)
                    {
                    "token_id_": 0,
                    "sent_id_": 0,
                    "para_id_": 0,
                    "doc_id_": 0,
                    "text_": "When",
                    "sent_pos_": 0,
                    "para_pos_": 0,
                    "doc_pos_": 0,
                    "lower_": "when",
                    ...
                    }

            pos (Tuple[str, ...], optional, default=NOUN,VERB,PROPN,ADJ): Part of speech of the tokens. <br/> Filters the most informative tokens: tokens whose PoS tag is in the 'pos' list. <br/> If None, the filter will be ignored.
            dep (Tuple[str, ...], optional, default=None): Dependencies of the tokens. <br/> Filters the most informative tokens: tokens whose dep tag is in the 'dep' list. <br/> If None, the filter will be ignored.
            lang (str, optional, default=None): Filters the tokens of the language (iso639). <br/> If None, the filter will be ignored.
            min_len (int, optional, default=0): The minimum length a token must have to be considered.
            min_count (int, optional, default=0): The minimum frequency a token must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                Valid input values:
                ["postings-list", "docterm-matrix"]

            boolean (bool, optional, default=False): If True return Boolean Vectors else Term Frequency. <br/> If True, the result is the same as onehot method.

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.

                    Example:
                    [format_ == "postings-list"]

                    {
                        "token1":
                              {
                                "doc1": tf1,
                                ...
                              },
                        ...
                    }

                     Example:
                    [format_ == "docterm-matrix"]

                    [{
                        "doc": "doc1",
                        "bow":
                              {
                               token1: tf1,
                               ...
                               }
                    },
                    ...
                    ]
        """

        filters = dict()
        for k, v in self.nlp.config.config['Vector_filter'].items():
            if v != 'None':
                filters[k] = bool(int(v))

        def __filter__(__token__):
            for key, value in {'dep_': dep, 'pos_': pos}.items():
                if value is not None and len(value) != 0 and __token__[key] not in value:
                    return False

            if len(__token__[self.token_field]) < min_len:
                return False

            for key, value in filters.items():
                if not __token__[key + '_'] == value:
                    return False

            if lang is not None and lang != __token__['lang_']:
                return False

            return True

        postings = defaultdict(lambda: defaultdict(int))
        for token in tokens:
            if not __filter__(token):
                continue

            key = " + ".join([token[g] for g in self.group_by_field])
            if boolean:
                postings[token[self.token_field]][key] = 1
            else:
                postings[token[self.token_field]][key] += 1

        for token in copy.deepcopy(postings):
            if sum(postings[token].values()) < min_count:
                del postings[token]

        if format_ == 'postings-list':
            return postings
        else:
            return self.postings2docterm(postings)

    def tfidf(self, tokens: Iterable[dict], normalize=True,
              pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
              dep: Tuple[str, ...] = None, lang: str = None, min_len: int = 0,
              min_count: int = 0, format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterable[dict]]:
        """
        Calculates Term Frequency Inverse Document Frequency.


        Args:
            tokens (Iterable[dict]): Stream of token records produced during the Tokenization stage.

                    Example:
                    >>> token = next(tokens)
                    >>> print(token)
                    {
                    "token_id_": 0,
                    "sent_id_": 0,
                    "para_id_": 0,
                    "doc_id_": 0,
                    "text_": "When",
                    "sent_pos_": 0,
                    "para_pos_": 0,
                    "doc_pos_": 0,
                    "lower_": "when",
                    ...
                    }

            normalize (bool, optional, default=True): If True, normalizes TF for max(TF).
            pos (Tuple[str, ...], optional, default=NOUN,VERB,PROPN,ADJ): Part of speech of the tokens. <br/> Filters the most informative tokens: tokens whose PoS tag is in the 'pos' list. <br/> If None, the filter will be ignored.
            dep (Tuple[str, ...], optional, default=None): Dependencies of the tokens. <br/> Filters the most informative tokens: tokens whose dep tag is in the 'dep' list. <br/> If None, the filter will be ignored.
            lang (str, optional, default=None): Filters the tokens of the language (iso639). <br/> If None, the filter will be ignored.
            min_len (int, optional, default=0): The minimum length a token must have to be considered.
            min_count (int, optional, default=0): The minimum frequency a token must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.

                    Example:
                    [format_ == "postings-list"]

                    {
                        "token1":
                              {
                                "group_by_field1": tfid1,
                                ...
                              },
                        ...
                    }

                     Example:
                    [format_ == "docterm-matrix"]

                    [{
                        group_by_field: "group_by_field1",
                        "bow":
                              {
                               token1: tfid1,
                               ...
                               }
                    },
                    ...
                    ]
        """


        postings = self.tf(tokens, pos, dep, lang, min_len, min_count, format_='postings-list')

        docterm = self.postings2docterm(postings)
        max_tf = {}
        n = 0
        for doc in docterm:
            n += 1
            max_tf[doc[self.group_by_field_key]] = max(doc['bow'].values())

        # Corpus size: the number of documents in the corpus
        N = n

        # The tf_dict will be update to tfidf_dict
        tfidf_postings = copy.deepcopy(postings)

        bar = tqdm(total=len(tfidf_postings), desc="TFIDF calculation in progress... ", position=0, leave=True)

        # For each token in the postings list
        for token in tfidf_postings.keys():

            docs = tfidf_postings[token]

            # For each doc which the token occurs in
            for doc, tf in docs.items():
                if normalize:
                    tf = tf / max_tf[doc]

                # Document Frequency
                df = len(postings[token])

                # Inverse Document Frequency
                idf = math.log(N / df)

                # Term Frequency Inverse Document Frequency
                tfidf_postings[token].update({doc: tf * idf})
            bar.update(1)
        bar.close()

        if format_ == 'postings-list':
            return tfidf_postings
        else:
            return self.postings2docterm(tfidf_postings)

    def mi(self, tokens: Iterable[dict], pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
           dep: Tuple[str, ...] = None, lang: str = None, min_len: int = 0,
           min_count: int = 0, format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterator[dict]]:
        """
        Calculates Mutual Information.

        Args:
            tokens (Iterable[dict]): Stream of token records produced during the Tokenization stage.

                    Example:
                    >>> token = next(tokens)
                    >>> print(token)
                    {
                    "token_id_": 0,
                    "sent_id_": 0,
                    "para_id_": 0,
                    "doc_id_": 0,
                    "text_": "When",
                    "sent_pos_": 0,
                    "para_pos_": 0,
                    "doc_pos_": 0,
                    "lower_": "when",
                    ...
                    }

            pos (Tuple[str, ...], optional, default=NOUN,VERB,PROPN,ADJ): Part of speech of the tokens. <br/> Filters the most informative tokens: tokens whose PoS tag is in the 'pos' list. <br/> If None, the filter will be ignored.
            dep (Tuple[str, ...], optional, default=None): Dependencies of the tokens. <br/> Filters the most informative tokens: tokens whose dep tag is in the 'dep' list. <br/> If None, the filter will be ignored.
            lang (str, optional, default=None): Filters the tokens of the language (iso639). <br/> If None, the filter will be ignored.
            min_len (int, optional, default=0): The minimum length a token must have to be considered.
            min_count (int, optional, default=0): The minimum frequency a token must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.

                    Example:
                    [format_ == "postings-list"]

                    {
                        "token1":
                              {
                                "doc1": mi1,
                                ...
                              },
                        ...
                    }

                    Example:
                    [format_ == "docterm-matrix"]

                    [{
                        "doc": "doc1",
                        "bow":
                              {
                               token1: mi1,
                               ...
                               }
                    },
                    ...
                    ]
        """

        postings = self.tf(tokens, pos, dep, lang, min_len, min_count, format_='postings-list')
        docterm = {record[self.group_by_field_key]: record for record in self.postings2docterm(postings)}

        # x: group_by_field label
        # y: token
        n_tokens = sum([sum(postings[token].values()) for token in postings])

        mi_postings = defaultdict(lambda :defaultdict(int))
        for token in postings:
            posting = defaultdict(int, postings[token])
            for label in posting:
                row = docterm[label]['bow']
                len_x = sum(posting.values())
                len_y = sum(row.values())

                p_x = len_x/n_tokens
                p_y = len_y/n_tokens
                p_x_y = posting[label]/n_tokens

                mi_postings[token][label] = p_x_y * math.log(p_x_y/(p_x*p_y))

        if format_ == 'postings-list':
            return mi_postings
        else:
            return self.postings2docterm(mi_postings)

    def onehot(self, tokens: Iterable[dict], pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
               dep: Tuple[str, ...] = None, lang: str = None, min_len: int = 0,
               min_count: int = 0, format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterable[dict]]:
        """
        Calculates One-hot encoding.

        Args:
            tokens (Iterable[dict]): Stream of token records produced during the Tokenization stage.

                    Example:
                    >>> token = next(tokens)
                    >>> print(token)
                    {
                    "token_id_": 0,
                    "sent_id_": 0,
                    "para_id_": 0,
                    "doc_id_": 0,
                    "text_": "When",
                    "sent_pos_": 0,
                    "para_pos_": 0,
                    "doc_pos_": 0,
                    "lower_": "when",
                    ...
                    }

            pos (Tuple[str, ...], optional, default=NOUN,VERB,PROPN,ADJ): Part of speech of the tokens. <br/> Filters the most informative tokens: tokens whose PoS tag is in the 'pos' list. <br/> If None, the filter will be ignored.
            dep (Tuple[str, ...], optional, default=None): Dependencies of the tokens. <br/> Filters the most informative tokens: tokens whose dep tag is in the 'dep' list. <br/> If None, the filter will be ignored.
            lang (str, optional, default=None): Filters the tokens of the language (iso639). <br/> If None, the filter will be ignored.
            min_len (int, optional, default=0): The minimum length a token must have to be considered.
            min_count (int, optional, default=0): The minimum frequency a token must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.

                    Example:
                    [format_ == "postings-list"]

                    {
                        "token1":
                              {
                                "doc1": 1,
                                "doc2": 0,
                                ...
                              },
                        ...
                    }

                    Example:
                    [format_ == "docterm-matrix"]

                    [{
                        "doc": "doc1",
                        "bow":
                              {
                               token1: 1,
                               ...
                               }
                    },
                    ...
                    ]
        """
        return self.tf(tokens, pos, dep, lang, min_len, min_count, boolean=True, format_=format_)

    def run(self, mode: str, tokens: Iterable[dict], normalize=True,
            pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
            dep: Tuple[str, ...] = None,
            lang: str = None, min_len=0, min_count=0,
            metadata: Dict[str, dict] = None) -> Iterable[dict]:
        """
        Runs the vectorization grouping token by self.token_field and self.group_by_field.

        Args:
            mode (str): Vectorization mode. <br/>

                    Valid input values:
                    ["tf", "tfidf", "mi", "onehot"]

            tokens (Iterable[dict]): Stream of token records produced during the Tokenization stage.

                    Example:
                    >>> token = next(tokens)
                    >>> print(token)
                    {
                    "token_id_": 0,
                    "sent_id_": 0,
                    "para_id_": 0,
                    "doc_id_": 0,
                    "text_": "When",
                    "sent_pos_": 0,
                    "para_pos_": 0,
                    "doc_pos_": 0,
                    "lower_": "when",
                    ...
                    }

            normalize (bool, optional, default=True): If True, normalizes TF for max(TF). <br/> This parameter is ignored if mode in ['tf', 'onehot', 'mi'].
            pos (Tuple[str, ...], optional, default=NOUN,VERB,PROPN,ADJ): Part of speech of the tokens. <br/> Filters the most informative tokens: tokens whose PoS tag is in the 'pos' list. <br/> If None, the filter will be ignored.
            dep (Tuple[str, ...], optional, default=None): Dependencies of the tokens. <br/> Filters the most informative tokens: tokens whose dep tag is in the 'dep' list. <br/> If None, the filter will be ignored.
            lang (str, optional, default=None): Filters the tokens of the language (iso639). <br/> If None, the filter will be ignored.
            min_len (int, optional, default=0): The minimum length a token must have to be considered.
            min_count (int, optional, default=0): The minimum frequency a token must have in the corpus to be considered.
            metadata (Dict[str, dict], optional, default=None): A dict containing metadata for each different group_by_field value.  <br/> Each vector will be associated with its own metadata.

                    Example:

                    {
                     "group_by_field1": {
                                         metadata1: 'metadata1',
                                         metadata2: 'metadata2',
                                         ...
                                        },
                     "group_by_field2": {
                                          metadata1: 'metadata11',
                                          metadata2: 'metadata22',
                                         ...
                                        },
                    ...
                    }


        Returns:
            Iterable[dict]: Returns a docterm matrix.

                    Example:
                    >> v = Vectorizer('doc_id', 'text')
                    >> record = v.run('tfidf', tokens)
                    >> print(next(record))
                    {
                        "doc": "doc1",
                        "bow":
                              {
                               token1: frequency1,
                               ...
                               }
                        metadata1: "metadata1",
                        metadata2: "metadata2",
                        ...
                    }
        """

        # in order to load the vectorization in a mongodb database
        if mode in ['tf', 'onehot']:
            docterm = getattr(self, mode)(tokens=tokens, pos=pos, dep=dep, lang=lang, min_len=min_len,
                                          min_count=min_count, format_='docterm-matrix')

        elif mode == 'tfidf':
            docterm = getattr(self, mode)(tokens=tokens, normalize=normalize, pos=pos, dep=dep, lang=lang,
                                          min_len=min_len, min_count=min_count,
                                          format_='docterm-matrix')

        # elif mode == 'mi':
        else:
            docterm = getattr(self, mode)(tokens=tokens, pos=pos, dep=dep, lang=lang, min_len=min_len,
                                          min_count=min_count,
                                          format_='docterm-matrix')

        # keep the information
        if metadata is not None and len(metadata) > 0:
            for row in docterm:
                record = dict(row)
                record.update(metadata[row[self.group_by_field_key]])
                yield record
        else:
            for row in docterm:
                yield row
