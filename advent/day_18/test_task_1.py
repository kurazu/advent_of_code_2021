from typing import Iterable, List, Tuple

import pytest
from advent.day_18.task_1 import (add_and_reduce_snailfish_numbers,
                                  add_snailfish_numbers, get_magnitude,
                                  get_number, reduce_snailfish_number,
                                  sum_snailfish_numbers)

GET_MAGNITUDE_SAMPLES: List[Tuple[str, int]] = [
    ("[9,1]", 29),
    ("[1,9]", 21),
    ("[[9,1],[1,9]]", 129),
    ("[[1,2],[[3,4],5]]", 143),
    ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
    ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
    ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
    ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
    ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
]


@pytest.mark.parametrize("number,expected_magnitude", GET_MAGNITUDE_SAMPLES)
def test_get_magnitude(number: str, expected_magnitude: int) -> None:
    snailfish_number = get_number(number)
    magnitude = get_magnitude(snailfish_number)
    assert magnitude == expected_magnitude


ADD_SAMPLES: List[Tuple[str, str, str]] = [
    ("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]", "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"),
]


@pytest.mark.parametrize("left,right,expected", ADD_SAMPLES)
def test_add_snailfish_numbers(left: str, right: str, expected: str) -> None:
    parsed_left = get_number(left)
    parsed_right = get_number(right)
    parsed_expected = get_number(expected)
    assert add_snailfish_numbers(parsed_left, parsed_right) == parsed_expected


REDUCE_SAMPLES: List[Tuple[str, str]] = [
    ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
]


@pytest.mark.parametrize("number,expected", REDUCE_SAMPLES)
def test_reduce_snailfish_number(number: str, expected: str) -> None:
    parsed_number = get_number(number)
    parsed_expected = get_number(expected)
    assert reduce_snailfish_number(parsed_number) == parsed_expected


ADD_AND_REDUCE_SAMPLES: List[Tuple[str, str, str]] = [
    (
        "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
        "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
        "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
    ),
    (
        "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
        "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
        "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
    ),
    (
        "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
        "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
        "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]",
    ),
    (
        "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]",
        "[7,[5,[[3,8],[1,4]]]]",
        "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]",
    ),
    (
        "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]",
        "[[2,[2,2]],[8,[8,1]]]",
        "[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]",
    ),
    (
        "[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]",
        "[2,9]",
        "[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]",
    ),
    (
        "[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]",
        "[1,[[[9,3],9],[[9,0],[0,7]]]]",
        "[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]",
    ),
    (
        "[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]",
        "[[[5,[7,4]],7],1]",
        "[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]",
    ),
    (
        "[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]",
        "[[[[4,2],2],6],[8,7]]",
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
    ),
]


def test_add_and_reduce_snailfish_numbers(left: str, right: str, expected: str) -> None:
    pass


SUM_SAMPLES: List[Tuple[Iterable[str], str]] = [
    (["[1,1]", "[2,2]", "[3,3]", "[4,4]"], "[[[[1,1],[2,2]],[3,3]],[4,4]]"),
    (["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5, 5]"], "[[[[3,0],[5,3]],[4,4]],[5,5]]"),
    (
        ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5, 5]", "[6,6]"],
        "[[[[5,0],[7,4]],[5,5]],[6,6]]",
    ),
    (
        [
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
            "[7,[5,[[3,8],[1,4]]]]",
            "[[2,[2,2]],[8,[8,1]]]",
            "[2,9]",
            "[1,[[[9,3],9],[[9,0],[0,7]]]]",
            "[[[5,[7,4]],7],1]",
            "[[[[4,2],2],6],[8,7]]",
        ],
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
    ),
]


@pytest.mark.parametrize("numbers,expected", SUM_SAMPLES)
def test_sum_snailfish_numbers(numbers: Iterable[str], expected: str) -> None:
    parsed_numbers = map(get_number, numbers)
    parsed_expected = get_number(expected)
    assert sum_snailfish_numbers(parsed_numbers) == parsed_expected
