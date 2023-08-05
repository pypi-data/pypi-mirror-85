"""Cards data structure.

Cards data are fetched from scryfall API, and reduced to a minimal set of data
as the original scryfall response contains a lot of information, such as artist
and artwork related data, price data, etc...
"""
from __future__ import annotations

from functools import total_ordering
from typing import Dict, List

from pydantic import BaseModel  # pylint: disable=no-name-in-module


@total_ordering
class Card(BaseModel):
    """A single card data.

    Only relevant data is shown here, and is parsed from a scryfall API response.
    """

    name: str
    oracle_text: str
    colors: List[str]
    color_identity: List[str]
    produced_mana: List[str]
    legalities: Dict[str, str]
    textless: bool
    scryfall_uri: str

    def __hash__(self) -> int:
        return hash(self.json())

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(name="{self.name}")>'

    def __eq__(self, other: Card) -> bool:
        return self.json() == other.json()

    def __lt__(self, other: Card) -> bool:
        return self.name < other.name
