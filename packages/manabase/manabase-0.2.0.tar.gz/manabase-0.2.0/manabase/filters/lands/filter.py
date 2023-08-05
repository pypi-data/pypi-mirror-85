"""Filters filter lands."""
from .base import LandFilter

# TODO: Add Shadowmoor/Eventide filter lands.


class FilterLandFilter(LandFilter):
    """Filters filter lands."""

    def __init__(self):
        pattern = r"^\{1\}, %(tap)s: Add %(symbols)s%(symbols)s\.$"
        super().__init__(pattern=pattern)
