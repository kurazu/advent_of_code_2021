from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional, TextIO

import numpy as np
import numpy.typing as npt

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)


PATTERN = re.compile(
    r"^\#\#\#\#\#\#\#\#\#\#\#\#\#\n"
    r"\#\.\.\.\.\.\.\.\.\.\.\.\#\n"
    r"\#\#\#(?P<AH>[A-D])\#(?P<BH>[A-D])\#(?P<CH>[A-D])\#(?P<DH>[A-D])\#\#\#\n"
    r"\s\s\#(?P<AL>[A-D])\#(?P<BL>[A-D])\#(?P<CL>[A-D])\#(?P<DL>[A-D])\#\n"
    r"\s\s\#\#\#\#\#\#\#\#\#$"
)


class Amphipod(Enum):
    AMBER = "A"
    BRONZE = "B"
    COPPER = "C"
    DESERT = "D"


@dataclass
class Board:
    # Left corner
    LF: Optional[Amphipod] = None
    LN: Optional[Amphipod] = None

    # Spaces between rooms
    AB: Optional[Amphipod] = None
    BC: Optional[Amphipod] = None
    CD: Optional[Amphipod] = None

    # Right corner
    RN: Optional[Amphipod] = None
    RF: Optional[Amphipod] = None

    # Rooms
    AH: Optional[Amphipod] = None
    AL: Optional[Amphipod] = None

    BH: Optional[Amphipod] = None
    BL: Optional[Amphipod] = None

    CH: Optional[Amphipod] = None
    CL: Optional[Amphipod] = None

    DH: Optional[Amphipod] = None
    DL: Optional[Amphipod] = None

    def __repr__(self) -> str:
        def f(amphipod: Optional[Amphipod]) -> str:
            return amphipod.value if amphipod is not None else " "

        return f"""#############
#{f(self.LF)}{f(self.LN)} {f(self.AB)} {f(self.BC)} {f(self.CD)} {f(self.RN)}{f(self.RF)}#
###{f(self.AH)}#{f(self.BH)}#{f(self.CH)}#{f(self.DH)}###
  #{f(self.AL)}#{f(self.BL)}#{f(self.CL)}#{f(self.DL)}#
  #########"""


def read_board(input: TextIO) -> Board:
    text = input.read()
    match = PATTERN.match(text)
    assert match
    match_groups = match.groupdict()
    parsed_groups = {key: Amphipod(value) for key, value in match_groups.items()}
    return Board(**parsed_groups)


def main(input: TextIO) -> str:
    starting_board = read_board(input)
    breakpoint()
    energy = 0
    return f"{energy}"


if __name__ == "__main__":
    run_with_file_argument(main)
