import logging
from typing import TextIO

import numpy as np
from numpy import typing as npt

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)


def parse_input(input: TextIO) -> npt.NDArray[int]:
    return np.array([list(map(int, line)) for line in get_lines(input)], dtype=int)


def get_low_points(heightmap: npt.NDArray[int]) -> npt.NDArray[bool]:
    height, width = heightmap.shape
    LOTS = 100

    padded_heightmap = np.pad(
        heightmap, [(1, 1), (1, 1)], mode="constant", constant_values=LOTS
    )

    left_higher = padded_heightmap[1:-1, :-2] > heightmap
    right_higher = padded_heightmap[1:-1, 2:] > heightmap
    top_higher = padded_heightmap[:-2, 1:-1] > heightmap
    bottom_higher = padded_heightmap[2:, 1:-1] > heightmap
    all_higher: npt.NDArray[bool] = (
        left_higher & right_higher & top_higher & bottom_higher
    )
    return all_higher


def main(input: TextIO) -> str:
    heightmap = parse_input(input)
    all_higher = get_low_points(heightmap)
    risk = np.sum(all_higher * (heightmap + 1))
    return f"{risk}"


if __name__ == "__main__":
    run_with_file_argument(main)
