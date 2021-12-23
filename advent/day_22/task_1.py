from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from itertools import cycle
from typing import Iterable, Iterator, NamedTuple, TextIO

import numpy as np
import numpy.typing as npt

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)

PATTERN = re.compile(
    r"^(?P<state>(on|off)) "
    r"x=(?P<min_x>\-?\d+)\.\.(?P<max_x>\-?\d+),"
    r"y=(?P<min_y>\-?\d+)\.\.(?P<max_y>\-?\d+),"
    r"z=(?P<min_z>\-?\d+)\.\.(?P<max_z>\-?\d+)"
    r"$"
)


class Instruction(NamedTuple):
    state: bool
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int


def read_instruction(line: str) -> Instruction:
    match = PATTERN.match(line)
    assert match is not None
    return Instruction(
        state=match.group("state") == "on",
        min_x=int(match.group("min_x")),
        max_x=int(match.group("max_x")),
        min_y=int(match.group("min_y")),
        max_y=int(match.group("max_y")),
        min_z=int(match.group("min_z")),
        max_z=int(match.group("max_z")),
    )


def read_instructions(input: TextIO) -> Iterable[Instruction]:
    return map(read_instruction, get_lines(input))


def filter_instructions(
    instructions: Iterable[Instruction], max_axis: int
) -> Iterable[Instruction]:
    return filter(
        lambda instruction: (
            abs(instruction.min_x) <= max_axis
            and abs(instruction.max_x) <= max_axis
            and abs(instruction.min_y) <= max_axis
            and abs(instruction.max_y) <= max_axis
            and abs(instruction.min_z) <= max_axis
            and abs(instruction.max_z) <= max_axis
        ),
        instructions,
    )


def get_reactor(max_axis: int) -> npt.NDArray[bool]:
    reactor_size = max_axis * 2 + 1  # 50 => +50, -50 and 0
    return np.zeros((reactor_size, reactor_size, reactor_size), dtype=bool)


def apply_instructions(
    instructions: Iterable[Instruction], reactor: npt.NDArray[bool], max_axis: int
) -> None:
    for state, min_x, max_x, min_y, max_y, min_z, max_z in instructions:
        reactor[
            max_axis + min_z : max_axis + max_z + 1,
            max_axis + min_y : max_axis + max_y + 1,
            max_axis + min_x : max_axis + max_x + 1,
        ] = state


def main(input: TextIO) -> str:
    max_axis = 50
    instructions = filter_instructions(read_instructions(input), max_axis)
    reactor = get_reactor(max_axis)
    apply_instructions(instructions, reactor, max_axis)
    reactor_cubes_on = np.sum(reactor)
    return f"{reactor_cubes_on}"


if __name__ == "__main__":
    run_with_file_argument(main)
