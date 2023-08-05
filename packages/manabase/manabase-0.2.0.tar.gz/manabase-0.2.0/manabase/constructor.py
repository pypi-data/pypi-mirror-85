"""Utility functions based on objects constructors."""
from inspect import Parameter, signature
from typing import TypeVar

ObjectType = TypeVar("ObjectType")


def represent(instance: ObjectType) -> str:
    """Return a representation based on constructor parameters.

    Example::

    ```python
    >>> from manabase.constructor import represent
    >>> class MyClass:
    ...     def __init__(self, value):
    ...         self.value = value
    >>> represent(MyClass(5))
    '<MyClass(value=5)>'

    ```
    """
    constructor = signature(instance.__class__.__init__)
    parameters = []

    for name, parameter in constructor.parameters.items():

        if name == "self":
            continue

        value = getattr(instance, name, None)
        parameters.append(parameter.replace(default=value, annotation=Parameter.empty))

    constructor = constructor.replace(parameters=parameters)

    return f"<{instance.__class__.__name__}{constructor}>"


def equals(instance: ObjectType, other: ObjectType) -> bool:
    """Compare two objects base on their constructor signature parameters.

    Example::

    ```python
    >>> from manabase.constructor import equals
    >>> class MyClass:
    ...     def __init__(self, value):
    ...         self.value = value
    >>> equals(MyClass(5), MyClass(5))
    True
    >>> equals(MyClass(5), MyClass(7))
    False

    ```
    """
    constructor = signature(instance.__class__.__init__)

    for name in constructor.parameters:

        if name == "self":
            continue

        left = getattr(instance, name, None)
        right = getattr(other, name, None)

        if left != right:
            return False

    return True
