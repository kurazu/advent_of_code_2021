from typing import List, Tuple

import pytest
from advent.day_18.task_1 import get_magnitude, get_number

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
