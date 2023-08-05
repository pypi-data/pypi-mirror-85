import re
import spacy
import string
import unicodedata
from spacy.tokens.doc import Doc
from nltk.corpus import stopwords
from collections import defaultdict
from typing import *
from nltk.stem.snowball import SnowballStemmer
from compling.config import ConfigManager

negations = {'en': ["not", "n't", "no", "none", "neither", "nor", "never", "hardly", "scarcely",
                    "barely", "rarely", "seldom", "doesn’t", "isn’t", "don't", "shouldn’t", "couldn’t",
                    "won't", "can't", 'nobody', 'naught', 'nil', 'nix', 'nonentity', 'nullity', 'nothingness',
                    'zilch'],
             'it': ["nemmeno", "neppure", "neanche", "nessuno", "alcuno", "veruno", "niuno", "niente", "nulla",
                    "affatto", "mica", "meno",
                    "mai più", "figurati", "figurarsi", "mai", "no", "né"],
             'es': ['nadie', 'nada', 'ni', 'jamás', 'jamas', 'nunca', 'tampoco', 'todavía no', 'todavia no',
                    'ya no', 'no', 'ninguno', 'ningún', 'ningun', 'ni siquiera', 'más'],
             'pt': ['nada', 'ninguém', 'ninguem', 'nenhum', 'tampouco', 'nem', 'nunca', 'jamais', 'não', 'nao',
                    'nenhum', 'nenhuma', "nem mesmo"],
             'zh': ['bù', '不', 'méi', '没', 'méiyǒu', '没有', "甚至", "完全不", "少", "決不", "不再"],
             'da': ["ikke engang", "ikke en gang", "ingen", "nogen", "ingen", "intet", "slet ikke", "ikke", "mindre",
                    "aldrig igen", "aldrig", "nej"],
             'nl': ["zelfs niet", "zelfs niet", "zelfs niet", "niemand", "niemand", "niets", "niets", "helemaal niet",
                    "niet", "minder", "nooit meer", "nooit", "nee"],
             'de': ["nicht", "nein", "es ist nicht", "weder", "noch", "noch nie", "kaum", "selten", "ist nicht",
                    "sollte nicht", "konnte nicht", "wird nicht", "kann nicht ", 'niemand', 'nichts', 'nichtigkeit'],
             'el': ["όχι", "κανένας", "ούτε", "ποτέ", "δεν", "κανένας", "νιξ", "μη ουσία", "ακυρότητα", "τίποτα"],
             'ja': ["ない", "ない", "いいえ", "なし", "どちらでもない", "どちらでもない", "まったくない", "しない", "ない", "しない",
                    "すべきではない", "できなかった", "しない", "できない", "誰もいない", "ない", "ジルチ」"],
             'lt': ["ne", "ne", "nėra", "nei", "nei", "niekada", "niekas", "nieko", "nulis", "nebuvimas", "niekingumas",
                    "niekis"],
             'nb': ["ikke", "ikke", "nei", "ingen", "verken", "eller", "aldri", "ingen", "intet", "null", 'nullitet',
                    'ingenting', ''],
             'pl': ["nie", "brak", "ani", "nigdy", "nic", 'nieważność', 'nicość'],
             'ro': ["nu", "nici unul", "nici", "niciodată", "nimeni", "nimic", "nonentitate", "nulitate", "neant"]}


class NLP:
    """
    **Natural Language Processing** (_NLP_) is a field of _Artificial Intelligence_ that gives the machines the ability to read, understand and derive meaning from _human languages_. It is a discipline that focuses on the interaction between data science and human language.
    """

    def __init__(self, spacy_model: str = None, language: str = None, iso639: str = None) -> None:
        """
        **\_\_init\_\_**: Creates a new _NLP_ object.

        Args:
            spacy_model (str, optional, default=None): Spacy model used in text processing.

                    Valid input values:
                    ["it_core_news_sm", "en_core_web_sm", "es_core_news_sm", "pt_core_news_sm",
                    "zh_core_web_sm", "da_core_news_sm", "nl_core_news_sm", "de_core_news_sm",
                    "el_core_news_sm", "ja_core_news_sm", "lt_core_news_sm", "nb_core_news_sm",
                    "pl_core_news_sm", "ro_core_news_sm", "fr_core_news_sm"]

                    Example:
                    You have to install the spacy model you want to use:
                    $ python -m spacy download en_core_web_sm

            language (str, optional, default=None): Language of the text to be processed.

                     Valid input values:
                     ["arabic", "danish", "dutch", "english", "finnish", "french", "german", "hungarian",
                     "italian", "norwegian", "portuguese", "romanian", "russian", "spanish", "swedish"]

            iso639 (str, optional, default=None): Standard _iso-639_ of the language.

                     Valid input values:
                     ["ar", "da", "nl", "en", "fi", "fr", "de", "hu", "it", "nb", "pt", "ro", "ru", "es", "sv"]
        """

        self.config = ConfigManager()

        if language is None:
            language = self.config.config['Corpus']['language']

        if iso639 is None:
            iso639 = self.config.config['Corpus']['iso639']

        if spacy_model is None:
            spacy_model = self.config.config['Spacy']['spacy_model_' + iso639]

        self.nlp_spacy = spacy.load(spacy_model)

        self.language = language
        self.iso639 = iso639

        self.stemmer = SnowballStemmer(language)

    def is_stopword(self, token: str) -> bool:
        """
        Returns True if the input token is a stopword, else False.

        Args:
            token (str): Text of the token that has to be checked.

        Returns:
            bool: True, if the token is a stopword, else False.

                    Example:
                    >> nlp = NLP()
                    >> nlp.is_stopword("beautiful")
                       False
                    >> nlp.is_stopword("of")
                       True
        """
        return token.lower() in self.stopwords_list()

    @staticmethod
    def is_ngram(token: str, sep: str = '_', n: int = None) -> bool:
        """
        Returns True if the input token is a stopword, else False.

        Args:
            token (str): Text of the token that has to be checked.
            sep (str, optional, default=_): The character separator that splits the n-gram into tokens.

                    Example:
                    - New_York -> [New, York]
                    - computer_science -> [computer, science]

            n (int, optional, default=None): If not None, checks if the input token is a n-gram of size n.

        Returns:
            bool: True, if the token is a n-gram, else False.

                    Example:
                    >> nlp = NLP()
                    >> nlp.is_ngram("New York")
                       False
                    >> nlp.is_ngram("New_York")
                       True
                    >> nlp.is_ngram("New_York", n=3)
                       False
                    >> nlp.is_ngram("New_York_is", n=3)
                       True
        """
        return token.count(sep) > 0 if n is None else token.count(sep) > n - 1

    @staticmethod
    def is_too_short(token: str, min_len: int) -> bool:
        """
        Returns True if token is shorter than min_len, else False.

        Args:
            token (str): Text of the token that has to be checked.
            min_len (int, optional, default=0): Tokens shorter than min_len are too short.

        Returns:
            bool: True, if the token is a too short, else False.

                    Example:
                    >> nlp = NLP()
                    >> nlp.is_too_short("NLP", min_len=2)
                       False
                    >> nlp.is_stopword("NLP", min_lent=4)
                       True
        """
        return len(token) >= min_len

    @staticmethod
    def is_lower(text: str) -> bool:
        """
        Returns True if text is a lowercase string, False otherwise.

        Args:
            text (str): The input text.

        Returns:
            bool: True, if the text is a lowercase string, False otherwise.

                    Example:
                    >> nlp = NLP()
                    >> nlp.is_lower("Consider your origin. You were not formed to live like brutes but to follow virtue and knowledge.")
                       False
                    >> nlp.is_lower("consider your origin. you were not formed to live like brutes but to follow virtue and knowledge.")
                       True
        """

        return text.islower()

    @staticmethod
    def is_upper(text: str) -> bool:
        """
        Returns True if text is a uppercase string, False otherwise.

        Args:
            text (str): The input text.

        Returns:
            bool: True, if the text is a uppercase string, False otherwise.

                    Example:
                    >> nlp = NLP()
                    >> nlp.is_upper("Consider your origin. You were not formed to live like brutes but to follow virtue and knowledge.")
                       False
                    >> nlp.is_upper("CONSIDER YOUR ORIGIN. YOU WERE NOT FORMED TO LIVE LIKE BRUTES BUT TO FOLLOW VIRTUE AND KNOWLEDGE.")
                       True
        """
        return text.isupper()

    @staticmethod
    def is_capitalize(text: str) -> bool:
        """
        Returns True if text is a capitalize string, False otherwise.

        Args:
            text (str): The input text.

        Returns:
            bool: True, if the text is a capitalize string, False otherwise.

                    Example:
                    >> nlp = NLP()
                    >> nlp.is_capitalize("Consider your origin. You were not formed to live like brutes but to follow virtue and knowledge.")
                       False
                    >> nlp.is_capitalize("Consider your origin. you were not formed to live like brutes but to follow virtue and knowledge.")
                       True
        """

        if len(text) < 2:
            return False

        return True if text[0].isupper() and text[1:].islower() else False

    @staticmethod
    def is_title(text: str) -> bool:
        """
        Returns True if text is a title string, False otherwise.

        Args:
            text (str): The input text.

        Returns:
            bool: True, if the text is a title string, False otherwise.

                    Example:
                    >> nlp = NLP()
                    >> nlp.is_title("Consider your origin. You were not formed to live like brutes but to follow virtue and knowledge.")
                       False
                    >> nlp.is_title("Consider Your Origin. You Were Not Formed To Live Like Brutes But To Follow Virtue And Knowledge.")
                       True
        """
        return text.istitle()

    @staticmethod
    def is_digit(token: str) -> bool:
        """
        Returns True if token is a digit string, False otherwise.

        Args:
            token (str): Text of the token that has to be checked.

        Returns:
            bool: True, if the token is a digit string, False otherwise.

                    Example:
                    >> nlp = NLP()
                    >> nlp.is_digit("1a2341g")
                       False
                    >> nlp.is_digit("11243")
                       True
        """
        return token.isdigit()

    @staticmethod
    def is_punct(token: str) -> bool:
        """
        Returns True if token is a punctuation character, False otherwise.

        Args:
            token (str): Text of the token that has to be checked.

        Returns:
            bool: True, if the token is a punctuation character, False otherwise.

                    Example:
                    >> nlp = NLP()
                    >> nlp.is_punct("word")
                       False
                    >> nlp.is_punct(".")
                       True
        """
        return token in string.punctuation

    @staticmethod
    def is_space(token: str) -> bool:
        """
        Returns True if token is a space character, False otherwise.

        Args:
            token (str): Text of the token that has to be checked.

        Returns:
            bool: True, if the token is a space character, False otherwise.

                    Example:
                    >> nlp = NLP()
                    >> nlp.is_space("word")
                       False
                    >> nlp.is_space(" ")
                       True
        """
        return token in string.whitespace

    @staticmethod
    def strip_punctuation(text: str, keep: Tuple[str, ...] = None, sc: Tuple[str, ...] = None) -> str:
        """
        Strips punctuation characters from a input text.

        Args:
            text (str): The input text.
            keep (Tuple[str, ...], optional, default=None): Punctuation characters to keep: they won't be stripped.
            sc (Tuple[str, ...], optional, default=None): Additional Special characters to be stripped.

        Returns:
            str: The text without punctuation characters.

                    Example:
                    >> nlp = NLP()
                    >> nlp.strip_punctuation("Consider your origin. You were not formed to live like brutes but to follow virtue and knowledge.")
                       "Consider your origin  you were not formed to live like brutes but to follow virtue and knowledge"
                    >> nlp.strip_punctuation("Cons ? der Your Or ? g ? n ✜!!! You Were Not Formed To Live Like Brutes But To Follow Virtue And Knowledge.",
                                        keep=["?"], sc=["✜"])
                       "Cons ? der Your Or ? g ? n      You Were Not Formed To Live Like Brutes But To Follow Virtue And Knowledge"
        """

        punctuation = string.punctuation
        if keep is not None and len(keep) > 0:
            punctuation = "".join([i for i in punctuation if i not in keep])
        if sc is not None and len(sc) > 0:
            punctuation += "".join(sc)

        if keep is not None:
            for k in keep:
                text = text.replace(k, ' ' + k + ' ')

        return text.translate(str.maketrans(dict.fromkeys(punctuation, ' '))).strip()

    @staticmethod
    def strip_accents(text: str) -> str:
        """
        Strips accents from a input text.

        Args:
            text (str): The input text.

        Returns:
            str: The text without accents characters.

                    Example:
                    >> nlp = NLP()
                    >> nlp.strip_accents("Nicolò sull’aereo salì ; per un bel viaggio partì.")
                       "Nicolo sull’aereo sali ; per un bel viaggio parti"
        """
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').strip()

    def strip_stopwords(self, text: str, min_len: int = 0) -> str:
        """
        Strips accents from a input text.

        Args:
            text (str): The input text.
            min_len (int, optional, default=0): Tokens shorter than min_len are stripped as stopwords.

        Returns:
            str: The text without accents characters.

                    Example:
                    >> nlp = NLP()
                    >> nlp.strip_stopwords("Consider your origin. You were not formed to live like brutes but to follow virtue and knowledge.")
                    "Consider origin. formed live like brutes follow virtue knowledge."
        """
        return " ".join(
            [token for token in text.split() if not self.is_stopword(token) and len(token) > min_len]).lower()

    @staticmethod
    def lower(text: str) -> str:
        """
        Returns a copy of the string converted to lowercase.

        Args:
            text (str): The input text.

        Returns:
            str: A copy of the string converted to lowercase.

                    Example:
                    >> nlp = NLP()
                    >> nlp.lower("Consider your origin. You were not formed to live like brutes but to follow virtue and knowledge.")
                    "consider your origin. you were not formed to live like brutes but to follow virtue and knowledge."
        """
        return text.lower()

    @staticmethod
    def upper(text: str) -> str:
        """
        Returns a copy of the string converted to uppercase.

        Args:
            text (str): The input text.

        Returns:
            str: A copy of the string converted to uppercase.

                    Example:
                    >> nlp = NLP()
                    >> nlp.upper("Consider your origin. You were not formed to live like brutes but to follow virtue and knowledge.")
                    "CONSIDER YOUR ORIGIN. YOU WERE NOT FORMED TO LIVE LIKE BRUTES BUT TO FOLLOW VIRTUE AND KNOWLEDGE."
        """
        return text.upper()

    @staticmethod
    def capitalize(text: str) -> str:
        """
        Returns a copy of the string converted to capitalize.

        Args:
            text (str): The input text.

        Returns:
            str: A copy of the string converted to capitalize.

                    Example:
                    >> nlp = NLP()
                    >> nlp.capitalize("Consider your origin. You were not formed to live like brutes but to follow virtue and knowledge.")
                    "Consider your origin. you were not formed to live like brutes but to follow virtue and knowledge."
        """
        return text.capitalize()

    @staticmethod
    def title(text: str) -> str:
        """
        Returns a copy of the string converted to title.

        Args:
            text (str): The input text.

        Returns:
            str: A copy of the string converted to title.

                    Example:
                    >> nlp = NLP()
                    >> nlp.title("Consider your origin. You were not formed to live like brutes but to follow virtue and knowledge.")
                    "Consider Your Origin. You Were Not Formed To Live Like Brutes But To Follow Virtue And Knowledge."
        """
        return text.title()

    def stem(self, token: str) -> str:
        """
        Strips affixes from the token and returns the stem.

        Args:
            token (str): The text of the input token.

        Returns:
            str: Returns the stem of the token.

                    Example:
                    >> nlp = NLP()
                    >> nlp.stem("beautiful")
                       "beauti"
        """
        return self.stemmer.stem(token)

    def split_skipgram(self, text: str, ws: int = 3) -> List[str]:
        """
        Returns a list of tokens as union of the tokens of each skipgrams pair.

        Args:
            text (str): The input text.
            ws (int, optional, default=3): Window size: size of sampling windows. <br/> The window of a word w_i will be [i-window_size, i+window_size+1]

        Returns:
            List[str]: A list of tokens as union of the tokens of each skipgrams pair.

                    Example:
                    >> nlp = NLP()
                    >> nlp.split_skipgram(text="My mistress' eyes are nothing like the sun", ws=2)

                    ["My", "mistress'", "My", "eyes", "My", "are", "mistress"", "eyes", "mistress'", "are", "mistress'", "nothing",
                    "eyes", "are", "eyes", "nothing", "eyes", "like", "are", "nothing", "are", "like", "are", "the",
                    "nothing", "like", "nothing", "the", "nothing", "sun", "like", "the", "like", "sun", "the", "sun"]
        """

        tokens = list()
        for skipgram in self.skipgrams(text, ws):
            tokens.extend(skipgram)
        return tokens

    def stopwords_list(self, include: List[str] = None) -> List[str]:
        """
        Returns a stopwords list.

        Args:
            include (List[str], optional, default=None): Include a list of arbitrary stopwords.

        Returns:
            List[str]: a list of stopwords.

                    Example:
                    >> nlp = NLP()
                    >> nlp.stopwords_list()
                       ["of", "a", "the", "some", ...]
                    >> nlp.stopwords_list(include=["my_word"])
                       ["my_word", "of", "a", "the", ...]
        """

        if not hasattr(self, 'stopwords'):
            self.stopwords = stopwords.words(self.language)
            if include is not None:
                self.stopwords.extend([s.lower() for s in include])

        return self.stopwords

    def ngrams(self, text: str, n: int, pos: Tuple[str] = ("PROPN", "VERB", "NOUN", "ADJ"),
               threshold: int = 50) -> Dict[str, int]:
        """
        Returns the most frequent n-grams in the text.

        Args:
            text (str): Input text.
            n (int): The size of n-grams: number of sequential strings that make up n-grams.
            pos (Tuple[str, ...], optional, default=PROPN,VERB,NOUN,ADJ): Part of speech of the first and the last token that make up n-grams. <br/> Filters the most informative n-grams. <br/> If None, the filter will be ignored.

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

            threshold (int, optional, default=50): Filters n-grams that have a frequency greater than threshold.

        Returns:
             Dict[str, int]: N-grams as keys, frequencies as values.

                        Example:
                        >> nlp = NLP()
                        >> text = "New York City (NYC), often called simply New York, is the most populous city in the United States. With an estimated 2019 population of 8,336,817 distributed over about 302.6 square miles (784 km2), New York City is also the most densely populated major city in the United States.[11] Located at the southern tip of the U.S. state of New York, the city is the center of the New York metropolitan area, the largest metropolitan area in the world by urban landmass.[12] With almost 20 million people in its metropolitan statistical area and approximately 23 million in its combined statistical area, it is one of the world's most populous megacities. New York City has been described as the cultural, financial, and media capital of the world, significantly influencing commerce,[13] entertainment, research, technology, education, politics, tourism, art, fashion, and sports. Home to the headquarters of the United Nations,[14] New York is an important center for international diplomacy."
                        >> nlp.ngrams(text, n=2, threshold=5)
                           {"New York": 6}
                        >> nlp.ngrams(text, n=3, threshold=3)
                           {"New York City": 6}
        """

        # Ngrams dict {ngram: frequency}
        ngram_frequencies = defaultdict(lambda: 1)

        # Scan of each source using a Sliding Window
        # Index Sliding Window
        c = 0

        # From text source to token list
        tokens = text.split()

        # Shift the Sliding Window until it covers the last token
        while c < len(tokens) - (n - 1):
            c += 1

            # First and last word can't be stopwords
            if self.is_stopword(tokens[c - 1]) or \
                    self.is_stopword(tokens[c + (n - 1) - 1]):
                continue

            ngram = tuple([tokens[c + i - 1] for i in range(0, n)])
            ngram_frequencies[ngram] = ngram_frequencies[ngram] + 1

        # Select the n grams you're interested in
        ngram_frequencies = {ngram: frequency for ngram, frequency in ngram_frequencies.items() if
                             frequency > threshold}

        if pos is None or len(pos) == 0:
            return ngram_frequencies

        # Ngram final list
        result = defaultdict(int)

        # First and last word must be in pos
        for ngram in ngram_frequencies:
            ngram_ = self.nlp_spacy(" ".join(ngram))
            if ngram_[0].pos_ in pos and ngram_[-1].pos_ in pos:
                ngram_ = " ".join([token.text for token in ngram_])
                result[ngram_] = ngram_frequencies[ngram]

        return result

    @staticmethod
    def skipgrams(text: str, ws: int = 3) -> List[Tuple[str, str]]:
        """
        Generates skipgram word pairs.

        Args:
            text (str): The input text.
            ws (int, optional, default=3): Window size: size of sampling windows. <br/> The window of a word w_i will be [i-window_size, i+window_size+1]

        Returns:
            List[Tuple[str, str]]: A list of tuple (skipgram pairs).

                    Example:
                    >> nlp = NLP()
                    >> nlp.skipgrams(text="My mistress' eyes are nothing like the sun", ws=2)
                        [("My", "mistress'"), ("My", "eyes"), ("My", "are"),
                        ("mistress"", "eyes"), ("mistress'", "are"), ("mistress"", "nothing"),
                        ("eyes", "are"), ("eyes", "nothing"), ("eyes", "like"),
                        ("are", "nothing"), ("are", "like"), ("are", "the"),
                        ("nothing", "like"), ("nothing", "the"), ("nothing", "sun"),
                        ("like", "the"), ("like", "sun"), ("the", "sun")]
        """

        skipgrams = []
        tokens = text.split()

        ws += 1
        for i in range(0, len(tokens) - 1):
            for j in range(1, ws + 1):
                if i != len(tokens) - j and i + j < len(tokens):
                    skipgrams.append((tokens[i], tokens[i + j]))

        return skipgrams

    def named_entities(self, text: str) -> List[Dict[str, Union[str, int]]]:
        """
        Returns a list of named entities in text.

        Args:
            text (str): The input text.

        Returns:
            List[Dict[str, Union[str, int]]]: A list of named entities. Each named entity is a dict with three keys:

                * _text_: the named entity
                * _start_: the position of the first token of the Named Entities in the text.
                * _end_: the position of the last token of the Named Entities in the text.

                    Example:
                    >> nlp = NLP()
                    >> nlp.named_entities(text="As former US President, Barack Obama said, 'Climate change is no longer some far off problem. It is happening here. It is happening now.'")
                      [
                       {"text": "US President", "start": 2, "end": 3"},
                       {"text": "Barack Obama", "start":4, "end":5},
                       {"text": "Climate", "start":6, "end": 6}
                      ]
        """
        import unidecode

        # cler text
        text = unidecode.unidecode(text)
        #text = self.strip_punctuation(text)

        if len(text) < 2:
            return []

        # find Named Entities by regex
        #"(?:(?<=^)|(?<=[^.]))\s+([A-Z]\w+)"
        named_entities = [{'start': m.start(0), 'end': m.end(0), 'text': m.group(0)}
                          for m in re.finditer("([A-Z]+[a-z]*)", text[0].capitalize() + text[1:], re.UNICODE)
                          if not self.is_stopword(m.group(0).lower())]

        text_spans = self.spans(text)

        # One or less named entities
        if len(named_entities) == 0:
            return list()
        elif len(named_entities) == 1:
            # pos start, pos end for each named entities
            for k, v in text_spans.items():
                if named_entities[0]['start'] in range(*k):
                    named_entities[0]['start'] = v
                    break

            for k, v in text_spans.items():
                if (named_entities[0]['end'] - 1) in range(*k):
                    named_entities[0]['end'] = v
                    break
            return [named_entities[0]]

        # Link consecutive named entities
        result = [named_entities[0]]
        for named_entity in named_entities[1:]:
            if result[-1]['end'] == named_entity['start'] - 1:
                result[-1]['text'] += " "+named_entity['text']
                result[-1]['end'] = named_entity['end']
            else:
                result.append(named_entity)

        # pos start, pos end for each named entities
        for ne in result:
            for k, v in text_spans.items():
                if ne['start'] in range(*k):
                    ne['start'] = v
                    break

            for k, v in text_spans.items():
                if (ne['end'] - 1) in range(*k):
                    ne['end'] = v
                    break
        return result

    @staticmethod
    def spans(text) -> Dict[Tuple[int, int], int]:
        """
        Returns the starting and ending character index for each token in the text.

        Args:
            text (str): The input text.

        Returns:
            Dict[Tuple[int, int], int]: A dict containing the the starting and ending character index for each token in the text as keys;
            and the token index for each token in text as values.

                    Example:
                    >> nlp = NLP()
                    >> nlp.spans("Consider your origin . You were not formed to live like brutes but to follow virtue and knowledge .")
                    {(0, 8): 0, (9, 13): 1, (14, 20): 2, (21, 22): 18, (23, 26): 4, (27, 31): 5, (32, 35): 6, (36, 42): 7, (43, 45): 13, (46, 50): 9, (51, 55): 10, (56, 62): 11, (63, 66): 12, (70, 76): 14, (77, 83): 15, (84, 87): 16, (88, 97): 17}

        """
        result = dict()
        point = 0  # Where we're in the text.

        for t, fragment in enumerate(text.split()):
            found_start = text.index(fragment, point)
            found_end = found_start + len(fragment)
            result[(found_start, found_end)] = t
            point = found_end

        return result

    def negated_tokens(self, t: Union[str, Doc]) -> List[bool]:
        """Returns a mask that specifies which tokens are negated in the text.

        Args:
            text (Union[str, spacy.tokens.doc.Doc]): The input text that has to be analyzed.

        Returns:
            bool: A mask that specifies which tokens are negated in the text.

                    Example:
                    >> nlp = NLP()
                    >> nlp.negated_tokens("She is neither beautiful nor smart, but She is so kind")
                       [False, False, False, True, False, True, False, False, False, False, False, False]
        """

        global negations

        tokens = t if type(t) is Doc else self.nlp_spacy(t)
        mask, negated = [], []

        # All children tokens linked to a parent token by a negation relationship
        for token in tokens:
            if token.dep_ == "neg" or token.text in negations[self.iso639]:
                negated += [x for x in token.head.children] + [token.head]

        for token in tokens:

            # All children tokens linked to a parent token by a negation relationship and
            # All tokens attached to a modifying adjective or adverb
            if (token in negated or (token.dep_ in ["amod", "advmod"] and token.head in negated)) and \
                    token.text not in negations[self.iso639]:
                mask.append(True)
                continue

            mask.append(False)
        return mask
