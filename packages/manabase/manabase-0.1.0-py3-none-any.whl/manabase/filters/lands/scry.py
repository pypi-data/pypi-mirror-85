"""Filter scry lands."""
from .base import LandFilter


class ScryLandFilter(LandFilter):
    """Filters scry lands."""

    def __init__(self):
        pattern = (
            r"^%(name)s enters the battlefield tapped\.\n"
            r"When %(name)s enters the battlefield, scry 1\. "
            r"\(Look at the top card of your library. You may put that card "
            r"on the bottom of your library.\)\n"
            r"%(tap)s: Add %(symbols)s or %(symbols)s\.$"
        )
        super().__init__(pattern)
