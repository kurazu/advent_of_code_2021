from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Iterable, Iterator, List, NamedTuple, Set, TextIO, Tuple

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

    def sum(self) -> int:
        return 0


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
    for state, min_x, max_x, min_y, max_y, min_z, max_z in instructions:
        reactor[min_z:max_z, min_y:max_y, min_x:max_x] = state


def sum_reactor(reactor: Reactor) -> int:
    pass


def main(input: TextIO) -> str:
    instructions = list(filter_instructions(read_instructions(input), 50))
    reactor = get_reactor(instructions)
    apply_instructions(instructions, reactor)
    return f"{reactor.sum()}"


if __name__ == "__main__":
    run_with_file_argument(main)
