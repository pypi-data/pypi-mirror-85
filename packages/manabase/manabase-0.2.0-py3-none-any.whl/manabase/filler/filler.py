"""Card list filler.

If you consume all filters and still does not reach the desired number of
lands, a filler can be used to add missing cards.
"""
from abc import ABCMeta, abstractmethod
from typing import List

from pydantic import BaseModel

from ..cards import Card, CardList
from ..colors import Color
from .distribution import Distribution


class ListFiller(BaseModel, metaclass=ABCMeta):
    """Fills a card list until its maximum size is reached."""

    distribution: Distribution

    @abstractmethod
    def generate_filler(self, slots: int) -> CardList:
        """Generate a filler card list to merge."""


class BasicLandFiller(ListFiller):
    """Fills the list with basic lands of the chosen colors."""

    colors: List[Color]

    def generate_filler(self, slots: int) -> CardList:
        cards = [Card.named(color.to_basic_land_name()) for color in self.colors]
        card_list = self.distribution.compute(cards)
        return card_list
