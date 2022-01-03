from __future__ import annotations

import logging
import operator
import re
from copy import copy
from dataclasses import dataclass
from enum import Enum
from typing import (DefaultDict, Dict, Iterable, List, NamedTuple, Optional,
                    Set, TextIO, Tuple)

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


class Field(Enum):
    # Left corner
    LF = "LF"
    LN = "LN"

    # Spaces between rooms
    AB = "AB"
    BC = "BC"
    CD = "CD"

    # Right corner
    RN = "RN"
    RF = "RF"

    # Rooms
    AH = "AH"
    AL = "AL"

    BH = "BH"
    BL = "BL"

    CH = "CH"
    CL = "CL"

    DH = "DH"
    DL = "DL"


class Board(dict[Field, Optional[Amphipod]]):
    def __init__(self) -> None:
        super().__init__()
        for field in Field:
            self[field] = None

    @staticmethod
    def format_amphipod(amphipod: Optional[Amphipod]) -> str:
        return amphipod.value if amphipod is not None else " "

    def __repr__(self) -> str:
        f = self.format_amphipod

        return f"""#############
#{f(self[Field.LF])}{f(self[Field.LN])} {f(self[Field.AB])} {f(self[Field.BC])} {f(self[Field.CD])} {f(self[Field.RN])}{f(self[Field.RF])}#
###{f(self[Field.AH])}#{f(self[Field.BH])}#{f(self[Field.CH])}#{f(self[Field.DH])}###
  #{f(self[Field.AL])}#{f(self[Field.BL])}#{f(self[Field.CL])}#{f(self[Field.DL])}#
  #########"""

    def id(self) -> str:
        f = self.format_amphipod

        return (
            f"{f(self[Field.LF])}{f(self[Field.LN])}{f(self[Field.AB])}{f(self[Field.BC])}{f(self[Field.CD])}{f(self[Field.RN])}{f(self[Field.RF])}"
            f"{f(self[Field.AH])}{f(self[Field.BH])}{f(self[Field.CH])}{f(self[Field.DH])}"
            f"{f(self[Field.AL])}{f(self[Field.BL])}{f(self[Field.CL])}{f(self[Field.DL])}"
        )


def get_target_board() -> Board:
    board = Board()

    board[Field.AH] = Amphipod.AMBER
    board[Field.AL] = Amphipod.AMBER
    board[Field.BH] = Amphipod.BRONZE
    board[Field.BL] = Amphipod.BRONZE
    board[Field.CH] = Amphipod.COPPER
    board[Field.CL] = Amphipod.COPPER
    board[Field.DH] = Amphipod.DESERT
    board[Field.DL] = Amphipod.DESERT

    return board


TARGET_BOARD = get_target_board()


def read_board(input: TextIO) -> Board:
    text = input.read()
    match = PATTERN.match(text)
    assert match
    match_groups = match.groupdict()
    parsed_groups = {Field(key): Amphipod(value) for key, value in match_groups.items()}
    board = Board()
    board.update(parsed_groups)
    return board


DISTANCES: Dict[Tuple[Field, Field], int] = {
    # From A to parking
    (Field.AH, Field.LF): 3,
    (Field.AL, Field.LF): 4,
    (Field.AH, Field.LN): 2,
    (Field.AL, Field.LN): 3,
    (Field.AH, Field.AB): 2,
    (Field.AL, Field.AB): 3,
    (Field.AH, Field.BC): 4,
    (Field.AL, Field.BC): 5,
    (Field.AH, Field.CD): 6,
    (Field.AL, Field.CD): 7,
    (Field.AH, Field.RN): 8,
    (Field.AL, Field.RN): 9,
    (Field.AH, Field.RF): 9,
    (Field.AL, Field.RF): 10,
    # From A to rooms
    (Field.AH, Field.BH): 4,
    (Field.AL, Field.BH): 5,
    (Field.AH, Field.BL): 5,
    (Field.AL, Field.BL): 6,
    (Field.AH, Field.CH): 6,
    (Field.AL, Field.CH): 7,
    (Field.AH, Field.CL): 7,
    (Field.AL, Field.CL): 8,
    (Field.AH, Field.DH): 8,
    (Field.AL, Field.DH): 9,
    (Field.AH, Field.DL): 9,
    (Field.AL, Field.DL): 10,
    # From B to parking
    # From B to rooms
    # From C to parking
    # From C to rooms
    # From D to parking
    # From D to rooms
}
for (from_field, to_field), cost in DISTANCES.items():
    assert (to_field, from_field) not in DISTANCES
    DISTANCES[to_field, from_field] = cost
MOVE_COSTS: Dict[Amphipod, int] = {
    Amphipod.AMBER: 1,
    Amphipod.BRONZE: 10,
    Amphipod.COPPER: 100,
    Amphipod.DESERT: 1000,
}


def move(board: Board, from_field: Field, to_field: Field) -> Tuple[Board, int]:
    assert board[to_field] is None
    amphipod = board[from_field]
    assert amphipod is not None
    new_board = copy(board)
    new_board[to_field] = amphipod
    new_board[from_field] = None

    distance = DISTANCES[from_field, to_field]
    cost = MOVE_COSTS[amphipod]
    return new_board, distance * cost


def get_possible_lf_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    amphipod = board[Field.LF]
    if amphipod is None:
        return
    if amphipod == Amphipod.AMBER:
        if board[Field.AH] is None and board[Field.AL] is None:
            yield board.move(from_field=Field.LF, to_field=Field.AL), 4
    elif amphipod == Amphipod.BRONZE:
        pass
    elif amphipod == Amphipod.COPPER:
        pass
    else:
        assert amphipod == Amphipod.DESERT
        pass


def get_possible_ln_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_ab_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_bc_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_cd_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_rn_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_rf_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_ah_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_al_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_bh_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_bl_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_ch_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_cl_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_dh_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_dl_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    pass


def get_possible_moves(board: Board) -> Iterable[Tuple[Board, int]]:
    yield from get_possible_lf_moves(board)
    yield from get_possible_ln_moves(board)
    yield from get_possible_ab_moves(board)
    yield from get_possible_bc_moves(board)
    yield from get_possible_cd_moves(board)
    yield from get_possible_rn_moves(board)
    yield from get_possible_rf_moves(board)
    yield from get_possible_ah_moves(board)
    yield from get_possible_al_moves(board)
    yield from get_possible_bh_moves(board)
    yield from get_possible_bl_moves(board)
    yield from get_possible_ch_moves(board)
    yield from get_possible_cl_moves(board)
    yield from get_possible_dh_moves(board)
    yield from get_possible_dl_moves(board)


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
