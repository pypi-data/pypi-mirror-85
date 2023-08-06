from typing import *
from compling.config import ConfigManager
import compling.analysis.lexical.tokenization.document_abc as abcdoc
from compling.analysis.lexical.tokenization.impl.paragraph import Paragraph


class Document(abcdoc.Document):
    def __init__(self, doc_id: int, para_list: List[Paragraph], config: ConfigManager, metadata: dict) -> None:
        """
        Represents a generic document, which is a sequence of paragraph in the input.
        A document is identified by grouping a list of paragraph.

        Args:
           doc_id (int): unique document identifier.
           para_list (List[Paragraph]): The list of paragraphs making up the document.
           config (ConfigManager): a ConfigManager object.
           metadata (dict): token metadata as a key-value pairs.

        Returns:
           None.
       """

        # unique identifiers
        self.doc_id_ = doc_id

        # document
        self.text_ = " . ".join([sentence.text() for sentence in para_list])

        # paragraph list
        self.para_list = para_list

        # add some field only if the value in config.ini file is True
        for k, v in config.config['Document_record'].items():
            if int(v):
                setattr(self, k + '_', getattr(self, k)())

        # add metaddata for this document record
        self.add_metadata(metadata)

    def named_entities(self) -> List[Dict[str, Union[str, int]]]:
        """Returns named entities in the document."""

        named_entities = list()
        offset = 0
        for i, para in enumerate(self.para_list):
            if i > 0:
                offset = sum([len(self.para_list[s].text_.split()) for s in range(0, i)])

            for ne in para.named_entities():
                ne_ = dict()
                ne_['doc_pos_start_'] = ne['para_pos_start_'] + offset
                ne_['doc_pos_end_'] = ne['para_pos_end_'] + offset
                ne_['text_'] = ne['text_']
                named_entities.append(ne_)

        return named_entities

    def text(self) -> str:
        """Returns the text of the document."""
        return self.text_

    def lower(self) -> str:
        """Returns the lower of the document."""
        return self.text_.lower()

    def lemma(self) -> str:
        """Returns a version of the document text with tokens replace by their lemma."""
        return " . ".join([sentence.lemma() for sentence in self.para_list])

    def negations(self) -> str:
        """Returns the text of the document where the text of negated tokens are preceded by the prefix 'NOT_'."""

        return " . ".join([para.negations() for para in self.para_list])

    def stem(self) -> str:
        """Returns a version of the document text with tokens replace by their stem."""
        return " . ".join([sentence.stem() for sentence in self.para_list])

    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the document."""
        for k, v in metadata.items():
            if hasattr(self, k + '_'):
                continue
            setattr(self, k + '_', v)

    def to_dict(self) -> dict:
        """Converts the document to a dict record."""
        return {k: v for k, v in self.__dict__.items() if k.endswith('_')}
