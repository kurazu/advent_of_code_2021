from __future__ import annotations

import logging
from typing import List, Set, TextIO, Tuple

import numpy as np
import numpy.typing as npt

from ..cli import run_with_file_argument
from .task_1 import Instruction, filter_instructions, read_instructions

logger = logging.getLogger(__name__)


class Reactor:
    def __init__(
        self, *, x_points: List[int], y_points: List[int], z_points: List[int]
    ) -> None:
        self.x_points = x_points + [x_points[-1] + 1]
        self.y_points = y_points + [y_points[-1] + 1]
        self.z_points = z_points + [z_points[-1] + 1]
        self.valid_x_points = set(x_points)
        self.valid_y_points = set(y_points)
        self.valid_z_points = set(z_points)
        self.cube = np.zeros(
            (len(self.z_points), len(self.y_points), len(self.x_points)), dtype=bool
        )

    @staticmethod
    def _get_cube_slice(valid_points: Set[int], points: List[int], key: slice) -> slice:
        start = key.start
        assert start in valid_points
        start_index = points.index(start)
        stop = key.stop
        assert stop in valid_points
        stop_index = points.index(stop)
        return slice(start_index, stop_index + 1)

    def __setitem__(self, key: Tuple[slice, slice, slice], value: bool) -> None:
        z_slice, y_slice, x_slice = key
        self.cube[
            self._get_cube_slice(self.valid_z_points, self.z_points, z_slice),
            self._get_cube_slice(self.valid_y_points, self.y_points, y_slice),
            self._get_cube_slice(self.valid_x_points, self.x_points, x_slice),
        ] = value

    @staticmethod
    def _get_cube_size(points: List[int], index: int) -> int:
        start = points[index]
        stop = points[index + 1]
        return stop - start

    def get_volume(
        self, *, z_cube_index: int, y_cube_index: int, x_cube_index: int
    ) -> int:
        z_size = self._get_cube_size(self.z_points, z_cube_index)
        y_size = self._get_cube_size(self.y_points, y_cube_index)
        x_size = self._get_cube_size(self.x_points, x_cube_index)
        return x_size * y_size * z_size

    def sum(self) -> int:
        logger.debug("Starting volume calculation")
        result = 0
        for z_cube_index in range(len(self.z_points) - 1):
            for y_cube_index in range(len(self.y_points) - 1):
                for x_cube_index in range(len(self.x_points) - 1):
                    if self.cube[z_cube_index, y_cube_index, x_cube_index]:
                        volume = self.get_volume(
                            z_cube_index=z_cube_index,
                            y_cube_index=y_cube_index,
                            x_cube_index=x_cube_index,
                        )
                        z_size = self._get_cube_size(self.z_points, z_cube_index)
                        y_size = self._get_cube_size(self.y_points, y_cube_index)
                        x_size = self._get_cube_size(self.x_points, x_cube_index)
                        logger.debug(
                            "Rector cube %d,%d,%d (%d x %d x %d) lit, volume %d",
                            z_cube_index,
                            y_cube_index,
                            x_cube_index,
                            z_size,
                            y_size,
                            x_size,
                            volume,
                        )
                        result += volume
        logger.debug("Final volume %d", result)
        return result


def get_reactor(instructions: List[Instruction]) -> Reactor:
    x_points = sorted(
        {
            mark
            for instruction in instructions
            for mark in [instruction.min_x, instruction.max_x]
        }
    )
    y_points = sorted(
        {
            mark
            for instruction in instructions
            for mark in [instruction.min_y, instruction.max_y]
        }
    )
    z_points = sorted(
        {
            mark
            for instruction in instructions
            for mark in [instruction.min_z, instruction.max_z]
        }
    )
    return Reactor(x_points=x_points, y_points=y_points, z_points=z_points)


def apply_instructions(instructions: List[Instruction], reactor: Reactor) -> None:
    logger.info("Initial reactor %d", reactor.sum())
    for instruction in instructions:
        reactor[
            instruction.min_z : instruction.max_z,
            instruction.min_y : instruction.max_y,
            instruction.min_x : instruction.max_x,
        ] = instruction.state
        logger.info("Reactor now at %d", reactor.sum())


def main(input: TextIO) -> str:
    instructions = list(read_instructions(input))
    reactor = get_reactor(instructions)
    apply_instructions(instructions, reactor)
    return f"{reactor.sum()}"


if __name__ == "__main__":
    run_with_file_argument(main)
