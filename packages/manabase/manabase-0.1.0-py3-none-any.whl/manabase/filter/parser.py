"""Parses a string representing filters.

Filter strings have their own very light syntax.

Instead of class names, every filter has an alias defined by
the `FILTER_CLASS_BY_ALIAS` constant.

Example::
```python
>>> from manabase.filter.parser import parse_filter_string
>>> filter_string = "original"
>>> parse_filter_string(filter_string, [])
<OriginalDualLandFilter()>

```

You can use binary operators and parenthesis to join and group them.

Example::
```python
>>> from manabase.filter.parser import parse_filter_string
>>> filter_string = "producer & original"
>>> parse_filter_string(filter_string, [])
<AndOperator(left=<ProducedManaFilter(colors=set(), exclusive=True, minimum_count=2)>\
, right=<OriginalDualLandFilter()>)>

```

If the filter constructor has parameters, you can initialize it by including
all arguments, wrapping them in curly braces instead of parenthesis.

Curly braces are used in order to stand out from grouping parenthesis.

Arguments must be integers, for boolean values you must use ``1`` for ``True``
and ``0`` for ``False``.

Example::
```python
>>> from manabase.filter.parser import parse_filter_string
>>> filter_string = "reference { 0, 1 } & fetch"
>>> parse_filter_string(filter_string, [])
<AndOperator(left=<BasicLandReferencedFilter(colors=set(), exclusive=False, \
minimum_count=1)>, right=<FetchLandFilter()>)>

The grammar used to parse the filter string does not support chaining multiple
operators, so if you use the invert unary operator (``~``), you must group it
to avoid errors if you join it to other operators.

Example::
```python
>>> from manabase.filter.parser import parse_filter_string
>>> filter_string = "producer & (~original)"
>>> parse_filter_string(filter_string, [])
<AndOperator(left=<ProducedManaFilter(colors=set(), exclusive=True, \
minimum_count=2)>, right=<InvertOperator(leaf=<OriginalDualLandFilter()>)>)>
"""
# pylint: disable=no-self-use
import inspect
from inspect import Parameter
from typing import List

from parsimonious import Grammar
from parsimonious.nodes import Node, NodeVisitor

from ..colors import Color
from ..filters.composite import CompositeFilter
from .data import FILTER_CLASS_BY_ALIAS, FilterAlias, FilterOperator

GRAMMAR = Grammar(
    r"""
    filters = (joined_filters / filter_group / filter)

    filter = alias (ws? arguments)?
    alias = ~"[a-z]+"i
    arguments = arguments_open ws values ws arguments_close
    arguments_open = "{"
    arguments_close = "}"
    values = (value / ~"\s*,\s*")*
    value = ~"[0-9]"

    filter_group = group_open ws joined_filters ws group_close
    group_open = "("
    group_close = ")"

    joined_filters = filter_arm? operator_left_arm+

    operator_left_arm = ws operator ws filter_arm

    ws = ~"\s*"

    filter_arm = (filter_group / filter)
    operator = (and / or / xor / invert)
    and = "&"
    or = "|"
    xor = "^"
    invert = "~"
    """
)


COLOR_DEPENDANT_PARAMETER_NAME = "colors"


class FilterStringVisitor(NodeVisitor):
    """Visit a filter string."""

    def __init__(self, colors: List[Color]):
        super().__init__()
        self.colors = colors

    def visit_filters(self, _, visited_children):
        """Return the root filter."""
        return visited_children[0]

    def visit_values(self, _, visited_children):
        """Return argument values of a filter constructor."""
        return [value for value in visited_children if not isinstance(value, Node)]

    def visit_value(self, node, _):
        """Return a single filter constructor argument value."""
        return int(node.text)

    def visit_filter(self, _, visited_children):
        """Build a filter from the alias and optionally arguments."""
        alias, optional_arguments = visited_children

        values = []
        if isinstance(optional_arguments, list):
            # ``optional_arguments`` are [<ws>, <arguments>]
            # Then, ``arguments`` are [<arguments_open>, <ws>, <values>, ...]
            values = optional_arguments[1][2]

        filter_class = FILTER_CLASS_BY_ALIAS[FilterAlias(alias.text)]

        constructor = inspect.signature(filter_class)

        args = []
        for parameter in constructor.parameters.values():

            if parameter.name == COLOR_DEPENDANT_PARAMETER_NAME:
                args.append(self.colors)
                continue

            if not values:
                break

            value = values.pop(0)

            if parameter.default != Parameter.empty:
                value_class = parameter.default.__class__
                value = value_class(value)

            args.append(value)

        parameters = constructor.bind_partial(*args)

        return filter_class(*parameters.args, **parameters.kwargs)

    def visit_filter_group(self, _, visited_children):
        """Return the root filter of the group, ignoring whitespace and parenthesis."""
        return visited_children[2]

    def visit_joined_filters(self, _, visited_children):
        """Join filters using operands.

        Multiple filters could be joined together, so the ``operator_left_arm``
        rule can match multiple tuples of (<operator>, <filter>)

        The left arm is optional in the case of invert operators, in which case
        the filter string would look like ``"~original"``.
        This is the only case where the left arm is omitted.
        """
        left, operator_left_arm = visited_children

        # We can have one of two cases:
        # Either we just have two filters joined, i.e ``producer & original``,
        # in this case ``operator_left_arm`` is [<operator>, <filter>],
        # or we have multiple, chained operations, i.e ``original | fast | reveal``,
        # and then the list we have is of the following shape:
        # [(<operator>, <filter>), (<operator>, <filter>), ...]
        # An edge case here is a list of two operations that we might process
        # as a normal [<operator>, <filter>] list, so just mind that.
        operations = operator_left_arm
        if len(operator_left_arm) == 2:
            if not isinstance(operator_left_arm[0], tuple):
                operations = [operator_left_arm]

        filter_ = None

        while operations:

            (operator, right) = operations.pop(0)

            if filter_ is None:
                filter_ = left if isinstance(left, CompositeFilter) else right

            filter_operator = FilterOperator(operator.text)
            if filter_operator == FilterOperator.and_:
                filter_ &= right
            if filter_operator == FilterOperator.or_:
                filter_ |= right
            if filter_operator == FilterOperator.xor:
                filter_ ^= right
            if filter_operator == FilterOperator.invert:
                filter_ = ~filter_  # pylint: disable=invalid-unary-operand-type

        return filter_

    def visit_operator_left_arm(self, _, visited_children):
        """Destructure the ``operator_left_arm`` rule."""
        _, operator, _, filter_ = visited_children
        return operator, filter_

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        if not visited_children:
            return node
        if len(visited_children) == 1:
            return visited_children[0]
        return visited_children


def parse_filter_string(string: str, colors: List[Color]) -> CompositeFilter:
    """Parse a filter string and return a filter tree."""
    tree = GRAMMAR.parse(string)
    visitor = FilterStringVisitor(colors)
    filter_ = visitor.visit(tree)
    return filter_
