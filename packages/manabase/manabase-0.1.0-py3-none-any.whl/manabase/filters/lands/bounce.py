"""Filter bounce lands."""
from .base import LandFilter


class BounceLandFilter(LandFilter):
    """Filters bounce lands."""

    def __init__(self):
        pattern = (
            r"^%(name)s enters the battlefield tapped\.\n"
            r"When %(name)s enters the battlefield, return a land "
            r"you control to its owner's hand\.\n"
            r"%(tap)s: Add %(symbols)s%(symbols)s\.$"
        )
        super().__init__(pattern)
