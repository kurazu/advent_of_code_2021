from __future__ import annotations

import functools
import logging
import operator
from typing import Iterable, List, Set, TextIO, Tuple

import numpy as np
import tqdm

from ..cli import run_with_file_argument
from .task_1 import Instruction, read_instructions

logger = logging.getLogger(__name__)


class Reactor:
    def __init__(
        self, *, x_points: List[int], y_points: List[int], z_points: List[int]
    ) -> None:
        self.x_points = x_points
        self.y_points = y_points
        self.z_points = z_points
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
        assert stop + 1 in valid_points
        stop_index = points.index(stop + 1)
        return slice(start_index, stop_index)

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
        result = 0
        with tqdm.tqdm(total=len(self)) as pbar:
            for z_cube_index in range(len(self.z_points) - 1):
                for y_cube_index in range(len(self.y_points) - 1):
                    for x_cube_index in range(len(self.x_points) - 1):
                        if self.cube[z_cube_index, y_cube_index, x_cube_index]:
                            result += self.get_volume(
                                z_cube_index=z_cube_index,
                                y_cube_index=y_cube_index,
                                x_cube_index=x_cube_index,
                            )
                        pbar.update(1)
        return result

    def __len__(self) -> int:
        shape: Iterable[int] = self.cube.shape
        return functools.reduce(operator.mul, shape)


def get_reactor(instructions: List[Instruction]) -> Reactor:
    x_points = sorted(
        {
            mark
            for instruction in instructions
            for mark in [instruction.min_x, instruction.max_x + 1]
        }
    )
    y_points = sorted(
        {
            mark
            for instruction in instructions
            for mark in [instruction.min_y, instruction.max_y + 1]
        }
    )
    z_points = sorted(
        {
            mark
            for instruction in instructions
            for mark in [instruction.min_z, instruction.max_z + 1]
        }
    )
    reactor = Reactor(x_points=x_points, y_points=y_points, z_points=z_points)
    logger.info("Created reactor of size %s", f"{len(reactor):,}")
    return reactor


def apply_instructions(instructions: List[Instruction], reactor: Reactor) -> None:
    for instruction in instructions:
        reactor[
            instruction.min_z : instruction.max_z,
            instruction.min_y : instruction.max_y,
            instruction.min_x : instruction.max_x,
        ] = instruction.state


def main(input: TextIO) -> str:
    logger.info("Reading instructions")
    instructions = list(read_instructions(input))
    logger.info("Creating reactor")
    reactor = get_reactor(instructions)
    logger.info("Applying instructions")
    apply_instructions(instructions, reactor)
    logger.info("Calculating cubes lit")
    return f"{reactor.sum()}"


if __name__ == "__main__":
    run_with_file_argument(main)
