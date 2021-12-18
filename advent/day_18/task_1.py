from __future__ import annotations

import ast
import logging
from functools import reduce
from typing import Any, Iterable, List, Optional, TextIO, Tuple, cast

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)


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


def visit_pairs(
    number: SnailFishNumber,
) -> Iterable[List[SnailFishNumber]]:
    def _visit_pairs(
        number: SnailFishNumber, path: List[SnailFishNumber]
    ) -> Iterable[List[SnailFishNumber]]:
        current_path = path + [number]
        yield current_path
        left, right = number
        if isinstance(left, tuple):
            yield from _visit_pairs(cast(SnailFishNumber, left), current_path)
        if isinstance(right, tuple):
            yield from _visit_pairs(cast(SnailFishNumber, right), current_path)

    yield from _visit_pairs(number, [])


def find_leftmost_nested_pair(
    number: SnailFishNumber,
) -> Optional[List[SnailFishNumber]]:
    for path in visit_pairs(number):
        if len(path) == 5:
            return path
    return None


def find_leftmost_big_number(
    number: SnailFishNumber,
) -> Optional[List[SnailFishNumber]]:
    for path in visit_pairs(number):
        *parents, pair = path
        left, right = pair
        if isinstance(left, int) and left >= 10:
            return path
        if isinstance(right, int) and right >= 10:
            return path
    return None


def explode_number(path: List[SnailFishNumber]) -> SnailFishNumber:
    *parents, pair = path
    left, right = pair


def split_number(path: List[SnailFishNumber]) -> SnailFishNumber:
    breakpoint()


def reduce_snailfish_number(number: SnailFishNumber) -> SnailFishNumber:
    while True:
        path = find_leftmost_nested_pair(number)
        if path is not None:
            number = explode_number(path)
            continue
        path = find_leftmost_big_number(number)
        if path is not None:
            number = split_number(path)
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
