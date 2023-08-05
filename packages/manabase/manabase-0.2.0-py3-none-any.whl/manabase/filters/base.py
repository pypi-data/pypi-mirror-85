"""A simple filter interface."""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Optional

from pydantic.main import BaseModel

from ..cards import Card


class CardFilter(BaseModel, metaclass=ABCMeta):
    """Filter than can be chained using bitwise operators.

    Example::
    ```python
    >>> from manabase.cards import Card
    >>> from manabase.colors import Color
    >>> from manabase.filters.base import CardFilter, FilterResult
    >>> class WhiteColorFilter(CardFilter):
    ...     def filter_card(self, card: Card) -> FilterResult:
    ...         if Color.white.value in card.colors:
    ...             return FilterResult(card=card, accepted_by=self)
    ...         return FilterResult(card=card)
    >>> class BlueColorFilter(CardFilter):
    ...     def filter_card(self, card: Card) -> FilterResult:
    ...         if Color.blue.value in card.colors:
    ...             return FilterResult(card=card, accepted_by=self)
    ...         return FilterResult(card=card)
    >>> class AndOperator(CardFilter):
    ...     left: CardFilter
    ...     right: CardFilter
    ...     def filter_card(self, card: Card) -> FilterResult:
    ...         left = self.left.filter_card(card)
    ...         if left.accepted_by is None:
    ...             return FilterResult(card=card)
    ...         return self.right.filter_card(card)
    >>> operator = AndOperator(left=WhiteColorFilter(), right=BlueColorFilter())
    >>> card = Card(
    ...     name="",
    ...     oracle_text="",
    ...     colors=[],
    ...     color_identity=[],
    ...     produced_mana=["W"],
    ...     legalities={},
    ...     textless=False,
    ...     scryfall_uri="",
    ... )
    >>> operator.filter_card(card)
    FilterResult(card=Card(...), accepted_by=None)
    >>> card.colors = ["W", "U"]
    >>> operator.filter_card(card)
    FilterResult(card=Card(...), accepted_by=BlueColorFilter(...))
    >>> card.colors = ["U"]
    >>> operator.filter_card(card)
    FilterResult(card=Card(...), accepted_by=None)

    ```
    """

    @abstractmethod
    def filter_card(self, card: Card) -> FilterResult:
        """Filter a single card.

        Example::

        ```python
        >>> from manabase.colors import Color
        >>> from manabase.filters.base import CardFilter, FilterResult
        >>> class WhiteColorFilter(CardFilter):
        ...     def filter_card(self, card: Card) -> FilterResult:
        ...         if Color.white.value in card.colors:
        ...             return FilterResult(card=card, accepted_by=self)
        ...         return FilterResult(card=card)
        >>> filter_ = WhiteColorFilter()
        >>> card = Card(
        ...     name="",
        ...     oracle_text="",
        ...     colors=[],
        ...     color_identity=[],
        ...     produced_mana=[],
        ...     legalities={},
        ...     textless=False,
        ...     scryfall_uri="",
        ... )
        >>> filter_.filter_card(card)
        FilterResult(card=Card(...), accepted_by=None)
        >>> card.colors = ["W"]
        >>> filter_.filter_card(card)
        FilterResult(card=Card(...), accepted_by=WhiteColorFilter(...))

        ```
        """


class FilterResult(BaseModel):
    """Result of a filter operation.

    `FilterResult.accepted_by` is filled with the filter that accepted the card.
    """

    card: Card
    accepted_by: Optional[CardFilter] = None
