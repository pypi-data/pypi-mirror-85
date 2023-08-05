"""Manage a list of priorities.

When the targetted number if lands is reached, priorities can be set to
decide whichever land is returned first, and whichever is discarded.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .cards import Card
from .filter.data import FilterAlias
from .filter.manager import FilteredCard


class PriorityManager(BaseModel):
    """Build prioritized lists of cards."""

    lands: int = 23
    occurrences: int = 1
    priorities: List[FilterAlias]

    @classmethod
    def default(cls, lands: int = 23, occurrences: int = 4) -> PriorityManager:
        """Build a default priority manager."""
        priorities = [
            FilterAlias.fetch,
            FilterAlias.original,
            FilterAlias.shock,
            FilterAlias.battle,
            FilterAlias.check,
            FilterAlias.reveal,
        ]
        return cls(lands=lands, occurrences=occurrences, priorities=priorities)

    @classmethod
    def from_string(
        cls,
        priorities: str,
        lands: int = 23,
        occurrences: int = 4,
    ) -> PriorityManager:
        """Build a priority manager from a string of space separated aliases.

        Example::
        ```python
        >>> from manabase.priorities import PriorityManager
        >>> string = "original fetch"
        >>> PriorityManager.from_string(string)
        PriorityManager(lands=23, occurrences=4, priorities=[<FilterAlias.original: \
'original'>, <FilterAlias.fetch: 'fetch'>])

        ```
        """
        priorities_list = [FilterAlias(alias) for alias in priorities.split()]
        return cls(lands=lands, occurrences=occurrences, priorities=priorities_list)

    def truncate_cards(self, cards: List[FilteredCard]) -> List[Card]:
        """Build a new list of cards by truncating the specified one."""
        truncated_cards = []

        if self.priorities:
            cards.sort(key=self._card_key, reverse=True)

        remaining_slots = self.lands

        for card in cards:
            for _ in range(self.occurrences):

                truncated_cards.append(Card(**card.dict()))

                remaining_slots -= 1
                if remaining_slots == 0:
                    return truncated_cards

        return truncated_cards

    def _card_key(self, card: FilteredCard) -> int:
        try:
            return len(self.priorities) - self.priorities.index(card.filter)
        except ValueError:
            return -1
