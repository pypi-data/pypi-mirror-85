"""Card specific filters."""
# pylint: disable=arguments-differ
from __future__ import annotations

from typing import Union

from ..cards import Card
from ..constructor import represent
from ..filters.composite import CompositeFilter


class CardResult:
    """The result of a card filtering method."""

    def __init__(self, card: Card, source: CompositeFilter):
        self.card = card
        self.source = source

    def __repr__(self) -> str:
        return represent(self)


class CardFilter(CompositeFilter):
    """A filter returning a `CardResult`."""

    def filter_value(self, card: Card) -> Union[CardResult, bool]:
        """Filter a card.

        If the filter does not let the card through, return ``False``.

        If the filter accepts the card, return a `CardResult`, which
        contains the card and an alias of the filter which let the card
        through.

        As filters can be composed, it is easy to lose by which filter a
        card has been accepted.
        """
        res = super().filter_value(card)
        if res:
            return CardResult(card, self)
        return False
