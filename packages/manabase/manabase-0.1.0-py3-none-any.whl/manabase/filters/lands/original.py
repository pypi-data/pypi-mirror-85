"""Filter original dual lands."""
from .base import LandFilter


class OriginalDualLandFilter(LandFilter):
    """Filters original dual lands."""

    def __init__(self):
        pattern = r"^\(%(tap)s: Add %(symbols)s or %(symbols)s\.\)$"
        super().__init__(pattern)
