"""Filter fast lands."""
from .base import LandFilter


class FastLandFilter(LandFilter):
    """Filters fast lands."""

    def __init__(self):
        pattern = (
            r"^%(name)s enters the battlefield tapped unless you control "
            r"two or fewer other lands\.\n"
            r"%(tap)s: Add %(symbols)s or %(symbols)s\.$"
        )
        super().__init__(pattern)
