"""Filter pain lands."""
from .base import LandFilter


class PainLandFilter(LandFilter):
    """Filters pain lands."""

    def __init__(self) -> None:
        pattern = (
            r"^%(tap)s: Add %(c)s.\n"
            r"%(tap)s: Add %(symbols)s or "
            r"%(symbols)s. %(name)s deals 1 damage to you.$"
        )
        super().__init__(pattern)
