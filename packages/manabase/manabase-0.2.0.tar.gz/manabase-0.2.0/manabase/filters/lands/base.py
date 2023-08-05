"""Base filter for lands.

It matches the card oracle text with a regex pattern.
"""
import re

from ...cards import Card
from ..base import FilterResult
from ..composite import CompositeFilter


class LandFilter(CompositeFilter):
    """Filters lands based on the oracle text."""

    pattern: str

    def filter_card(self, card: Card) -> FilterResult:
        # TODO: #4 Filter lands by extension first ?
        regex = re.compile(self._process_pattern(self.pattern))
        res = bool(regex.match(card.oracle_text))
        if not res:
            return FilterResult(card=card)
        return FilterResult(card=card, accepted_by=self)

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
