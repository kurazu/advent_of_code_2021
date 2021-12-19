from __future__ import annotations

import logging
import math
import re
from collections import Counter
from itertools import combinations, starmap
from typing import Dict, Iterable, List, TextIO, Tuple

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


def get_edges(beacons: npt.NDArray[int]) -> Dict[float, Tuple[int, int]]:
    enumerated_beacons = enumerate(beacons)
    result: Dict[float, Tuple[int, int]] = {}
    for (a_idx, a_beacon), (b_idx, b_beacon) in combinations(enumerated_beacons, 2):
        dist = distance(a_beacon, b_beacon)
        assert dist not in result
        result[dist] = a_idx, b_idx
    return result


def main(input: TextIO) -> str:
    scanners = list(read_beacons(input))

    has_repeating_distances = False
    for i, beacons in enumerate(scanners):
        distances = starmap(distance, combinations(beacons, 2))
        counter = Counter(distances)
        repeating_distances = (
            count for dist, count in counter.most_common() if count > 2
        )
        for count in repeating_distances:
            logger.info("Scanner %d repeated distance %d", i, count)
            has_repeating_distances = True
        logger.info("Scanner %d done", i)
    assert not has_repeating_distances

    # if 12 nodes need to overlap, then COMB(12,2) edges must math (size of clique edges)
    min_edges = math.comb(12, 2)
    for (a_idx, a), (b_idx, b) in combinations(enumerate(scanners), 2):
        first_edges = get_edges(a)
        second_edges = get_edges(b)
        common_edges = set(first_edges) & set(second_edges)
        if len(common_edges) >= min_edges:
            logger.info(
                "Scanner %d and %d have %d common edges",
                a_idx,
                b_idx,
                len(common_edges),
            )

    number_of_beacons = 0
    return f"{number_of_beacons}"


if __name__ == "__main__":
    run_with_file_argument(main)
