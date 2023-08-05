"""Handles request cards caching."""
from typing import List, Optional

from appdirs import user_cache_dir
from diskcache import Index

from .cards import Card
from .version import __version__


class CacheManager:
    """Manages card cache."""

    def __init__(self, cache_dir: Optional[str] = None) -> None:
        self.cache_dir = cache_dir or CacheManager._default_cache_dir()
        self.index = self._create_index()

    @staticmethod
    def _default_cache_dir() -> str:
        """Return a default cache directory"""

        return user_cache_dir("manabase", version=__version__)

    def _create_index(self) -> Index:
        """Create a disk index."""
        index = Index(self.cache_dir)
        return index

    def has_cache(self) -> bool:
        """Return ``True`` if ``index`` has a card cache."""
        try:
            self.index.peekitem()
        except KeyError:
            return False
        return True

    def write_cache(self, cards: List[Card]):
        """Write cards to the local cache."""
        data = {card.name: card for card in cards}
        self.index.update(data)

    def read_cache(self) -> List[Card]:
        """Read cards from the local cache."""
        return self.index.values()
