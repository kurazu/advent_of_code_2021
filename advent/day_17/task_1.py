from __future__ import annotations

import functools
import io
import logging
import operator
import re
from dataclasses import dataclass
from typing import (Callable, Dict, Iterable, List, NamedTuple, Optional,
                    Protocol, TextIO)

from returns.curry import partial

from ..cli import run_with_file_argument
from ..io_utils import read_line

logger = logging.getLogger(__name__)


TARGET_SPEC_PATTERN = re.compile(
    r"^target area: x=(?P<min_x>\d+)\.\.(?P<max_x>\d+), "
    r"y=(?P<min_y>\-\d+)..(?P<max_y>-\d+)$"
)


@dataclass
class Vector:
    x: int
    y: int

    def __add__(self, velocity: Vector) -> Vector:
        return Vector(x=self.x + velocity.x, y=self.y + velocity.y)


@dataclass
class TargetArea:
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def __contains__(self, point: Vector) -> bool:
        return (
            self.min_x <= point.x <= self.max_x and self.min_y <= point.y <= self.max_y
        )


def drag_x_velocity(x_velocity: int) -> int:
    assert x_velocity >= 0
    if x_velocity > 0:
        return x_velocity - 1
    else:
        return 0


def fire(velocity: Vector, target_area: TargetArea) -> Optional[int]:
    # logger.info("Firing %s", velocity)
    position = Vector(x=0, y=0)
    positions = [position]
    while position.x <= target_area.max_x and position.y >= target_area.min_y:
        position = position + velocity
        positions.append(position)
        velocity.x = drag_x_velocity(velocity.x)
        velocity.y -= 1
        if position in target_area:
            return max(position.y for position in positions)
    return None


def arithmetic_progression_sum(n: int) -> int:
    return ((1 + n) * n) // 2


def find_valid_x_velocities(target_area: TargetArea) -> Iterable[int]:
    x_velocity = 1
    while (x_distance := arithmetic_progression_sum(x_velocity)) <= target_area.max_x:
        if x_distance >= target_area.min_x:
            yield x_velocity
        x_velocity += 1


def get_target_area(input: TextIO) -> TargetArea:
    target_spec = read_line(input)
    match = TARGET_SPEC_PATTERN.match(target_spec)
    assert match is not None

    return TargetArea(
        min_x=int(match.group("min_x")),
        max_x=int(match.group("max_x")),
        min_y=int(match.group("min_y")),
        max_y=int(match.group("max_y")),
    )


def main(input: TextIO) -> str:
    target_area = get_target_area(input)

    logger.info("Target area: %s", target_area)

    max_y = fire(Vector(x=7, y=2), target_area)
    logger.info("max y=%s", max_y)
    max_y = fire(Vector(x=6, y=3), target_area)
    logger.info("max y=%s", max_y)
    max_y = fire(Vector(x=17, y=-4), target_area)
    logger.info("max y=%s", max_y)
    max_y = fire(Vector(x=6, y=9), target_area)
    logger.info("max y=%s", max_y)

    valid_x_velocities = list(find_valid_x_velocities(target_area))
    logger.info("x velocities to try %s", valid_x_velocities)

    velocities_to_try = (
        Vector(x=x_velocity, y=y_velocity)
        for x_velocity in valid_x_velocities
        for y_velocity in range(1000, -1000, -1)
    )
    best_ys = filter(
        None, map(partial(fire, target_area=target_area), velocities_to_try)
    )

    top_y = max(best_ys)
    return f"{top_y}"


if __name__ == "__main__":
    run_with_file_argument(main)
