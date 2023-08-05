"""Filter our cards based on their color identity."""
import re
from typing import List, Set, Union

from ..cards import Card
from ..colors import Color
from ..filters.composite import CompositeFilter
from .base import FilterResult


class ProducedManaFilter(CompositeFilter):
    """A filter checking for colors in the card produced mana.

    Args:
        colors (List[Color]): A list of `Color`s to match.
        exclusive (bool): If ``True``, exclude all cards containing a color
            outside ``colors``.
        minimum_count (int): Minimum amount of colors matched from ``colors`` in
            the card produced mana.

    Example::

    ```python
    >>> from manabase.filters.colors import ProducedManaFilter
    >>> from manabase.colors import Color
    >>> from manabase.cards import Card
    >>> colors = [Color.white, Color.blue, Color.black]
    >>> filter_ = ProducedManaFilter(colors=colors)
    >>> card = Card(
    ...     name="",
    ...     oracle_text="",
    ...     colors=[],
    ...     color_identity=[],
    ...     produced_mana=["W", "U"],
    ...     legalities={},
    ...     textless=False,
    ...     scryfall_uri="",
    ... )
    >>> filter_.filter_card(card)
    FilterResult(card=Card(...), accepted_by=ProducedManaFilter(...))
    >>> card.produced_mana = ["W", "U", "G"]
    >>> filter_.filter_card(card)
    FilterResult(card=Card(...), accepted_by=None)
    >>> filter_.exclusive = False
    >>> filter_.filter_card(card)
    FilterResult(card=Card(...), accepted_by=ProducedManaFilter(...))
    >>> card.produced_mana = ["W"]
    >>> filter_.filter_card(card)
    FilterResult(card=Card(...), accepted_by=None)
    >>> filter_.minimum_count = 1
    >>> filter_.filter_card(card)
    FilterResult(card=Card(...), accepted_by=ProducedManaFilter(...))

    ```
    """

    colors: Set[Color]
    exclusive: bool = True
    minimum_count: int = 2

    def filter_card(self, card: Card) -> Union[FilterResult, bool]:
        produced_mana = [Color(mana) for mana in card.produced_mana if mana != "C"]
        if self.exclusive and not set(produced_mana).issubset(self.colors):
            return FilterResult(card=card)
        if len(self.colors.intersection(produced_mana)) < self.minimum_count:
            return FilterResult(card=card)
        return FilterResult(card=card, accepted_by=self)


class BasicLandReferencedFilter(CompositeFilter):
    """A filter checking if the card text referenced some basic land names.

    Args:
        colors (List[Color]): A list of `Color`s to match their basic land names.
        exclusive (bool): If ``True``, exclude all cards containing a land name
            outside ``colors``.
        minimum_count (int): Minimum amount of land name matched from ``colors`` in
            the card text.

    Example::

    ```python
    >>> from manabase.filters.colors import BasicLandReferencedFilter
    >>> from manabase.colors import Color
    >>> from manabase.cards import Card
    >>> colors = [Color.white, Color.blue, Color.black]
    >>> filter_ = BasicLandReferencedFilter(colors=colors)
    >>> card = Card(
    ...     name="",
    ...     oracle_text="a Plains or Island",
    ...     colors=[],
    ...     color_identity=[],
    ...     produced_mana=[],
    ...     legalities={},
    ...     textless=False,
    ...     scryfall_uri="",
    ... )
    >>> filter_.filter_card(card)
    FilterResult(card=Card(...), accepted_by=BasicLandReferencedFilter(...))
    >>> card.oracle_text = "a Plains, Island or Forest"
    >>> filter_.filter_card(card)
    FilterResult(card=Card(...), accepted_by=None)
    >>> filter_.exclusive = False
    >>> filter_.filter_card(card)
    FilterResult(card=Card(...), accepted_by=BasicLandReferencedFilter(...))
    >>> card.oracle_text = "a Plains"
    >>> filter_.filter_card(card)
    FilterResult(card=Card(...), accepted_by=None)
    >>> filter_.minimum_count = 1
    >>> filter_.filter_card(card)
    FilterResult(card=Card(...), accepted_by=BasicLandReferencedFilter(...))

    ```
    """

    colors: Set[Color]
    exclusive: bool = True
    minimum_count: int = 2
    names: Set[str]

    def __init__(self, **kwargs):
        if "names" not in kwargs:
            colors = kwargs.get("colors") or []
            kwargs["names"] = set(color.to_basic_land_name() for color in colors)
        super().__init__(**kwargs)

    def filter_card(self, card: Card) -> Union[FilterResult, bool]:
        names = set(self._extract_basic_land_names(card))
        if self.exclusive and not names.issubset(self.names):
            return FilterResult(card=card)
        if len(self.names.intersection(names)) < self.minimum_count:
            return FilterResult(card=card)
        return FilterResult(card=card, accepted_by=self)

    @staticmethod
    def _extract_basic_land_names(card: Card) -> List[str]:
        """Extract basic land names from a card text.

        Example::

        ```python
        >>> from manabase.filters.colors import BasicLandReferencedFilter
        >>> card = Card(
        ...     name="",
        ...     oracle_text="a Plains or Island",
        ...     colors=[],
        ...     color_identity=[],
        ...     produced_mana=[],
        ...     legalities={},
        ...     textless=False,
        ...     scryfall_uri="",
        ... )
        >>> BasicLandReferencedFilter._extract_basic_land_names(card)
        ['Plains', 'Island']
        >>> card.oracle_text = "a Plains, Island, Swamp, Mountain of Forest"
        >>> BasicLandReferencedFilter._extract_basic_land_names(card)
        ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']

        ```
        """
        regex = re.compile("(Plains|Island|Swamp|Mountain|Forest)")
        names = filter(None, regex.findall(card.oracle_text))
        return list(names)
