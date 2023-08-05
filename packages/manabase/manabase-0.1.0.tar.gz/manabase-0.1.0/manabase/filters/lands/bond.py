"""Filter bond lands."""
from .base import LandFilter


class BondLandFilter(LandFilter):
    """Filters bond lands."""

    def __init__(self):
        pattern = (
            r"^%(name)s enters the battlefield tapped unless you have "
            r"two or more opponents\.\n"
            r"%(tap)s: Add %(symbols)s or %(symbols)s\.$"
        )
        super().__init__(pattern)
