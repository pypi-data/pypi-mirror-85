import abc
from typing import Tuple, Iterable
from compling.analysis.sentiment.lexicon.lexicon import Lexicon


class SentimentLexiconBased(metaclass=abc.ABCMeta):
    """
    The most popular unsupervised strategies used in _sentiment analysis_ are _lexical-based_ methods. <br/>
    They make use of a predefined list of words, where each word is associated with a specific _sentiment_. <br/>
    Lexicon-based strategies are very efficient and simple methods. They make use of a sentiment _lexicon_
     to assign a polarity value to each text document by following a basic algrithm. A sentiment lexicon is a
     list of lexical features (e.g., words, phrase, etc.) which are labeled according to their semantic
     orientation (i.e. polarity) as either _positive_ or _negative_.
    """

    def filter(self, index: Iterable[dict], regex_pattern: str) -> None:
        """
        Filters the sentences/paragraphs/documents to be considered to calculate a polarity value.

        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).
            regex_pattern (str): The filter uses this regex.
        """

    def run(self, lexicon: Lexicon, tf_: bool = True) -> Tuple[dict, dict]:
        """
        Performs sentiment analysis of the texts in the index calculating the polarity level for each different
        group_by_field value.

        Args:
            lexicon (Lexicon): A Lexicon object.
            tf_ (bool, optional, default=True): If True, considers the frequency of the words: the token polarity will be summed n times, where n is the token frequency in the text. <br/> If false, the polarity of a token in the text will be summed exactly once. <br/>

        Returns:
            Tuple[dict, dict]: Two dict are returned:

                * the first contains the polarity value for each different grouped_by_field value.

                         Example:
                         {
                          "grouped_by_field1": {
                                                "pos": 0,
                                                "neg":1,
                                                "obj":3},
                           ...,
                         }

                * the second contains the words classified as positive/negative with their polarity value for each different grouped_by_field value.

                         Example:
                         {
                          "grouped_by_field1": {
                                                "neg": {
                                                        "fuck": 12.0,
                                                        "bad": 7.0,
                                                        ...
                                                        },
                                                "pos": {
                                                        "good": 11.0,
                                                        "love": 2.0,
                                                        ...
                                                        }
                                                },
                          ...
                        }
        """
