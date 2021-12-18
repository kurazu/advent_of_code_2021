from __future__ import annotations

import abc
import ast
import enum
import logging
from functools import reduce
from typing import (Any, Iterable, List, NamedTuple, Optional, TextIO, Tuple,
                    cast)

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
    def __str__(self) -> str:
        ...


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

    def __str__(self) -> str:
        return f"[{self.left},{self.right}]"


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

    def __str__(self) -> str:
        return f"{self.value}"


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


# def find_leftmost_nested_pair(
#     number: SnailfishNumber,
# ) -> Optional[TreePath]:
#     for path in visit_pairs(number):
#         if len(path.parents) == 4:
#             return path
#     return None


# def find_leftmost_big_number(
#     number: SnailfishNumber,
# ) -> Optional[Tuple[TreePath, Side]]:
#     for path in visit_pairs(number):
#         left, right = path.node
#         if isinstance(left, int) and left >= 10:
#             return path, Side.LEFT
#         if isinstance(right, int) and right >= 10:
#             return path, Side.RIGHT
#     return None


# def explode_number(path: TreePath) -> SnailfishNumber:
#     breakpoint()


# def split_number(path: TreePath, side: Side) -> SnailfishNumber:
#     breakpoint()


def reduce_snailfish_number(number: SnailfishNumber) -> SnailfishNumber:
    while True:
        path = find_leftmost_nested_pair(number)
        if path is not None:
            number = explode_number(path)
            continue
        path_and_side = find_leftmost_big_number(number)
        if path_and_side is not None:
            path, side = path_and_side
            number = split_number(path, side)
            continue
        # No more action to take
        break
    return number


def add_snailfish_numbers(a: SnailfishNumber, b: SnailfishNumber) -> SnailfishNumber:
    container = ContainerNumber()
    container.set_left(a)
    container.set_right(b)
    return container


def sum_snailfish_numbers(numbers: Iterable[SnailfishNumber]) -> SnailfishNumber:
    return reduce(add_and_reduce_snailfish_numbers, numbers)


def add_and_reduce_snailfish_numbers(
    a: SnailfishNumber, b: SnailfishNumber
) -> SnailfishNumber:
    return reduce_snailfish_number(add_snailfish_numbers(a, b))


def main(input: TextIO) -> str:
    numbers = get_numbers(input)

    final_sum = sum_snailfish_numbers(numbers)
    magnitude = final_sum.get_magnitude()

    return f"{magnitude}"


if __name__ == "__main__":
    run_with_file_argument(main)
