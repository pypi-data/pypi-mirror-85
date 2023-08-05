import abc
from typing import *
from compling.nlptoolkit.nlp import NLP


class Vectorization(metaclass=abc.ABCMeta):
    """
    The process of converting text into vector is called vectorization.
    The set of corpus documents vectorized corpus makes up the Vector Space Model, which can have a sparse or
    dense representation.
    """

    def __init__(self, group_by_field: Union[str, List[str]], token_field: str = 'text') -> None:
        """
        **\_\_init\_\_**: Creates a new Vectorization object.

        Args:
            token_field (str, optional, default=text): A field containing the text of tokens (e.g. text, lemma, ...). <br/> The tokens will be grouped by this field.
            group_by_field (Union[str, List[str]]): Fields linked to tokens in the corpus (e.g. doc_id, sent_id, metadata1, ...).  <br/> The tokens will be grouped by these field.
        """
        self.token_field = token_field + '_'

        if isinstance(group_by_field, str):
            self.group_by_field = [group_by_field + '_']
        else:
            self.group_by_field = [g + '_' for g in group_by_field]

        self.group_by_field_key = " + ".join(self.group_by_field)

        self.nlp = NLP()

    @abc.abstractmethod
    def tf(self, tokens: Iterable[dict], pos: Tuple[str, ...] = ("NOUN", "VERB", "PROPN", "NGRAM"),
           dep: Tuple[str, ...] = None, lang: str = None, min_len: int = 0,
           min_count: int = 0, format_: str = "docterm-matrix", boolean=False) -> Union[
        Dict[str, dict], Iterable[dict]]:
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

    @abc.abstractmethod
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

    @abc.abstractmethod
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

    @abc.abstractmethod
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

    @abc.abstractmethod
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
