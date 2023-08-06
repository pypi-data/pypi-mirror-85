from nltk.corpus import sentiwordnet as swn
from compling.analysis.sentiment.lexicon.lexicon import Lexicon
from typing import Tuple

class Sentiwordnet(Lexicon):
    """Sentiwordnet Lexicon Implementation of Lexicon Abastract Class."""

    def __init__(self, pos: Tuple[str, str]=('ADJ', 'ADV')) -> None:
        """
        **\_\_init\_\_**: Creates a new Sentiwordnet object.

        Args:
            pos (Tuple[str], optional, default=ADJ,ADV): SentiWordNet Lexicon returns a token polarities for each part of speech that token may have in the speech. <br/> If not None, filters the token polarities for part of speech in the pos tuple.

        This class sums the polarity value of the parts of speech you choose
        """
        senti_pos_dict = {'n': 'NOUN', 'v': 'VERB', 'a': 'ADJ', 's': 'ADJ', 'r': 'ADV'}
        self.pos = [k for k, v in senti_pos_dict.items() if v in pos or pos is None or len(pos) == 0]

    def polarity(self, token: str) -> dict:
        """
        Returns the token polarities.

        Args:
            token (str): The text of the input token.

        Args:
            dict: Polarities type as keys, sentiment values as values.

                    Example:
                    {
                     'pos' : 0.9,
                     'neg' : 0.1,
                     'obj' : 0.3
                    }
        """

        senti_synsets = [senti_synset for senti_synset in list(swn.senti_synsets(token.replace("NOT_", "")))
                 if senti_synset.synset._pos in self.pos ]

        polarities = dict({'neg': 0, 'pos': 0, 'obj': 0})
        for senti_synset in senti_synsets:
            if token.startswith('NOT_'):
                polarities['neg'] += senti_synset.pos_score()
                polarities['pos'] += senti_synset.neg_score()
            else:
                polarities['pos'] += senti_synset.pos_score()
                polarities['neg'] += senti_synset.neg_score()
            polarities['obj'] += senti_synset.obj_score()
        return polarities