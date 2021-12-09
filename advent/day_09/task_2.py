import logging
import operator
from collections import defaultdict, deque
from functools import reduce
from typing import Deque, Dict, Iterable, List, NamedTuple, TextIO

import numpy as np
from numpy import typing as npt

from ..cli import run_with_file_argument
from ..io_utils import get_lines
from .task_1 import get_low_points, parse_input

logger = logging.getLogger(__name__)


class Point(NamedTuple):
    x: int
    y: int


MIN_VALUE = -1
MAX_VALUE = 10


def get_neighbours(point: Point, heightmap: npt.NDArray[int]) -> Iterable[Point]:
    height, width = heightmap.shape
    if point.x - 1 >= 0:
        yield Point(x=point.x - 1, y=point.y)
    if point.x + 1 < width:
        yield Point(x=point.x + 1, y=point.y)
    if point.y - 1 >= 0:
        yield Point(x=point.x, y=point.y - 1)
    if point.y + 1 < height:
        yield Point(x=point.x, y=point.y + 1)


def find_basin(low_point: Point, heightmap: npt.NDArray[int]) -> npt.NDArray[bool]:
    queue: Dict[Point, int] = defaultdict(lambda: MAX_VALUE)
    queue[low_point] = MIN_VALUE
    basin = np.zeros_like(heightmap, dtype=bool)

    while queue:
        point = next(iter(queue))
        previous_value = queue.pop(point)
        point_value = heightmap[point.y, point.x]
        if point_value >= 9:
            continue  # peaks are excluded
        elif point_value <= previous_value:
            continue  # not uphill traversal
        # This point is another part of the basin
        basin[point.y, point.x] = True
        # Check all neighboring points
        for neighbour_point in get_neighbours(point, heightmap):
            if basin[neighbour_point.y, neighbour_point.x]:
                continue  # this point is already belonging to this basin
            queue[neighbour_point] = min(queue[neighbour_point], point_value)

    logger.info("Basin\n%s", basin.astype(int))
    return basin


def main(input: TextIO) -> str:
    heightmap = parse_input(input)
    low_points = get_low_points(heightmap)
    basins: List[npt.NDArray[bool]] = []
    for y, row in enumerate(low_points):
        for x, cell in enumerate(row):
            if not cell:
                continue
            basin = find_basin(Point(x=x, y=y), heightmap)
            basins.append(basin)
    basins.sort(key=np.sum, reverse=True)
    biggest_basins = basins[:3]
    sizes = map(np.sum, biggest_basins)
    multiplied_sizes = reduce(operator.mul, sizes)
    return f"{multiplied_sizes}"


if __name__ == "__main__":
    run_with_file_argument(main)
