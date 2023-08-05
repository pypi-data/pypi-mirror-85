"""Filter fetch lands."""
from .base import LandFilter


class FetchLandFilter(LandFilter):
    """Filters fetch lands."""

    def __init__(self):
        pattern = (
            r"^%(tap)s, Pay 1 life, Sacrifice %(name)s: "
            r"Search your library for (a|an) "
            r"%(basics)s or %(basics)s card, "
            r"put it onto the battlefield, then shuffle your library\.$"
        )
        super().__init__(pattern)
