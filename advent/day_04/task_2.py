import itertools
import logging
import re
from typing import Iterable, List, TextIO

import numpy as np
import pandas as pd

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)

BOARD_SIZE = 5


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
            for line in itertools.islice(lines, 0, BOARD_SIZE)
        ]
        boards.append(board)

    boards_array = np.array(boards)
    assert boards_array.shape[1:] == (BOARD_SIZE, BOARD_SIZE)
    previous = np.zeros((len(boards_array),), dtype="bool")
    for called_number in called_numbers:
        # cross out a number
        boards_array[boards_array == called_number] = np.nan

        # check for cross-out numbers
        eliminated = np.isnan(boards_array)

        # check for full rows
        rows = np.sum(eliminated, axis=-1)
        full_rows = rows >= BOARD_SIZE
        has_full_row = np.any(full_rows, axis=-1)
        assert has_full_row.shape == (len(boards_array),)
        # if np.any(has_full_row):
        #     # we have a match, we need to figure out on which board though
        #     winning_board_index = np.argmax(has_full_row)
        #     break

        # check for full columns
        columns = np.sum(eliminated, axis=-2)
        full_columns = columns >= BOARD_SIZE
        has_full_column = np.any(full_columns, axis=-1)
        assert has_full_column.shape == (len(boards_array),)
        # if np.any(has_full_column):
        #     # we have a match, we need to figure out on which board though
        #     winning_board_index = np.argmax(has_full_column)
        #     break

        has_full_row_or_column = has_full_row | has_full_column
        if np.all(has_full_row_or_column):  # we wait until all boards win
            winning_board_index = np.argmax(~previous)
            break
        previous = has_full_row_or_column
    else:
        raise AssertionError("No board wins")

    last_number = int(called_number)
    winning_board_sum = int(np.nansum(boards_array[winning_board_index]))
    logger.info("last_number=%d, winning_board_sum=%d", last_number, winning_board_sum)
    return f"{last_number * winning_board_sum}"


if __name__ == "__main__":
    run_with_file_argument(main)
