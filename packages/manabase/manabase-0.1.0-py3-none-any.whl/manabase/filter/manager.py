"""Filter management."""
from __future__ import annotations

from typing import List

from ..cards import Card
from ..colors import Color
from ..filters.card import CardResult
from ..filters.colors import BasicLandReferencedFilter, ProducedManaFilter
from ..filters.composite import CompositeFilter
from ..filters.lands.battle import BattleLandFilter
from ..filters.lands.check import CheckLandFilter
from ..filters.lands.fetch import FetchLandFilter
from ..filters.lands.original import OriginalDualLandFilter
from ..filters.lands.reveal import RevealLandFilter
from ..filters.lands.shock import ShockLandFilter
from .data import FILTER_ALIAS_BY_CLASS_NAME, FilterAlias
from .parser import parse_filter_string


class FilteredCard(Card):
    """A card tagged with the filter that let it through."""

    filter: FilterAlias


class FilterManager:
    """Filter lists of cards."""

    def __init__(self, colors: List[Color], filters: CompositeFilter):
        self.colors = colors
        self.filters = filters

    @classmethod
    def default(cls, colors: List[Color]) -> FilterManager:
        """Create a default filter tree."""
        return cls(
            colors,
            (
                ProducedManaFilter(colors)
                & (
                    OriginalDualLandFilter()
                    | ShockLandFilter()
                    | BattleLandFilter()
                    | CheckLandFilter()
                    | RevealLandFilter()
                )
            )
            | (
                BasicLandReferencedFilter(
                    colors,
                    exclusive=False,
                    minimum_count=1,
                )
                & FetchLandFilter()
            ),
        )

    @classmethod
    def from_string(cls, filter_string: str, colors: List[Color]) -> FilterManager:
        """Create a filter tree from a filter string."""
        filters = parse_filter_string(filter_string, colors)
        return cls(colors, filters)

    def filter_cards(self, cards: List[Card]) -> List[FilteredCard]:
        """Filter a list of cards."""
        filtered_cards = []

        for card in cards:

            res = self.filters.filter_value(card)

            if not isinstance(res, CardResult):
                continue

            # TODO: #13 Add thorough testing of filters.
            # Maybe even always return a CardResult from `Filter` downstream ?

            alias = FILTER_ALIAS_BY_CLASS_NAME[res.source.__class__.__name__]
            filtered_cards.append(
                FilteredCard(
                    filter=alias,
                    **card.dict(),
                )
            )

        return filtered_cards
