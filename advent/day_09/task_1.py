import logging
from typing import TextIO

import numpy as np

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    heightmap = np.array([list(map(int, line)) for line in get_lines(input)], dtype=int)
    height, width = heightmap.shape
    LOTS = 100

    padded_heightmap = np.pad(
        heightmap, [(1, 1), (1, 1)], mode="constant", constant_values=LOTS
    )

    left_higher = padded_heightmap[1:-1, :-2] > heightmap
    right_higher = padded_heightmap[1:-1, 2:] > heightmap
    top_higher = padded_heightmap[:-2, 1:-1] > heightmap
    bottom_higher = padded_heightmap[2:, 1:-1] > heightmap
    all_higher = left_higher & right_higher & top_higher & bottom_higher
    risk = np.sum(all_higher * (heightmap + 1))
    return f"{risk}"


if __name__ == "__main__":
    run_with_file_argument(main)
