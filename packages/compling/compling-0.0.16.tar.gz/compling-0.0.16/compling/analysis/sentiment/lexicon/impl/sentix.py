import csv
import pkg_resources
from compling.analysis.sentiment.lexicon.lexicon import Lexicon
from collections import defaultdict
from typing import Tuple

csv.field_size_limit(1000000)

__sentix__ = pkg_resources.resource_filename('compling', 'senti-lexicons/sentix.csv')

class Sentix(Lexicon):
    """Sentix Lexicon Implementation of Lexicon Abastract Class.

    Italian Language.

    http://valeriobasile.github.io/twita/sentix.html
    """

    def __init__(self, pos: Tuple[str, str]=('ADJ', 'ADV')) -> None:
        self.sentiment = defaultdict(lambda: defaultdict(float))

        with open(__sentix__, encoding='utf-8', mode='r') as f:
            rows = csv.reader(f, delimiter='\t')

            columns = next(rows)

            for row in rows:
                record = dict(zip(columns, row))
                lemma, synset = record['lemma'], record['POS']
                self.sentiment[lemma][synset] = record

        senti_pos_dict = {'n': 'NOUN', 'v': 'VERB', 'a': 'ADJ', 's': 'ADJ', 'r': 'ADV'}
        self.pos = [k for k, v in senti_pos_dict.items() if v in pos or pos is None or len(pos) == 0]

    def polarity(self, token:str) -> dict:
        """
        Returns the token polarities.

        Args:
            token (str): The text of the input token.

        Returns:
            dict: Polarities type as keys, sentiment values as values.

                    Example:
                    {
                     'pos' : 0.9,
                     'neg' : 0.1,
                     'obj' : 0.3
                    }
        """

        polarities = dict({'neg': 0, 'pos': 0, 'obj': 0})

        if token.replace("NOT_", "") not in self.sentiment:
            return polarities

        for synset in self.sentiment[token.replace("NOT_", "")]:
            if not synset in self.pos:
                continue

            if token.startswith('NOT_'):
                polarities['neg'] += float(self.sentiment[token.replace("NOT_", "")][synset]['pos'])
                polarities['pos'] += float(self.sentiment[token.replace("NOT_", "")][synset]['neg'])
            else:
                polarities['pos'] += float(self.sentiment[token.replace("NOT_", "")][synset]['pos'])
                polarities['neg'] += float(self.sentiment[token.replace("NOT_", "")][synset]['neg'])

        return polarities