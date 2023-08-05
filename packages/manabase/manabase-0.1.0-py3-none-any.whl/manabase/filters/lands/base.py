"""Base filter for lands.

It matches the card oracle text with a regex pattern.
"""
import re
from typing import Union

from ...cards import Card
from ..card import CardFilter, CardResult


class LandFilter(CardFilter):
    """Filters lands based on the oracle text."""

    def __init__(self, pattern: str):
        self._regex = re.compile(self._process_pattern(pattern))

    def filter_value(self, card: Card) -> Union[CardResult, bool]:
        # TODO: #4 Filter lands by extension first ?
        res = bool(self._regex.match(card.oracle_text))
        if not res:
            return False
        return CardResult(card, self)

    @staticmethod
    def _process_pattern(pattern: str) -> str:
        """Format the pattern with helpers.

        Patterns support the ``name``, ``symbols``, ``tap``, ``basics``,
        and ``c`` formatting keys.
        """
        context = {
            "name": r"[\w\s']+",
            "symbols": r"\{(W|U|B|R|G)\}",
            "tap": r"\{T\}",
            "basics": r"(Plains|Island|Swamp|Mountain|Forest)",
            "c": r"\{C\}",
        }
        return pattern % context
