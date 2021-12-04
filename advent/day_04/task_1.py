import itertools
import logging
import re
from typing import Iterable, List, TextIO

import numpy as np
import pandas as pd

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    lines = iter(input)
    called_numbers: Iterable[float] = map(float, next(lines).strip().split(","))
    boards: List[List[List[float]]] = []
    while True:
        try:
            empty_line = next(lines)
        except StopIteration:
            break
        assert empty_line == "\n", f"Line {empty_line!r} not empty"
        board = [
            [float(part) for part in re.split(r"\s+", line.strip())]
            for line in itertools.islice(lines, 0, 5)
        ]
        boards.append(board)

    boards_array = np.array(boards)
    for called_number in called_numbers:
        # cross out a number
        boards_array[boards_array == called_number] = np.nan
        breakpoint()

    last_number = 0
    winning_board_sum = 0
    logger.info("last_number=%d, winning_board_sum=%d", last_number, winning_board_sum)
    return f"{last_number * winning_board_sum}"


if __name__ == "__main__":
    run_with_file_argument(main)
