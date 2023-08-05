"""Filter cycling lands."""
from .base import LandFilter


class CyclingLandFilter(LandFilter):
    """Filters cycling lands."""

    def __init__(self):
        pattern = (
            r"^\(%(tap)s: Add %(symbols)s or %(symbols)s\.\)\n"
            r"%(name)s enters the battlefield tapped\.\n"
            r"Cycling \{2\} \(\{2\}, Discard this card: Draw a card\.\)$"
        )
        super().__init__(pattern)
