from __future__ import annotations

import itertools
import logging
import math
import re
from collections import Counter
from itertools import combinations, starmap
from typing import Dict, Iterable, List, TextIO, Tuple

import networkx as nx
import numpy as np
import numpy.typing as npt
from networkx.drawing.nx_pydot import write_dot

from ..cli import run_with_file_argument
from ..io_utils import read_line
from .task_1 import (build_neighbourhood_graph, check_for_repeating_distances,
                     read_beacons, traverse_and_resolve_scanners)

logger = logging.getLogger(__name__)


def manhattan_distance(a: npt.NDArray, b: npt.NDArray) -> float:
    dist: float = np.sum(np.abs(a - b))
    return dist


def main(input: TextIO) -> str:
    scanners = list(read_beacons(input))
    check_for_repeating_distances(scanners)
    neighbourhood_graph = build_neighbourhood_graph(scanners)
    scanner_positions = traverse_and_resolve_scanners(scanners, neighbourhood_graph)

    scanner_distances = itertools.starmap(
        manhattan_distance, combinations(scanner_positions, 2)
    )
    biggest_distance = max(scanner_distances)
    return f"{biggest_distance}"


if __name__ == "__main__":
    run_with_file_argument(main)
