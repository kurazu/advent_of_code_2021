from __future__ import annotations

import logging
from typing import TextIO

from ..cli import run_with_file_argument
from .task_1 import Vector, fire, get_target_area

logger = logging.getLogger(__name__)


def find_min_x_velocity(min_x: int) -> int:
    distance = 1
    x_velocity = 1
    while distance < min_x:
        x_velocity += 1
        distance += x_velocity
    return x_velocity


def main(input: TextIO) -> str:
    target_area = get_target_area(input)
    logger.info("Target area: %s", target_area)

    min_x_velocity = find_min_x_velocity(target_area.min_x)
    logger.info("Min X velocity %d", min_x_velocity)
    max_x_velocity = target_area.max_x
    logger.info("Max X velocity %d", max_x_velocity)

    min_y_velocity = target_area.min_y
    logger.info("Min Y velocity %d", min_y_velocity)

    y = min_y_velocity
    hits = 0
    while True:
        for x in range(min_x_velocity, max_x_velocity + 1):
            velocity = Vector(x=x, y=y)
            if fire(velocity, target_area) is not None:
                hits += 1
                logger.info("Scored %d hit at x=%d,y=%d", hits, x, y)
        y += 1

    return f"{hits}"


if __name__ == "__main__":
    run_with_file_argument(main)
