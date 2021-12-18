from __future__ import annotations

import abc
import ast
import logging
import math
from functools import reduce
from typing import Any, Iterable, Optional, TextIO

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)


class SnailfishNumber(metaclass=abc.ABCMeta):
    parent: Optional[SnailfishNumber] = None

    @property
    @abc.abstractmethod
    def is_container(self) -> bool:
        ...

    def set_parent(self, parent: SnailfishNumber) -> None:
        assert self.parent is None
        self.parent = parent

    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:
        ...

    @abc.abstractmethod
    def get_magnitude(self) -> int:
        ...

    @abc.abstractmethod
    def __repr__(self) -> str:
        ...

    @abc.abstractmethod
    def visit(self) -> Iterable[SnailfishNumber]:
        ...

    def get_parents(self) -> Iterable[SnailfishNumber]:
        if self.parent is None:
            return
        yield self.parent
        yield from self.parent.get_parents()


class ContainerNumber(SnailfishNumber):
    is_container = True
    left: SnailfishNumber
    right: SnailfishNumber

    def set_left(self, left: SnailfishNumber) -> None:
        self.left = left
        left.set_parent(self)

    def set_right(self, right: SnailfishNumber) -> None:
        self.right = right
        right.set_parent(self)

    def replace_child(
        self, child: SnailfishNumber, replacement: SnailfishNumber
    ) -> None:
        if child is self.left:
            self.set_left(replacement)
        else:
            assert child is self.right
            self.set_right(replacement)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ContainerNumber):
            return False
        left_equals = self.left == other.left
        right_equals = self.right == other.right
        return left_equals and right_equals

    def get_magnitude(self) -> int:
        return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()

    def __repr__(self) -> str:
        return f"[{self.left!r},{self.right!r}]"

    def visit(self) -> Iterable[SnailfishNumber]:
        yield self
        yield from self.left.visit()
        yield from self.right.visit()


class LiteralNumber(SnailfishNumber):
    is_container = False
    value: int

    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LiteralNumber):
            return False
        return self.value == other.value

    def get_magnitude(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"{self.value}"

    def visit(self) -> Iterable[SnailfishNumber]:
        yield self

    def __iadd__(self, other: int) -> LiteralNumber:
        self.value += other
        return self


def parse_number(value: Any) -> SnailfishNumber:
    if isinstance(value, int):
        return LiteralNumber(value=value)
    elif isinstance(value, tuple):
        left_value, right_value = value
        left_number = parse_number(left_value)
        right_number = parse_number(right_value)
        container = ContainerNumber()
        container.set_left(left_number)
        container.set_right(right_number)
        return container
    else:
        raise AssertionError("Unknown node type")


def get_number(number: str) -> ContainerNumber:
    number_with_tuple_syntax = number.replace("[", "(").replace("]", ")")
    parsed_number = ast.literal_eval(number_with_tuple_syntax)
    assert isinstance(parsed_number, tuple)
    assert len(parsed_number) == 2
    left_value, right_value = parsed_number
    root = ContainerNumber()
    root.set_left(parse_number(left_value))
    root.set_right(parse_number(right_value))
    return root


def get_numbers(input: TextIO) -> Iterable[ContainerNumber]:
    return map(get_number, get_lines(input))


# def visit_pairs(
#     number: SnailfishNumber,
# ) -> Iterable[TreePath]:
#     def _visit_pairs(
#         number: SnailfishNumber, parents: List[Parent]
#     ) -> Iterable[TreePath]:
#         yield TreePath(parents=parents, node=number)
#         left, right = number
#         if isinstance(left, tuple):
#             yield from _visit_pairs(
#                 cast(SnailfishNumber, left),
#                 parents + [Parent(node=number, side=Side.LEFT)],
#             )
#         if isinstance(right, tuple):
#             yield from _visit_pairs(
#                 cast(SnailfishNumber, right),
#                 parents + [Parent(node=number, side=Side.RIGHT)],
#             )

#     yield from _visit_pairs(number, [])


def find_leftmost_nested_pair(
    number: SnailfishNumber,
) -> Optional[ContainerNumber]:
    for node in number.visit():
        if (
            isinstance(node, ContainerNumber)
            and sum(1 for parent in node.get_parents()) == 4
        ):
            return node
    return None


def find_leftmost_big_number(
    number: SnailfishNumber,
) -> Optional[LiteralNumber]:
    for node in number.visit():
        if isinstance(node, LiteralNumber) and node.value >= 10:
            return node
    return None


def find_closest_literal_on_the_left(
    root: ContainerNumber, child: SnailfishNumber
) -> Optional[LiteralNumber]:
    last_literal_seen: Optional[LiteralNumber] = None
    for node in root.visit():
        if node is child:
            break
        elif isinstance(node, LiteralNumber):
            last_literal_seen = node
    else:
        raise AssertionError()
    return last_literal_seen


def find_closest_literal_on_the_right(
    root: ContainerNumber, child: SnailfishNumber
) -> Optional[LiteralNumber]:
    nodes = root.visit()
    for node in nodes:
        if node is child:
            break
    else:
        raise AssertionError()

    for node in nodes:
        if isinstance(node, LiteralNumber):
            return node
    else:
        return None


def explode_number(
    root: ContainerNumber, node_to_explode: ContainerNumber
) -> ContainerNumber:
    left = node_to_explode.left
    assert isinstance(left, LiteralNumber)
    closest_left_literal = find_closest_literal_on_the_left(root, left)
    if closest_left_literal is not None:
        closest_left_literal += left.value

    right = node_to_explode.right
    assert isinstance(right, LiteralNumber)
    closest_right_literal = find_closest_literal_on_the_right(root, right)
    if closest_right_literal is not None:
        closest_right_literal += right.value

    parent = node_to_explode.parent
    assert parent is not None
    assert isinstance(parent, ContainerNumber)
    parent.replace_child(node_to_explode, LiteralNumber(0))

    return root


def split_node(value: int) -> ContainerNumber:
    half = value / 2
    left_value = math.floor(half)
    right_value = math.ceil(half)
    container = ContainerNumber()
    container.set_left(LiteralNumber(left_value))
    container.set_right(LiteralNumber(right_value))
    return container


def split_number(
    root: ContainerNumber, node_to_split: LiteralNumber
) -> ContainerNumber:
    replacement = split_node(node_to_split.value)

    parent = node_to_split.parent
    assert parent is not None
    assert isinstance(parent, ContainerNumber)
    parent.replace_child(node_to_split, replacement)

    return root


def reduce_snailfish_number(number: ContainerNumber) -> ContainerNumber:
    logger.info("Reducing number %r", number)
    while True:
        container_node = find_leftmost_nested_pair(number)
        if container_node is not None:
            number = explode_number(number, container_node)
            logger.info("After exploding %r", number)
            continue
        literal_node = find_leftmost_big_number(number)
        if literal_node is not None:
            number = split_number(number, literal_node)
            logger.info("After splitting %r", number)
            continue
        # No more action to take
        break
    logger.info("Reduced to %r", number)
    return number


def add_snailfish_numbers(
    left: ContainerNumber, right: ContainerNumber
) -> ContainerNumber:
    container = ContainerNumber()
    container.set_left(left)
    container.set_right(right)
    return container


def sum_snailfish_numbers(numbers: Iterable[ContainerNumber]) -> ContainerNumber:
    return reduce(add_and_reduce_snailfish_numbers, numbers)


def add_and_reduce_snailfish_numbers(
    a: ContainerNumber, b: ContainerNumber
) -> ContainerNumber:
    return reduce_snailfish_number(add_snailfish_numbers(a, b))


def main(input: TextIO) -> str:
    numbers = get_numbers(input)

    final_sum = sum_snailfish_numbers(numbers)
    magnitude = final_sum.get_magnitude()

    return f"{magnitude}"


if __name__ == "__main__":
    run_with_file_argument(main)
