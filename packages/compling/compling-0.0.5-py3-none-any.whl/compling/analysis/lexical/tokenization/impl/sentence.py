from typing import *
import compling.nlptoolkit as nlptoolkit
from compling.config import ConfigManager
import compling.analysis.lexical.tokenization.sentence_abc as abcsent
from compling.analysis.lexical.tokenization.impl.token import Token


class Sentence(abcsent.Sentence):
    def __init__(self, sent_id: int, token_id: int, sent: str, nlp: nlptoolkit.NLP, config: ConfigManager,
                 para_id: int, doc_id: int,
                 para_pos: int, doc_pos: int, metadata: dict) -> None:
        """
        Represents a generic sentence, which is a sequence of tokens in the input.
        A sentence is identified using a tokenizer, which breaks up the sequence of characters in the input into a sequence
        of tokens.

        Args:
           sent_id (int): unique sentence identifier.
           token_id (int): unique token identifier. The token_id of the first token in the sentence.
           sent (str): text of the sentence.
           nlp (NLP): a Natural Language Processing object.
           config (ConfigManager): a Config manager object.
           para_id (int): unique paragraph identifier. The id of the paragraph the sentence occurs in.
           doc_id (int): unique document identifier. The id of the document the sentence occurs in.
           para_pos (int): position index in the paragraph of the first token in the sentence.
           doc_pos (int): position index in the document of the first token in the sentence.
           metadata (dict): token metadata as a key-value pairs.

        Returns:
           None.
        """

        # unique identifiers
        self.token_id = token_id
        self.sent_id_ = sent_id

        # Natural Language Object
        self.nlp = nlp

        # sentence
        self.text_ = sent

        # position index
        self.para_pos = para_pos
        self.doc_pos = doc_pos

        # token list
        sentence = nlp.nlp_spacy(sent)
        # find negated token
        negation_mask = nlp.negated_tokens(sentence)
        self.token_list = [Token(self.next_token_id(), token, nlp, config,
                                 sent_id, para_id, doc_id,
                                 sent_pos, self.next_para_pos(), self.next_doc_pos(), negation_mask[sent_pos], metadata)
                           for sent_pos, token in enumerate(sentence)]

        # add some field only if the value in config.ini file is True
        for k, v in config.config['Sentence_record'].items():
            if int(v):
                setattr(self, k + '_', getattr(self, k)())

        # add metadata for this sentence record
        self.add_metadata(metadata)

    def named_entities(self) -> List[Dict[str, Union[str, int]]]:
        """Returns named entities in the sentence."""
        named_entities = self.nlp.named_entities(self.text_)

        for ne_ in named_entities:
            ne_['sent_pos_start_'] = ne_.pop('start')
            ne_['sent_pos_end_'] = ne_.pop('end')
            ne_['text_'] = ne_.pop('text')

        return named_entities

    def next_para_pos(self) -> int:
        """Returns the next token position in the paragraph."""
        self.para_pos += 1
        return self.para_pos

    def next_doc_pos(self) -> int:
        """Returns the next token position in the document."""
        self.doc_pos += 1
        return self.doc_pos

    def next_token_id(self) -> int:
        """Returns the next token id."""
        self.token_id += 1
        return self.token_id

    def text(self) -> str:
        """Return the text of the sentence."""
        return self.text_

    def lower(self) -> str:
        """Return the lowercase version of the sentence text."""
        return self.text_.lower()

    def negations(self) -> str:
        """Return the text of the sentence where the text of negated tokens are preceded by the prefix 'NOT_'"""
        text = lambda token: 'NOT_' + token.text() if token.is_negated_ else token.text()

        return " ".join([text(token) for token in self.token_list])

    def lemma(self) -> str:
        """Returns a version of the sentence text with tokens replace by their lemma."""
        return " ".join([token.lemma() for token in self.token_list])

    def stem(self) -> str:
        """Returns a version of the sentence text with tokens replace by their stem."""

        return " ".join([token.stem() for token in self.token_list])

    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the sentence."""
        for k, v in metadata.items():
            if hasattr(self, k + '_'):
                continue
            setattr(self, k + '_', v)
        for token in self.token_list:
            token.add_metadata(metadata)

    def to_dict(self) -> dict:
        """Converts the sentence to a dict record."""
        return {k: v for k, v in self.__dict__.items() if k.endswith('_')}
