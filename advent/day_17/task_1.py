from __future__ import annotations

import functools
import io
import logging
import operator
import re
from dataclasses import dataclass
from typing import (Callable, Dict, Iterable, List, NamedTuple, Optional,
                    Protocol, TextIO)

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
    position = Vector(x=0, y=0)
    positions = [position]
    while position.x <= target_area.max_x and position.y >= target_area.min_y:
        position = position + velocity
        positions.append(position)
        velocity.x = drag_x_velocity(velocity.x)
        velocity.y -= 1
        logger.info(
            "After step %d the position is x=%d,y=%d",
            len(positions),
            position.x,
            position.y,
        )
        if position in target_area:
            logger.info("HIT!")
            return max(position.y for position in positions)
    logger.info("Miss x=%d,y=%d", position.x, position.y)
    return None




def main(input: TextIO) -> str:
    # read the map
    target_spec = read_line(input)
    match = TARGET_SPEC_PATTERN.match(target_spec)
    assert match is not None

    target_area = TargetArea(
        min_x=int(match.group("min_x")),
        max_x=int(match.group("max_x")),
        min_y=int(match.group("min_y")),
        max_y=int(match.group("max_y")),
    )

    logger.info("Target area: %s", target_area)

    max_y = fire(Vector(x=7, y=2), target_area)
    logger.info("max y=%s", max_y)
    max_y = fire(Vector(x=6, y=3), target_area)
    logger.info("max y=%s", max_y)

    top_y = 0
    return f"{top_y}"


if __name__ == "__main__":
    run_with_file_argument(main)
