"""Implements a filter tree using bitwise operators.

Filters can be chained together using bitwise operators.

Example::

```python
>>> from manabase.cards import Card
>>> from manabase.filters.composite import CompositeFilter, FilterResult
>>> class ColorFilter(CompositeFilter):
...     color: str
...     def filter_card(self, card: Card) -> FilterResult:
...         if self.color in card.colors:
...             return FilterResult(card=card, accepted_by=self)
...         return FilterResult(card=card)
>>> filters = ColorFilter(color="W") & ColorFilter(color="U")
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
>>> filters.filter_card(card)
FilterResult(card=Card(...), accepted_by=None)
>>> card.colors = ["W"]
>>> filters.filter_card(card)
FilterResult(card=Card(...), accepted_by=None)
>>> card.colors = ["U"]
>>> filters.filter_card(card)
FilterResult(card=Card(...), accepted_by=None)
>>> card.colors = ["W", "U"]
>>> filters.filter_card(card)
FilterResult(card=Card(...), accepted_by=ColorFilter(...))

```
"""
from __future__ import annotations

from abc import ABCMeta

from ..cards import Card
from .base import CardFilter, FilterResult


class CompositeFilter(CardFilter, metaclass=ABCMeta):
    """A filter that can be chained to other filters using bitwise operators."""

    def __and__(self, other: CompositeFilter) -> CompositeFilter:
        return AndOperator(left=self, right=other)

    def __or__(self, other: CompositeFilter) -> CompositeFilter:
        return OrOperator(left=self, right=other)

    def __xor__(self, other: CompositeFilter) -> CompositeFilter:
        return XorOperator(left=self, right=other)

    def __invert__(self) -> CompositeFilter:
        return InvertOperator(leaf=self)


class AndOperator(CompositeFilter):
    """An ``and`` operator.

    The two filters should return ``True`` to let the value through.
    """

    left: CompositeFilter
    right: CompositeFilter

    def filter_card(self, card: Card) -> FilterResult:
        left = self.left.filter_card(card)
        if left.accepted_by is None:
            return FilterResult(card=card)
        return self.right.filter_card(card)


class OrOperator(CompositeFilter):
    """An ``or`` operator.

    At least one of the two filters should return ``True`` to let the value through.
    """

    left: CompositeFilter
    right: CompositeFilter

    def filter_card(self, card: Card) -> FilterResult:
        left = self.left.filter_card(card)
        if left.accepted_by is not None:
            return left
        right = self.right.filter_card(card)
        return right


class XorOperator(CompositeFilter):
    """An ``xor`` operator.

    Exactly one of the two filters should return ``True`` to let the value through.
    """

    left: CompositeFilter
    right: CompositeFilter

    def filter_card(self, card: Card) -> FilterResult:
        left = self.left.filter_card(card)
        right = self.right.filter_card(card)
        if left.accepted_by is not None and right.accepted_by is not None:
            return FilterResult(card=card)
        if left.accepted_by is None and right.accepted_by is None:
            return FilterResult(card=card)
        if left.accepted_by is not None:
            return FilterResult(card=card, accepted_by=self.left)
        return FilterResult(card=card, accepted_by=self.right)


class InvertOperator(CompositeFilter):
    """A ``not`` operator.

    Reverses the value of the filter.
    """

    leaf: CompositeFilter

    def filter_card(self, card: Card) -> FilterResult:
        res = self.leaf.filter_card(card)
        if res.accepted_by is not None:
            return FilterResult(card=card)
        return FilterResult(card=card, accepted_by=self.leaf)
