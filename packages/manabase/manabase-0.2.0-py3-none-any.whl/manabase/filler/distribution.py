"""Compute cards distributions."""
from abc import ABCMeta, abstractmethod
from math import ceil
from typing import List

from pydantic import BaseModel

from ..cards import Card, CardList, MaximumSizeExceeded


class Distribution(BaseModel, metaclass=ABCMeta):
    """Computes a distribution of cards."""

    maximum: int

    @abstractmethod
    def compute(self, cards: List[Card]) -> CardList:
        """Compute a card list filled with `Distribution.cards`.

        Occurrences of each card are based on `Distribution.weights`.

        Example::

        ```python
        >>> from manabase.filler.distribution import Distribution
        >>> from manabase.cards import CardList
        >>> class SimpleDistribution(Distribution):
        ...     def compute(self, cards):
        ...         card_list = CardList(self.maximum)
        ...         for card in cards:
        ...             card_list.add_card(card, 1)
        ...         return card_list
        >>> cards = [Card.named('card 1')]
        >>> distribution = SimpleDistribution(maximum=1)
        >>> distribution.compute(cards)
        CardList(entries=[CardEntry(name='card 1'...)], ...)

        ```
        """


class WeightedDistribution(Distribution):
    """Perform a weighted distribution of cards.

    Example::

    ```python
    >>> from manabase.filler.distribution import WeightedDistribution
    >>> cards = [Card.named("Plains"), Card.named("Island"), Card.named("Swamp")]
    >>> weights = [3, 1, 3]
    >>> distribution = WeightedDistribution(maximum=21, weights=weights)
    >>> distribution.compute(cards)
    CardList(entries=[CardEntry(name='Plains'...occurrences=9), CardEntry(name='Island'\
...occurrences=3), CardEntry(name='Swamp'...occurrences=9)]...)

    ```
    """

    weights: List[int]

    def compute(self, cards: List[Card]) -> CardList:
        """Compute a card list filled with `Distribution.cards`.

        Occurrences of each card are based on `Distribution.weights`.

        Raises:
            ValueError: If the number of cards does not match the number of weights.
        """
        if len(self.weights) != len(cards):
            raise ValueError(
                f"Weighted distribution should be computed on {len(cards)} cards."
            )
        card_list = CardList(self.maximum)
        total_weight = sum(self.weights)

        for card, weight in zip(cards, self.weights):

            occurrences = ceil(weight * self.maximum / total_weight)

            try:
                card_list.add_card(card, occurrences)
            except MaximumSizeExceeded:
                if card_list.available:
                    card_list.add_card(card, card_list.available)
                break

        return card_list
