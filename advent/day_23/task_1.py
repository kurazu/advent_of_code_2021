from __future__ import annotations

import logging
import operator
import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List, NamedTuple, Optional, Set, TextIO, Tuple

from ..cli import run_with_file_argument

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

    @staticmethod
    def format_amphipod(amphipod: Optional[Amphipod]) -> str:
        return amphipod.value if amphipod is not None else " "

    def __repr__(self) -> str:
        f = self.format_amphipod

        return f"""#############
#{f(self.LF)}{f(self.LN)} {f(self.AB)} {f(self.BC)} {f(self.CD)} {f(self.RN)}{f(self.RF)}#
###{f(self.AH)}#{f(self.BH)}#{f(self.CH)}#{f(self.DH)}###
  #{f(self.AL)}#{f(self.BL)}#{f(self.CL)}#{f(self.DL)}#
  #########"""

    def id(self) -> str:
        f = self.format_amphipod

        return (
            f"{f(self.LF)}{f(self.LN)}{f(self.AB)}{f(self.BC)}{f(self.CD)}{f(self.RN)}{f(self.RF)}"
            f"{f(self.AH)}{f(self.BH)}{f(self.CH)}{f(self.DH)}"
            f"{f(self.AL)}{f(self.BL)}{f(self.CL)}{f(self.DL)}"
        )


TARGET_BOARD = Board(
    AH=Amphipod.AMBER,
    AL=Amphipod.AMBER,
    BH=Amphipod.BRONZE,
    BL=Amphipod.BRONZE,
    CH=Amphipod.COPPER,
    CL=Amphipod.COPPER,
    DH=Amphipod.DESERT,
    DL=Amphipod.DESERT,
)


def read_board(input: TextIO) -> Board:
    text = input.read()
    match = PATTERN.match(text)
    assert match
    match_groups = match.groupdict()
    parsed_groups = {key: Amphipod(value) for key, value in match_groups.items()}
    return Board(**parsed_groups)


class DFSResult(NamedTuple):
    steps: List[Board]
    total_energy: int


def get_possible_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    return []


Stack = List[Board]


def dfs(starting_board: Board) -> Tuple[Stack, int]:
    best_energy = float("inf")
    boards_seen: Set[str] = set()

    def recursive_search(
        stack: Stack, stack_energy: int
    ) -> Optional[Tuple[Stack, int]]:
        nonlocal best_energy

        *_, current_board = stack
        boards_seen.add(current_board.id())
        if current_board == TARGET_BOARD:
            # Terminal state
            best_energy = min(best_energy, stack_energy)
            return stack, stack_energy
        else:
            possibilities: List[Tuple[Stack, int]] = []
            for possible_board, move_energy in get_possible_moves(current_board):
                possible_board_id = possible_board.id()
                possible_energy = stack_energy + move_energy
                if possible_board_id in boards_seen:
                    continue  # We've seen this state
                elif possible_energy >= best_energy:
                    continue  # This state is already worse than the current best
                else:  # State to explore
                    possible_result = recursive_search(
                        stack + [possible_board], possible_energy
                    )
                    if possible_result is None:
                        continue
                    else:
                        possibilities.append(possible_result)
            if not possibilities:
                return None
            else:
                possibilities.sort(key=operator.itemgetter(1))
                return possibilities[0]

    best_result = recursive_search([starting_board], 0)
    assert best_result is not None
    return best_result


def main(input: TextIO) -> str:
    starting_board = read_board(input)
    stack, energy = dfs(starting_board)
    for board in stack:
        logger.info("Step\n%r\n", board)
    return f"{energy}"


if __name__ == "__main__":
    run_with_file_argument(main)
