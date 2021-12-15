from __future__ import annotations

import logging
from typing import Iterable, NamedTuple, TextIO

import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from ..cli import run_with_file_argument
from ..io_utils import read_numbers_array

logger = logging.getLogger(__name__)


class Point(NamedTuple):
    y: int
    x: int

    def get_left(self) -> Point:
        return Point(x=self.x - 1, y=self.y)

    def get_right(self) -> Point:
        return Point(x=self.x + 1, y=self.y)

    def get_above(self) -> Point:
        return Point(x=self.x, y=self.y - 1)

    def get_below(self) -> Point:
        return Point(x=self.x, y=self.y + 1)


def find_route_risk(world: npt.NDArray[int]) -> int:
    height, width = world.shape

    # the distances are all set to "infinity"
    max_value = np.iinfo(world.dtype).max
    distances = np.zeros_like(world)
    distances.fill(max_value)

    # Mask of visited points
    visited = np.zeros_like(world, dtype=bool)

    # we start at top left and are supposed to end at bottom right
    start_point = Point(y=0, x=0)
    end_point = Point(y=height - 1, x=width - 1)

    # we visit the starting points
    distances[start_point] = 0

    def get_neighbours(point: Point) -> Iterable[Point]:
        # left
        left = point.get_left()
        if left.x >= 0:
            yield left
        # right
        right = point.get_right()
        if right.x < width:
            yield right
        # above
        above = point.get_above()
        if above.y >= 0:
            yield above
        # below
        below = point.get_below()
        if below.y < height:
            yield below

    def get_unvisited_neighbours(point: Point) -> Iterable[Point]:
        for point in get_neighbours(point):
            if not visited[point]:
                yield point

    def choose_current() -> Point:
        # Choose unvisited point with lowest distance
        y, x = np.unravel_index(
            np.argmin(np.where(visited, max_value, distances)), distances.shape
        )
        return Point(y=int(y), x=int(x))

    # calculate distances from start point to all other points
    # using Dijkstra's algorithm
    for _ in tqdm(range(width * height)):
        current = choose_current()
        for neighbour in get_unvisited_neighbours(current):
            cost = world[neighbour]
            distances[neighbour] = min(distances[neighbour], distances[current] + cost)
        visited[current] = True

    # query for distance to end point
    risk: int = distances[end_point]
    return risk


def main(input: TextIO) -> str:
    # read the map
    world = read_numbers_array(input)
    risk = find_route_risk(world)
    return f"{risk}"


if __name__ == "__main__":
    run_with_file_argument(main)
