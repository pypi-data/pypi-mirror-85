from typing import *
from tqdm import tqdm
from datetime import datetime
from collections import defaultdict
from nltk.tokenize import sent_tokenize
from compling.analysis.lexical.tokenization import tokenization_abc
from collections.abc import Iterable as abciterable
from compling.analysis.lexical.tokenization.impl.sentence import Sentence
from compling.analysis.lexical.tokenization.impl.paragraph import Paragraph
from compling.analysis.lexical.tokenization.impl.document import Document


class Tokenizer(tokenization_abc.Tokenization):
    """
    Tokenization converts input text to streams of tokens, where each token is a separate word, punctuation sign,
    number/amount, date, etc.

    A Tokenizer object converts the corpus documents into a stream of:

       * _tokens_: tokens occurring in those documents. Each token is characterized by:
          * _token_id_: unique token identifier;
          * _sent_id_: unique sentence identifier. The id of the sentence the token occurs in;
          * _para_id_: unique paragraph identifier. The id of the paragraph the token occurs in;
          * _doc_id_: unique document identifier. The id of the document the token occurs in;
          * _text_: the text of the token;
          * a large variety of _optional meta-information_ (e.g. PoS tag, dep tag, lemma, stem, ...);
       * _sentences_ : sentences occurring in those documents. Each sentence is characterized by:
          * _sent_id_: unique sentence identifier;
          * _para_id_: unique paragraph identifier. The id of the paragraph the sentence occurs in;
          * _doc_id_: unique document identifier. The id of the document the sentence occurs in;
          * _text_: the text of the sentence;
          * a large variety of _optional meta-information_ (e.g.lemma, stem, ...);
       * _paragraphs_: sentences occurring in those documents. Each paragraph is characterized by:
          * _para_id_: unique paragraph identifier;
          * _doc_id_: unique document identifier. The id of the document the paragraph occurs in;
          * _text_: the text of the paragraph;
          * a large variety of _optional meta-information_ (e.g.lemma, stem, ...);
       * _documents_: Each document is characterized by:
          * _doc_id_: unique document identifier;
          * _text_: the text of the document;
          * a large variety of _optional meta-information_ (e.g.lemma, stem, ...);

    A Tokenizer object is also able to retrieve frequent n-grams to be considered as unique tokens.

    For each record (token, sentence, paragraph, document) are stored some metadata.
    You can edit the config.ini file to change those stored by default.

    In order to run tokenization you need to provide a Iterable[dict], where each document is a dict
    and has a key where it stores the text of the document. By default the text key is 'text', you can change it
    editing the config.ini file.

    For each document in your corpus, all key/value data (except for text key) are added as metadata to
    that document records. (e.g. title, author, ...).
    """

    def __init__(self, docs: Iterable[dict], domain_stopwords: List[str] = None) -> None:
        """
        Creates a new Tokenizer object.

        Args:
            docs (Iterable[dict]): Stream of json documents as dicts. <br/> Each document must have a key where the text of the document is stored.
            domain_stopwords (List[str], optional, default=None): You can provide a list of arbitrary stopwords specific to your corpus domain.
        """

        # super __init__
        super(Tokenizer, self).__init__(docs)

        # add some stopwords to nlp list.
        self.nlp.stopwords_list(include=domain_stopwords)

    def ngrams2tokens(self, n: Union[int, Iterable[int]], pos: Tuple[str, ...] = ("PROPN", "VERB", "NOUN", "ADJ"),
                      corpus_threshold: int = 50,
                      doc_threshold: int = 0,
                      len_gram: int = 3, include: Tuple[str, ...] = None, replace: bool = True) -> Dict[int, str]:
        """
        Returns frequent n-grams in the corpus. They will be considered as tokens during the Tokenization task.

        Args:
           n (Union[int, Iterable[int]]): If int, the size of n-grams. (e.g. n=2, bigrams) <br/> If Iterable[int], the sizes of n-grams. (e.g. n=[2,3,5], bigrams, trigrams, fivegrams)
           pos (Tuple[str, ...], optional): default ('PROPN', 'VERB', 'NOUN', 'ADJ'). <br/> Part of speech of the first and the last token that make up n-grams. <br/> Filters the most informative n-grams. <br/> If None, the filter will be ignored.

                   Example:
                   pos = ("PROPN", "VERB", "NOUN", "ADJ")

                   These n-grams are IGNORED:
                   - "of a": of [ADP], a [DET]
                   - "at home":  at [ADP], home [NOUN]
                   - "as much then": as [ADP], as [ADP]
                   - "a computer scientist": a [DET], scientist [NOUN]
                   - "of natural phenomena": of [ADP], phenomena [NOUN]
                   - ...

                   These n-grams are CONSIDERED:
                   * "mother Earth": mother [NOUN], Earth [PROPN]
                   * "John likes": John [PROPN], likes [VERB]
                   * "computer scientist": computer [NOUN], scientist [NOUN]
                   * "Galilean scientific method": Galilean [ADJ], method [NOUN]
                   * "understanding of natural phenomena": understanding [NOUN], phenomena [NOUN]
                   ...

           corpus_threshold (int, optional, default=50): Filters n-grams that have a corpus frequency greater than corpus_threshold.
           doc_threshold (int, optional, default=0): Filters n-grams that have in frequency greater than doc_threshold. <br/> The frequency of an n-gram in the corpus is the sum of the frequency of that n-gram in documents where the ngram occurs at least doc_thresold times.
           len_gram (int, optional, default=3): The size of the first and the last token that make up n-grams must be at least 'len_gram'.

                   Example:
                   len_gram = 5

                   These n-grams are IGNORED:
                   - "John likes": John [4], likes [5]
                   - "New York":  New [3], York [3]
                   - ...

                   These n-grams are CONSIDERED:
                   * "mother Earth": mother [6], Earth [5]
                   * "computer scientist": computer [8], scientist [9]
                   ...

           include (Tuple[str, ...], optional, default=None): Include a list of arbitrary n-grams.
           replace (bool, optional, default=True): If True, replaces a n-gram with its tokens separated by '_'. <br/> Else, concatenates a new token, made merging the n-gram tokens with '_', to the n-gram.

                   Example:

                    - replace = True:
                      "New York is the most populous city in the United States."
                       ->
                      "New_York is the most populous city in the United_States."

                    - replace = False:
                      "New York is the most populous city in the United States."
                       ->
                      "New York New_York is the most populous city in the United States United_States."

        Returns:
            Dict[str, int]: N-grams as keys, frequencies as values. <br/> The frequencies of the n-grams included arbitrarily are set to 0.


                    Example:
                    include = ("Giorgio Napolitano")

                     {
                        "New York": 51,
                        "Giorgio Napolitano": 0,
                        ...
                        "Donald Trump": 402
                     }
        """

        # list of sizes of n-grams
        if isinstance(n, abciterable):
            sizes = n
        else:
            sizes = [n]

        ngram_frequencies = defaultdict(int)
        bar = tqdm(total=len(self.docs), desc='N-grams Retrieval in progress...', position=0, leave=True)
        # for each corpus doc
        for doc in self.docs:
            text = doc[self.text_key]
            for n in sizes:
                for ngram, frequency in self.nlp.ngrams(text, n, pos=tuple(), threshold=doc_threshold).items():
                    ngram_frequencies[ngram] += frequency
            bar.update(1)
        bar.close()

        # Select the n grams you're interested in
        ngram_frequencies = {ngram: frequency for ngram, frequency in ngram_frequencies.items() if
                             frequency >= corpus_threshold}

        # Ngram final list
        result = defaultdict(int)

        # First and last word must be in pos and at least len_gram sized
        for ngram in ngram_frequencies:
            ngram_ = self.nlp.nlp_spacy(" ".join(ngram))
            if ngram_[0].pos_ in pos and ngram_[-1].pos_ in pos and \
                    len(ngram_[0].text) >= len_gram and len(ngram_[-1].text) >= len_gram:
                ngram_ = " ".join([token.text for token in ngram_])
                result[ngram_] = ngram_frequencies[ngram]

        # add arbitrary n-grams
        if include is not None:
            for ngram in include:
                if ngram not in result:
                    result[ngram] = 0

        # sorted by len: first we replace the longer n-grams, then shorter ones.
        result = sorted(result.items(), key=lambda x: len(x[0]), reverse=True)

        # updates doc: replaces n-grams with tokens
        for doc in self.docs:
            for ngram in result:
                if replace:
                    doc[self.text_key] = doc[self.text_key].replace(ngram, ngram.replace(' ', '_'))
                else:
                    doc[self.text_key] = doc[self.text_key].replace(ngram, ngram + ' ' + ngram.replace(' ', '_'))
        return result

    def run(self, doc_id: int = 0, token_id: int = 0, sent_id: int = 0, para_id: int = 0,
            para_size: int = 3, index_doc: bool = True, index_sent: bool = True,
            index_para: bool = True) -> Iterable[Dict[str, dict]]:
        """
        Runs the tokenization for each document of the corpus.

        Args:
            doc_id (int, optional, default=0): Unique document identifier. <br/> Numeric id of documents. <br/> A progressive id will be assigned to the documents starting from this number.
            token_id (int, optional, default=0): Unique token identifier. <br/> Numeric id of tokens. <br/> A progressive id will be assigned to the tokens starting from this number.
            sent_id (int, optional, default=0): Unique sentence identifier. <br/> Numeric id of sentences. <br/> A progressive id will be assigned to the sentences starting from this number.
            para_id (int, optional, default=0): Unique paragraph identifier. <br/> Numeric id of paragraphs. <br/> A progressive id will be assigned to the paragraphs starting from this number.
            para_size (int, optional, default=3): The paragraph size: the number of sentences that makes up a paragraph.
            index_doc (bool, optional, default=True): If True, returns the records of the documents index as values of the key 'documents'.
            index_sent (bool, optional, default=True): If True, returns the records of the sentences index as values of the key 'sentences'.
            index_para (bool, optional, default=True): If True, returns the records of the paragraphs index as values of the key 'paragraphs'.

        Returns:
            Iterable[Dict[str, dict]]: Stream of tokens, sentences, paragraphs, documents records.

                Example:
                [index_sent == True, index_para == False, index_doc == True]

                >>> t = Tokenizer(docs=my_docs, domain_stopwords=my_domain_stopwords)
                >>> records = t.run():
                >>> next(records).keys()
                dict_keys(["tokens", "sentences", "documents"])


                Example:
                >>> record = next(records)
                >>> tokens = record["tokens"]
                >>> sentences = record["sentences"]
                >>> print(tokens)
                [
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
                    },
                    ...
                ]
                >>> print(sentences)
                [
                    {
                     "sent_id_": 0,
                     "text_": "When We , though all unworthy , were called to succeed on the Apostolic Throne the meek Pius X , whose life of holiness and well doing was cut short by grief -atti_degli_apostoli- the fratricidal struggle that had just burst forth in Europe , We , too , on turning a fearful glance on the blood stained battlefields , felt the anguish of a father , who sees his homestead devastated and in ruins before the fury of the hurricane .",
                     "named_entities_": ["Apostolic Throne", "Pius X", "Europe"],
                    ...
                    }
                ]


            Check the config.ini file for records information.
        """

        # list of sentences making up a paragraph
        # list of paragraphs making up a document
        sent_list, para_list = list(), list()

        # tokenization of each doc
        bar = tqdm(total=len(list(self.docs)), desc='Tokenization in progress...', position=0, leave=True)
        for doc in self.docs:

            text = doc[self.text_key]

            metadata = dict()
            for k, v in doc.items():
                if k == self.text_key:
                    continue
                try:
                    # if it's a date
                    v = datetime.strptime(v, self.date_format)
                except:
                    pass
                metadata[k] = v

            # token position inside the paragraphs/documents: -1, Sentence will increment it, so that it can start from 0.
            para_pos, doc_pos = -1, -1

            # tokenization of each sentence
            for sent in sent_tokenize(text, language=self.nlp.language):
                # Sentence will increment token_id, so that it can start from 0.
                sent = Sentence(sent_id, token_id - 1, sent, self.nlp, self.nlp.config, para_id,
                                doc_id, para_pos, doc_pos, metadata)
                para_pos, doc_pos = sent.para_pos, sent.doc_pos
                sent_list.append(sent)

                # new paragraph
                if len(sent_list) == para_size:
                    para_list.append(Paragraph(para_id, sent_list, self.nlp.config, metadata))
                    sent_list = list()
                    # next paragraph
                    para_id += 1

                # next token
                token_id = sent.token_id
                # next sentence
                sent_id += 1

            # Reset sentence list. Remove item from the previous source.
            # The last paragraph can be shorter than the others.
            # new paragraph
            if len(sent_list) > 0:
                para_list.append(Paragraph(para_id, sent_list, self.nlp.config, metadata))
                para_id += 1
                sent_list = list()

            # new document
            doc = Document(doc_id, para_list, self.nlp.config, metadata)
            para_list = list()

            # next document
            doc_id += 1

            # build records
            doc_records, para_records, sent_records, token_records = list(), list(), list(), list()
            if index_doc:
                doc_records.append(doc.to_dict())
            if index_para:
                para_records.extend([para.to_dict() for para in doc.para_list])
            for para in doc.para_list:
                if index_sent:
                    sent_records.extend([sent.to_dict() for sent in para.sent_list])
                for sent in para.sent_list:
                    token_records.extend([token.to_dict() for token in sent.token_list])

            # store data in database
            tokenization_ = dict()
            tokenization_['tokens'] = token_records
            if index_sent:
                tokenization_['sentences'] = sent_records
            if index_para:
                tokenization_['paragraphs'] = para_records
            if index_doc:
                tokenization_['documents'] = doc_records

            bar.update(1)
            yield tokenization_
        bar.close()
