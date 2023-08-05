"""Color definitions.

Colors are defined as an enum for convenience.

It can be parsed from a string of color identifiers using the `Color.from_string`
method.

Example::

```python
>>> from manabase.colors import Color
>>> Color.from_string("w")
[<Color.white: 'W'>]

```

This method is case insensitive to work with most APIs by default.

Example::

```python
>>> from manabase.colors import Color
>>> Color.from_string("wUb")
[<Color.white: 'W'>, <Color.blue: 'U'>, <Color.black: 'B'>]

```
"""
from __future__ import annotations

from enum import Enum
from typing import List, Optional, Tuple


class Color(Enum):
    """Definition of all possible colors."""

    white = "W"
    blue = "U"
    black = "B"
    red = "R"
    green = "G"

    @staticmethod
    def all() -> List[Color]:
        """Return all colors, in clockwise order from white to green."""
        return [Color.white, Color.blue, Color.black, Color.red, Color.green]

    @classmethod
    def from_string(cls, colors: str) -> List[Color]:
        """Generate a list of `Color` from a string of color identifiers.

        Color identifiers are single letters corresponding to a color.

        A string of color identifiers is any string containing one or more
        of these letters, in any order, for example ``"wub"``

        Methods manipulating these strings are case insensitive, to work
        with most APIs.

        Colors are identified by the following letters:

            - White: ``w``
            - Blue: ``u``
            - Black: ``b``
            - Red: ``r``
            - Green: ``g``
        """
        return [Color(color.upper()) for color in colors]

    @classmethod
    def to_string(cls, *colors: Color) -> str:
        """Return a string identifier of a list of `Color`s.

        Examples::

        ```python
        >>> from manabase.colors import Color
        >>> Color.to_string(Color.white, Color.blue, Color.black)
        'WUB'

        ```
        """
        return "".join([c.value for c in colors])

    def to_basic_land_name(self) -> Optional[str]:
        """Return the basic land name for this `Color`."""
        if self == Color.white:
            return "Plains"
        if self == Color.blue:
            return "Island"
        if self == Color.black:
            return "Swamp"
        if self == Color.red:
            return "Mountain"
        if self == Color.green:
            return "Forest"
        return None

    @staticmethod
    def dual_combinations(colors: List[Color]) -> List[Tuple[Color, Color]]:
        """Return a list of all possible dual color combinations.

        Example::

        ```python
        >>> from manabase.colors import Color
        >>> Color.dual_combinations([Color.white, Color.blue, Color.black])
        [(<Color.white: 'W'>, <Color.blue: 'U'>), (<Color.white: 'W'>, \
<Color.black: 'B'>), (<Color.blue: 'U'>, <Color.black: 'B'>)]

        ```
        """
        combinations = []
        while colors:
            first = colors.pop(0)
            for other in colors:
                combinations.append((first, other))
        return combinations
