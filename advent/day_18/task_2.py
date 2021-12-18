from __future__ import annotations

import logging
from copy import deepcopy
from itertools import combinations
from typing import TextIO

from ..cli import run_with_file_argument
from .task_1 import add_and_reduce_snailfish_numbers, get_numbers

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    numbers = list(get_numbers(input))
    highest_magnitude = -1

    for number_a, number_b in combinations(numbers, 2):
        a_plus_b = add_and_reduce_snailfish_numbers(
            deepcopy(number_a), deepcopy(number_b)
        )
        a_plus_b_magnitude = a_plus_b.get_magnitude()
        if a_plus_b_magnitude > highest_magnitude:
            highest_magnitude = a_plus_b_magnitude
            logger.info(
                "Highest magnitude %d from %r + %r",
                a_plus_b_magnitude,
                number_a,
                number_b,
            )

        b_plus_a = add_and_reduce_snailfish_numbers(
            deepcopy(number_b), deepcopy(number_a)
        )
        b_plus_a_magnitude = b_plus_a.get_magnitude()
        if b_plus_a_magnitude > highest_magnitude:
            highest_magnitude = b_plus_a_magnitude
            logger.info(
                "Highest magnitude %d from %r + %r",
                b_plus_a_magnitude,
                number_b,
                number_a,
            )

    return f"{highest_magnitude}"


if __name__ == "__main__":
    run_with_file_argument(main)
