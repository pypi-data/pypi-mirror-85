from typing import *
from compling.config import ConfigManager
import compling.analysis.lexical.tokenization.paragraph_abc as abcpara
from compling.analysis.lexical.tokenization.impl.sentence import Sentence


class Paragraph(abcpara.Paragraph):
    def __init__(self, para_id: int, sent_list: List[Sentence], config: ConfigManager, metadata: dict) -> None:
        """
        Represents a generic paragraph, which is a sequence of sentence in the input.
        A paragraph is identified by grouping a list of sentence.

        Args:
           para_id (int): unique paragraph identifier.
           sent_list (List[Sentence]): The list of sentences making up the paragraph.
           config (ConfigManager): a ConfigManager object.
           metadata (dict): token metadata as a key-value pairs.

        Returns:
           None.
        """

        # unique identifiers
        self.para_id_ = para_id

        # paragraph
        self.text_ = " . ".join([sentence.text() for sentence in sent_list])

        # sentence list
        self.sent_list = sent_list

        # add some field only if the value in config.ini file is True
        for k, v in config.config['Paragraph_record'].items():
            if int(v):
                setattr(self, k + '_', getattr(self, k)())

        # add metadata for this paragraph record
        self.add_metadata(metadata)

    def named_entities(self) -> List[Dict[str, Union[str, int]]]:
        """Returns named entities in the paragraph."""

        named_entities = list()
        offset = 0
        for i, sent in enumerate(self.sent_list):
            if i > 0:
                offset = sum([len(self.sent_list[s].text_.split()) for s in range(0, i)])

            for ne in sent.named_entities():
                ne_ = dict()
                ne_['para_pos_start_'] = ne['sent_pos_start_'] + offset
                ne_['para_pos_end_'] = ne['sent_pos_end_'] + offset
                ne_['text_'] = ne['text_']
                named_entities.append(ne_)

        return named_entities

    def text(self) -> str:
        """Return the text of the paragraph."""
        return self.text_

    def lower(self) -> str:
        """Return the lowercase text of the paragraph."""
        return self.text_.lower()

    def lemma(self) -> str:
        """Returns a version of the paragraph text with tokens replace by their lemma."""

        return " . ".join([sentence.lemma() for sentence in self.sent_list])

    def negations(self) -> str:
        """Return the text of the paragraph where the text of negated tokens are preceded by the prefix 'NOT_'."""

        return " . ".join([sent.negations() for sent in self.sent_list])

    def stem(self) -> str:
        """Returns a version of the paragraph text with tokens replace by their stem."""
        return " . ".join([sentence.stem() for sentence in self.sent_list])

    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the paragraph."""
        for k, v in metadata.items():
            if hasattr(self, k + '_'):
                continue
            setattr(self, k + '_', v)

    def to_dict(self) -> dict:
        """Converts the paragraph to a dict record."""
        return {k: v for k, v in self.__dict__.items() if k.endswith('_')}
