import logging
from collections import Counter
from typing import List, TextIO

import numpy as np

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)

DAYS = 256
MAX_COUNTER = 8


def main(input: TextIO) -> str:
    fish = np.zeros((MAX_COUNTER + 1,), dtype=int)
    for status in map(int, input.readline().strip().split(",")):
        fish[status] += 1
    for day in range(DAYS):
        new_fish_count = fish[0]
        fish[:-1] = fish[1:]
        fish[-1] = new_fish_count
        fish[6] += new_fish_count
    fish_count = np.sum(fish)
    return f"{fish_count}"


if __name__ == "__main__":
    run_with_file_argument(main)
