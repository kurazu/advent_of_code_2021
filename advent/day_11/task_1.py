import logging
from typing import List, Optional, TextIO

import numpy as np
import numpy.typing as npt

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)


def read_input(input: TextIO) -> npt.NDArray[int]:
    return np.array([list(map(int, line)) for line in get_lines(input)], dtype=int)


STEPS = 3
PADDING = 1


def main(input: TextIO) -> str:
    octopusses = read_input(input)
    padded_octopusses = np.pad(octopusses, [(PADDING, PADDING), (PADDING, PADDING)])
    octopusses = padded_octopusses[PADDING:-PADDING, PADDING:-PADDING]
    flashes = 0
    for step in range(STEPS):
        # increase power level of all octopusses by 1
        octopusses += 1

        # a mask of octopusses that did not yet flash this step
        not_flashed = np.ones_like(octopusses)

        while True:
            # find the octopusses that need to flash
            flashing: npt.NDArray[bool] = octopusses >= 9

            # the ones that we will flash are the ones that have the power and have
            # not yet flashed this step
            flash: npt.NDArray[bool] = flashing & not_flashed

            indices = np.argwhere(flash)
            if not len(indices):
                break  # no more octopusses left to flash
            # Increase the power of all neighbouring octopusses
            for y, x in indices:
                padded_octopusses[
                    y - 1 + PADDING : y + 1 + PADDING, x - 1 + PADDING : x + 1 + PADDING
                ] += 1
                flashes += 1

            # Mark the ones that flashed and remove them from the mask
            not_flashed[flash] = True

        logger.info("Step %d:\n%s", step + 1, octopusses)
    flashes = 0
    return f"{flashes}"


if __name__ == "__main__":
    run_with_file_argument(main)
