from __future__ import annotations

import logging
from typing import TextIO

import numpy as np
import numpy.typing as npt

from ..cli import run_with_file_argument
from ..io_utils import read_numbers_array
from .task_1 import find_route_risk

logger = logging.getLogger(__name__)

ENLARGE_TIMES = 5


def shift_world(world: npt.NDArray[int], diff: int) -> npt.NDArray[int]:
    shifted_world: npt.NDArray[int] = (world + diff - 1) % 9 + 1
    return shifted_world


def enlarge_world(world: npt.NDArray[int]) -> npt.NDArray[int]:
    height, width = world.shape
    # create a new map 5 times bigger
    enlarged_world = np.zeros(
        (height * ENLARGE_TIMES, width * ENLARGE_TIMES), dtype=world.dtype
    )
    for y_diff in range(ENLARGE_TIMES):
        for x_diff in range(ENLARGE_TIMES):
            diff = x_diff + y_diff
            enlarged_world[
                y_diff * height : (y_diff + 1) * height,
                x_diff * width : (x_diff + 1) * width,
            ] = shift_world(world, diff)

    return enlarged_world


def main(input: TextIO) -> str:
    # read the map
    world = read_numbers_array(input)
    # enlarge
    enlarged_world = enlarge_world(world)
    # find route
    risk = find_route_risk(enlarged_world)
    return f"{risk}"


if __name__ == "__main__":
    run_with_file_argument(main)
