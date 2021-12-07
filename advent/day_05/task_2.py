import logging
import re
from typing import Iterable, List, TextIO

import numpy as np

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)

LINE_REGEXP = re.compile(
    r"^(?P<start_x>\d+),(?P<start_y>\d+)\s\-\>\s(?P<end_x>\d+),(?P<end_y>\d+)$"
)


def range(start: int, end: int) -> Iterable[int]:
    sign = np.sign(end - start)
    result: Iterable[int] = np.arange(start, end + sign, sign)
    return result


def main(input: TextIO) -> str:
    edges: List[List[int]] = []
    for line in input:
        line = line.strip()
        if not line:
            continue
        match = LINE_REGEXP.match(line)
        assert match is not None
        start_x, start_y, end_x, end_y = map(int, match.groups())
        edges.append([start_x, start_y, end_x, end_y])

    edges_array = np.array(edges)
    del edges

    max_x = np.max(edges_array[:, (0, 2)])
    max_y = np.max(edges_array[:, (1, 3)])
    board = np.zeros((max_x + 1, max_y + 1))

    for start_x, start_y, end_x, end_y in edges_array:
        if start_x == end_x:  # vertical line
            ranges = [start_y, end_y]
            board[start_x, min(ranges) : max(ranges) + 1] += 1
        elif start_y == end_y:  # horizontal line
            ranges = [start_x, end_x]
            board[min(ranges) : max(ranges) + 1, start_y] += 1
        else:  # diagonal line
            for x, y in zip(
                range(start_x, end_x),
                range(start_y, end_y),
            ):
                board[x, y] += 1

    overlapping_points = np.sum(board >= 2)
    return f"{overlapping_points}"


if __name__ == "__main__":
    run_with_file_argument(main)
