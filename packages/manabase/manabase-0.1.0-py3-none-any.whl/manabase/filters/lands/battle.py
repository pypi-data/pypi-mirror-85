"""Filter battle lands."""
from .base import LandFilter


class BattleLandFilter(LandFilter):
    """Filters battle lands."""

    def __init__(self):
        pattern = (
            r"^\(%(tap)s: Add %(symbols)s or %(symbols)s\.\)\n"
            r"%(name)s enters the battlefield tapped unless you control "
            r"two or more basic lands.$"
        )
        super().__init__(pattern)
