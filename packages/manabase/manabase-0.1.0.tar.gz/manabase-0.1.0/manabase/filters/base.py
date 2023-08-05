"""A simple filter interface."""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any

from ..constructor import equals, represent


class Filter(metaclass=ABCMeta):
    """Filter than can be chained using bitwise operators.

    Example::
    ```python
    >>> from manabase.filters.composite import Filter
    >>> class MoreThanTwo(Filter):
    ...     def filter_value(self, value: int) -> bool:
    ...         return value > 2
    >>> class LessThanTen(Filter):
    ...     def filter_value(self, value: int) -> bool:
    ...         return value < 10
    >>> class AndOperator(Filter):
    ...     def __init__(self, left: Filter, right: Filter):
    ...         self.left = left
    ...         self.right = right
    ...     def filter_value(self, value: Any) -> bool:
    ...         left = self.left.filter_value(value)
    ...         if not left:
    ...             return False
    ...         right = self.right.filter_value(value)
    ...         return right
    >>> operator = AndOperator(MoreThanTwo(), LessThanTen())
    >>> operator.filter_value(1)
    False
    >>> operator.filter_value(5)
    True
    >>> operator.filter_value(12)
    False

    ```
    """

    @abstractmethod
    def filter_value(self, value: Any) -> bool:
        """Filter a single value.

        Example::

        ```python
        >>> from manabase.filters.composite import Filter
        >>> class MoreThanTwo(Filter):
        ...     def filter_value(self, value: int) -> bool:
        ...         return value > 2
        >>> filter_ = MoreThanTwo()
        >>> filter_.filter_value(2)
        False
        >>> filter_.filter_value(10)
        True

        ```
        """

    def __repr__(self) -> str:
        return represent(self)

    def __eq__(self, other: Filter) -> bool:
        return equals(self, other)
