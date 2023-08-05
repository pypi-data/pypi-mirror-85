import abc
from typing import *


class Sentence(metaclass=abc.ABCMeta):
    """
    Represents a generic sentence, which is a sequence of tokens in the input.
    A sentence is identified using a tokenizer, which breaks up the sequence of characters in the input into a sequence
    of tokens.
    """

    @abc.abstractmethod
    def named_entities(self) -> List[str]:
        """Returns named entities in the sentence."""

    @abc.abstractmethod
    def text(self) -> str:
        """Return the text of the sentence."""

    @abc.abstractmethod
    def lower(self) -> str:
        """Return the lowercase version of the sentence text."""

    @abc.abstractmethod
    def negations(self) -> str:
        """Return the text of the sentence where the text of negated tokens are preceded by the prefix 'NOT_'"""

    @abc.abstractmethod
    def lemma(self) -> str:
        """Returns a version of the sentence text with tokens replace by their lemma."""

    @abc.abstractmethod
    def stem(self) -> str:
        """Returns a version of the sentence text with tokens replace by their stem."""

    @abc.abstractmethod
    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the sentence."""

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """Converts the sentence to a dict record."""