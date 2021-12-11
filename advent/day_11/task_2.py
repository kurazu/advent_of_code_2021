import logging
from itertools import count
from typing import List, Optional, TextIO

import numpy as np
import numpy.typing as npt

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)


def read_input(input: TextIO) -> npt.NDArray[int]:
    return np.array([list(map(int, line)) for line in get_lines(input)], dtype=int)


PADDING = 1
MAX_ENERGY = 9


def main(input: TextIO) -> str:
    octopusses = read_input(input)
    padded_octopusses = np.pad(octopusses, [(PADDING, PADDING), (PADDING, PADDING)])
    octopusses = padded_octopusses[PADDING:-PADDING, PADDING:-PADDING]

    logger.info("Before any steps:\n%s", octopusses)

    flashes = 0
    for step in count(1):
        # increase power level of all octopusses by 1
        octopusses += 1

        # a mask of octopusses that did not yet flash this step
        can_still_flash = np.ones_like(octopusses)

        while True:
            # find the octopusses that need to flash
            flashing: npt.NDArray[bool] = octopusses > MAX_ENERGY

            # the ones that we will flash are the ones that have the power and have
            # not yet flashed this step
            flash: npt.NDArray[bool] = flashing & can_still_flash

            indices = np.argwhere(flash)
            if not len(indices):
                break  # no more octopusses left to flash
            # Increase the power of all neighbouring octopusses
            for y, x in indices:
                padded_octopusses[
                    y - 1 + PADDING : y + 2 + PADDING, x - 1 + PADDING : x + 2 + PADDING
                ] += 1
                # Mark the ones that flashed and remove them from the mask
                can_still_flash[y, x] = False
                # Count number of flashes
                flashes += 1

        # Zero any octopusses that flashed
        octopusses[octopusses > MAX_ENERGY] = 0
        logger.info("Step %d:\n%s", step + 1, octopusses)

        if np.sum(octopusses) == 0:
            return f"{step}"

    raise AssertionError("Simultainous flash not found")


if __name__ == "__main__":
    run_with_file_argument(main)
