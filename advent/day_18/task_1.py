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


# class SnailfishNumber(metaclass=abc.ABCMeta):
#     parent: Optional[SnailfishNumber] = None

#     @property
#     @abc.abstractmethod
#     def is_container(self) -> bool:
#         ...

#     def set_parent(self, parent: SnailfishNumber) -> None:
#         assert self.parent is None
#         self.parent = parent


class Side(str, enum.Enum):
    LEFT = "left"
    RIGHT = "right"


# class ContainerNumber(SnailfishNumber):
#     is_container = True
#     left: SnailfishNumber
#     right: SnailfishNumber

#     def __init__(self) -> None:
#         pass

#     def set_left(self, left: SnailfishNumber) -> None:
#         self.left = left
#         left.set_parent(self)

#     def set_right(self, right: SnailfishNumber) -> None:
#         self.right = right
#         right.set_parent(self)


# class LiteralNumber(SnailfishNumber):
#     is_container = False
#     value: int

#     def __init__(self, value: int) -> None:
#         super().__init__()
#         self.value = value


SnailFishNumber = Tuple[Any, Any]


def get_number(number: str) -> SnailFishNumber:
    number_with_tuple_syntax = number.replace("[", "(").replace("]", ")")
    parsed_number = ast.literal_eval(number_with_tuple_syntax)
    assert isinstance(parsed_number, tuple)
    assert len(parsed_number) == 2
    return cast(SnailFishNumber, parsed_number)


def get_numbers(input: TextIO) -> Iterable[SnailFishNumber]:
    return map(get_number, get_lines(input))


def get_magnitude(number: SnailFishNumber) -> int:
    left, right = number
    left_value = left if isinstance(left, int) else get_magnitude(left)
    right_value = right if isinstance(right, int) else get_magnitude(right)
    return 3 * left_value + 2 * right_value


class Parent(NamedTuple):
    node: SnailFishNumber
    side: Side


class TreePath(NamedTuple):
    parents: List[Parent]
    node: SnailFishNumber


def visit_pairs(
    number: SnailFishNumber,
) -> Iterable[TreePath]:
    def _visit_pairs(
        number: SnailFishNumber, parents: List[Parent]
    ) -> Iterable[TreePath]:
        yield TreePath(parents=parents, node=number)
        left, right = number
        if isinstance(left, tuple):
            yield from _visit_pairs(
                cast(SnailFishNumber, left),
                parents + [Parent(node=number, side=Side.LEFT)],
            )
        if isinstance(right, tuple):
            yield from _visit_pairs(
                cast(SnailFishNumber, right),
                parents + [Parent(node=number, side=Side.RIGHT)],
            )

    yield from _visit_pairs(number, [])


def find_leftmost_nested_pair(
    number: SnailFishNumber,
) -> Optional[TreePath]:
    for path in visit_pairs(number):
        if len(path.parents) == 4:
            return path
    return None


def find_leftmost_big_number(
    number: SnailFishNumber,
) -> Optional[Tuple[TreePath, Side]]:
    for path in visit_pairs(number):
        left, right = path.node
        if isinstance(left, int) and left >= 10:
            return path, Side.LEFT
        if isinstance(right, int) and right >= 10:
            return path, Side.RIGHT
    return None


def explode_number(path: TreePath) -> SnailFishNumber:
    breakpoint()


def split_number(path: TreePath, side: Side) -> SnailFishNumber:
    breakpoint()


def reduce_snailfish_number(number: SnailFishNumber) -> SnailFishNumber:
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


def add_snailfish_numbers(a: SnailFishNumber, b: SnailFishNumber) -> SnailFishNumber:
    return (a, b)


def sum_snailfish_numbers(numbers: Iterable[SnailFishNumber]) -> SnailFishNumber:
    return reduce(add_and_reduce_snailfish_numbers, numbers)


def add_and_reduce_snailfish_numbers(
    a: SnailFishNumber, b: SnailFishNumber
) -> SnailFishNumber:
    return reduce_snailfish_number(add_snailfish_numbers(a, b))


def main(input: TextIO) -> str:
    numbers = get_numbers(input)

    final_sum = sum_snailfish_numbers(numbers)
    magnitude = get_magnitude(final_sum)

    return f"{magnitude}"


if __name__ == "__main__":
    run_with_file_argument(main)
