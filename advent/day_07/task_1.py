import logging
from typing import TextIO

import numpy as np

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    crabs = np.array(list(map(int, input.readline().strip().split(","))), dtype=int)
    max_x = np.max(crabs)
    distances = np.abs(crabs - np.expand_dims(np.arange(max_x + 1), 1))
    target_distances = np.sum(distances, axis=-1)
    position = np.argmin(target_distances)
    logger.info("Best position: %d", position)
    fuel_used = np.min(target_distances)
    return f"{fuel_used}"


if __name__ == "__main__":
    run_with_file_argument(main)
