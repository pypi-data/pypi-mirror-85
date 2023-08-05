"""Filter reveal lands."""
from .base import LandFilter


class RevealLandFilter(LandFilter):
    """Filters reveal lands."""

    def __init__(self):
        pattern = (
            r"^As %(name)s enters the battlefield, you may reveal (a|an) "
            r"%(basics)s or %(basics)s card from your hand\. "
            r"If you don't, %(name)s enters the battlefield tapped\.\n"
            r"%(tap)s: Add %(symbols)s or %(symbols)s\.$"
        )
        super().__init__(pattern)
