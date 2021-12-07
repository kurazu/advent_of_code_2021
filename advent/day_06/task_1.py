import logging
from typing import List, TextIO

import numpy as np

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)

DAYS = 80


def main(input: TextIO) -> str:
    fish = np.array(list(map(int, input.readline().strip().split(","))), dtype=int)
    logger.info("Initial state: %s", ",".join(map(str, fish)))
    for day in range(DAYS):
        mask = fish == 0
        new_fish_count = np.sum(mask)
        fish[mask] = 6
        fish[~mask] -= 1
        new_fish = np.ones((new_fish_count,), dtype=int)
        new_fish.fill(8)
        fish = np.concatenate([fish, new_fish])
        logger.info("After %2d days: %s", day + 1, ",".join(map(str, fish[:26])))
    return f"{len(fish)}"


if __name__ == "__main__":
    run_with_file_argument(main)
