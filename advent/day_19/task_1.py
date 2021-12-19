from __future__ import annotations

import logging
import re
from collections import Counter
from itertools import combinations, starmap
from typing import Iterable, List, TextIO, Tuple

import numpy as np
import numpy.typing as npt

from ..cli import run_with_file_argument
from ..io_utils import read_line

logger = logging.getLogger(__name__)

HEADER_PATTERN = re.compile(r"^\-\-\-\sscanner\s\d+\s\-\-\-$")


def read_beacons(input: TextIO) -> Iterable[npt.NDArray]:
    while True:
        header = read_line(input)
        if not header:
            break
        beacons: List[Tuple[int, int, int]] = []
        assert HEADER_PATTERN.match(header) is not None
        while line := read_line(input):
            x, y, z = map(int, line.split(","))
            beacons.append((x, y, z))
        yield np.array(beacons)


def distance(a: npt.NDArray[int], b: npt.NDArray[int]) -> float:
    dist: float = np.linalg.norm(a - b)
    return dist


def main(input: TextIO) -> str:
    scanners = list(read_beacons(input))

    for i, beacons in enumerate(scanners):
        distances = starmap(distance, combinations(beacons, 2))
        counter = Counter(distances)
        repeating_distances = (
            count for dist, count in counter.most_common() if count > 2
        )
        for count in repeating_distances:
            logger.info("Scanner %d repeated distance %d", i, count)
        logger.info("Scanner %d done", i)

    number_of_beacons = 0
    return f"{number_of_beacons}"


if __name__ == "__main__":
    run_with_file_argument(main)
