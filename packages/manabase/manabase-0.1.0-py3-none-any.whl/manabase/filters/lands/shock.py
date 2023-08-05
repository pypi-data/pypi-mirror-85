"""Filter shock lands."""
from .base import LandFilter


class ShockLandFilter(LandFilter):
    """Filters shock lands."""

    def __init__(self):
        pattern = (
            r"^\(%(tap)s: Add %(symbols)s or %(symbols)s\.\)\n"
            r"As %(name)s enters the battlefield, you may pay 2 life\. "
            r"If you don't, it enters the battlefield tapped\.$"
        )
        super().__init__(pattern)
