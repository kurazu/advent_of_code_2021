from __future__ import annotations

import functools
import logging
import operator
import re
import sys
from copy import copy
from dataclasses import dataclass, field
from enum import Enum
from typing import (Any, Callable, DefaultDict, Dict, Iterable, List,
                    NamedTuple, Optional, Protocol, Set, TextIO, Tuple)

from returns.curry import partial

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


class Move(NamedTuple):
    from_field: Field
    to_field: Field


def get_distances() -> Dict[Move, int]:
    distances = {
        # From A to parking
        Move(Field.AH, Field.LF): 3,
        Move(Field.AL, Field.LF): 4,
        Move(Field.AH, Field.LN): 2,
        Move(Field.AL, Field.LN): 3,
        Move(Field.AH, Field.AB): 2,
        Move(Field.AL, Field.AB): 3,
        Move(Field.AH, Field.BC): 4,
        Move(Field.AL, Field.BC): 5,
        Move(Field.AH, Field.CD): 6,
        Move(Field.AL, Field.CD): 7,
        Move(Field.AH, Field.RN): 8,
        Move(Field.AL, Field.RN): 9,
        Move(Field.AH, Field.RF): 9,
        Move(Field.AL, Field.RF): 10,
        # From A to rooms
        Move(Field.AH, Field.BH): 4,
        Move(Field.AL, Field.BH): 5,
        Move(Field.AH, Field.BL): 5,
        Move(Field.AL, Field.BL): 6,
        Move(Field.AH, Field.CH): 6,
        Move(Field.AL, Field.CH): 7,
        Move(Field.AH, Field.CL): 7,
        Move(Field.AL, Field.CL): 8,
        Move(Field.AH, Field.DH): 8,
        Move(Field.AL, Field.DH): 9,
        Move(Field.AH, Field.DL): 9,
        Move(Field.AL, Field.DL): 10,
        # From B to parking
        Move(Field.BH, Field.LF): 5,
        Move(Field.BL, Field.LF): 6,
        Move(Field.BH, Field.LN): 4,
        Move(Field.BL, Field.LN): 5,
        Move(Field.BH, Field.AB): 2,
        Move(Field.BL, Field.AB): 3,
        Move(Field.BH, Field.BC): 2,
        Move(Field.BL, Field.BC): 3,
        Move(Field.BH, Field.CD): 4,
        Move(Field.BL, Field.CD): 5,
        Move(Field.BH, Field.RN): 6,
        Move(Field.BL, Field.RN): 7,
        Move(Field.BH, Field.RF): 7,
        Move(Field.BL, Field.RF): 9,
        # From B to rooms
        Move(Field.BH, Field.AH): 4,
        Move(Field.BL, Field.AH): 5,
        Move(Field.BH, Field.AL): 5,
        Move(Field.BL, Field.AL): 6,
        Move(Field.BH, Field.CH): 4,
        Move(Field.BL, Field.CH): 5,
        Move(Field.BH, Field.CL): 5,
        Move(Field.BL, Field.CL): 6,
        Move(Field.BH, Field.DH): 6,
        Move(Field.BL, Field.DH): 7,
        Move(Field.BH, Field.DL): 7,
        Move(Field.BL, Field.DL): 8,
        # From C to parking
        Move(Field.CH, Field.LF): 7,
        Move(Field.CL, Field.LF): 8,
        Move(Field.CH, Field.LN): 6,
        Move(Field.CL, Field.LN): 7,
        Move(Field.CH, Field.AB): 4,
        Move(Field.CL, Field.AB): 5,
        Move(Field.CH, Field.BC): 2,
        Move(Field.CL, Field.BC): 3,
        Move(Field.CH, Field.CD): 2,
        Move(Field.CL, Field.CD): 3,
        Move(Field.CH, Field.RN): 4,
        Move(Field.CL, Field.RN): 5,
        Move(Field.CH, Field.RF): 5,
        Move(Field.CL, Field.RF): 6,
        # From C to rooms
        Move(Field.CH, Field.AH): 6,
        Move(Field.CL, Field.AH): 7,
        Move(Field.CH, Field.AL): 7,
        Move(Field.CL, Field.AL): 8,
        Move(Field.CH, Field.BH): 4,
        Move(Field.CL, Field.BH): 5,
        Move(Field.CH, Field.BL): 5,
        Move(Field.CL, Field.BL): 6,
        Move(Field.CH, Field.DH): 4,
        Move(Field.CL, Field.DH): 5,
        Move(Field.CH, Field.DL): 5,
        Move(Field.CL, Field.DL): 6,
        # From D to parking
        Move(Field.DH, Field.LF): 9,
        Move(Field.DL, Field.LF): 10,
        Move(Field.DH, Field.LN): 8,
        Move(Field.DL, Field.LN): 9,
        Move(Field.DH, Field.AB): 6,
        Move(Field.DL, Field.AB): 7,
        Move(Field.DH, Field.BC): 4,
        Move(Field.DL, Field.BC): 5,
        Move(Field.DH, Field.CD): 2,
        Move(Field.DL, Field.CD): 3,
        Move(Field.DH, Field.RN): 2,
        Move(Field.DL, Field.RN): 3,
        Move(Field.DH, Field.RF): 3,
        Move(Field.DL, Field.RF): 4,
        # From D to rooms
        Move(Field.DH, Field.AH): 8,
        Move(Field.DL, Field.AH): 9,
        Move(Field.DH, Field.AL): 9,
        Move(Field.DL, Field.AL): 10,
        Move(Field.DH, Field.BH): 6,
        Move(Field.DL, Field.BH): 7,
        Move(Field.DH, Field.BL): 7,
        Move(Field.DL, Field.BL): 8,
        Move(Field.DH, Field.CH): 4,
        Move(Field.DL, Field.CH): 5,
        Move(Field.DH, Field.CL): 5,
        Move(Field.DL, Field.CL): 6,
    }
    extra: Dict[Move, int] = {}
    for (from_field, to_field), cost in distances.items():
        key = Move(to_field, from_field)
        if key in distances:
            assert distances[key] == cost
        else:
            extra[key] = cost

    return {**distances, **extra}


DISTANCES = get_distances()


MOVE_COSTS: Dict[Amphipod, int] = {
    Amphipod.AMBER: 1,
    Amphipod.BRONZE: 10,
    Amphipod.COPPER: 100,
    Amphipod.DESERT: 1000,
}


def validate_move(board: Board, move: Move) -> Amphipod:
    from_field, to_field = move
    assert board[to_field] is None
    amphipod = board[from_field]
    assert amphipod is not None

    return amphipod


def get_move_energy(board: Board, move: Move) -> int:
    amphipod = validate_move(board, move)

    distance = DISTANCES[move]
    cost = MOVE_COSTS[amphipod]
    return distance * cost


def move(board: Board, move: Move) -> Board:
    amphipod = validate_move(board, move)
    from_field, to_field = move

    new_board = copy(board)
    new_board[to_field] = amphipod
    new_board[from_field] = None

    return new_board


@dataclass
class move_producer:
    source_field: Field

    def __call__(
        self, callback: Callable[[Board, Field, Amphipod], Iterable[Move]]
    ) -> Callable[[Board], Iterable[Move]]:
        @functools.wraps(callback)
        def move_producer_wrapper(board: Board) -> Iterable[Move]:
            amphipod = board[self.source_field]
            if amphipod is None:
                return  # there is no amphipod here
            yield from callback(board, self.source_field, amphipod)

        return move_producer_wrapper


def get_possible_a_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    if amphipod == Amphipod.AMBER:
        if board[Field.AH] is None and board[Field.AL] is None:
            yield Move(from_field=source_field, to_field=Field.AL)
        elif board[Field.AL] == Amphipod.AMBER and board[Field.AH] is None:
            yield Move(from_field=source_field, to_field=Field.AH)


def get_possible_b_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    if amphipod == Amphipod.BRONZE:
        if board[Field.BH] is None and board[Field.BL] is None:
            yield Move(from_field=source_field, to_field=Field.BL)
        elif board[Field.BL] == Amphipod.BRONZE and board[Field.BH] is None:
            yield Move(from_field=source_field, to_field=Field.BH)


def get_possible_c_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    if amphipod == Amphipod.COPPER:
        if board[Field.CH] is None and board[Field.CL] is None:
            yield Move(from_field=source_field, to_field=Field.CL)
        elif board[Field.CL] == Amphipod.COPPER and board[Field.CH] is None:
            yield Move(from_field=source_field, to_field=Field.CH)


def get_possible_d_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    if amphipod == Amphipod.DESERT:
        if board[Field.DH] is None and board[Field.DL] is None:
            yield Move(from_field=source_field, to_field=Field.DL)
        elif board[Field.DL] == Amphipod.DESERT and board[Field.DH] is None:
            yield Move(from_field=source_field, to_field=Field.DH)


def get_possible_lx_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    yield from get_possible_a_moves(board, source_field, amphipod)

    if board[Field.AB] is not None:
        return  # Blocked

    yield from get_possible_b_moves(board, source_field, amphipod)

    if board[Field.BC] is not None:
        return  # blocked

    yield from get_possible_c_moves(board, source_field, amphipod)

    if board[Field.CD] is not None:
        return  # blocked

    yield from get_possible_d_moves(board, source_field, amphipod)


@move_producer(Field.LF)
def get_possible_lf_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    if board[Field.LN] is not None:
        return  # blocked
    yield from get_possible_lx_moves(board, source_field, amphipod)


@move_producer(Field.LN)
def get_possible_ln_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    yield from get_possible_lx_moves(board, source_field, amphipod)


def get_possible_rx_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    yield from get_possible_d_moves(board, source_field, amphipod)

    if board[Field.CD] is not None:
        return  # blocked

    yield from get_possible_c_moves(board, source_field, amphipod)

    if board[Field.BC] is not None:
        return  # blocked

    yield from get_possible_b_moves(board, source_field, amphipod)

    if board[Field.AB] is not None:
        return  # Blocked

    yield from get_possible_a_moves(board, source_field, amphipod)


@move_producer(Field.RF)
def get_possible_rf_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    if board[Field.RN] is not None:
        return  # Blocked
    yield from get_possible_rx_moves(board, source_field, amphipod)


@move_producer(Field.RN)
def get_possible_rn_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    yield from get_possible_rx_moves(board, source_field, amphipod)


@move_producer(Field.AB)
def get_possible_ab_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    yield from get_possible_a_moves(board, source_field, amphipod)
    yield from get_possible_b_moves(board, source_field, amphipod)

    if board[Field.BC] is not None:
        return  # blocked

    yield from get_possible_c_moves(board, source_field, amphipod)

    if board[Field.CD] is not None:
        return  # blocked

    yield from get_possible_d_moves(board, source_field, amphipod)


@move_producer(Field.BC)
def get_possible_bc_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    yield from get_possible_b_moves(board, source_field, amphipod)
    yield from get_possible_c_moves(board, source_field, amphipod)

    if board[Field.CD] is None:
        yield from get_possible_d_moves(board, source_field, amphipod)

    if board[Field.AB] is None:
        yield from get_possible_a_moves(board, source_field, amphipod)


@move_producer(Field.CD)
def get_possible_cd_moves(
    board: Board, source_field: Field, amphipod: Amphipod
) -> Iterable[Move]:
    yield from get_possible_c_moves(board, source_field, amphipod)
    yield from get_possible_d_moves(board, source_field, amphipod)

    if board[Field.BC] is not None:
        return  # blocked

    yield from get_possible_b_moves(board, source_field, amphipod)

    if board[Field.AB] is not None:
        return  # blocked

    yield from get_possible_a_moves(board, source_field, amphipod)


def get_possible_blocking_moves(
    board: Board,
    source_field: Field,
    target_field: Field,
    possible_obstacles: Set[Field] = set(),
) -> Iterable[Move]:
    if board[target_field] is not None:
        return  # something is at the target
    for obstacle_field in possible_obstacles:
        if board[obstacle_field] is not None:
            return  # something is blocking the way
    yield Move(source_field, target_field)


class GetMovesCallback(Protocol):
    def __call__(
        self, target_field: Field, possible_obstacles: Set[Field] = set()
    ) -> Iterable[Move]:
        ...


def blocking_moves_producer(
    callback: Callable[[Board, Field, Amphipod, GetMovesCallback], Iterable[Move]],
) -> Callable[[Board, Field, Amphipod], Iterable[Move]]:
    @functools.wraps(callback)
    def blocking_moves_producer_wrapper(
        board: Board, source_field: Field, amphipod: Amphipod
    ) -> Iterable[Move]:
        get_moves = partial(get_possible_blocking_moves, board, source_field)
        yield from callback(board, source_field, amphipod, get_moves)

    return blocking_moves_producer_wrapper


# We don't need to consider moves room -> other room, becuase they can always
# be experessed as room -> middle parking -> other room
# thus the transition taking same energy cost, but in two moves.


@move_producer(Field.AH)
@blocking_moves_producer
def get_possible_ah_moves(
    board: Board, source_field: Field, amphipod: Amphipod, get_moves: GetMovesCallback
) -> Iterable[Move]:
    if amphipod == Amphipod.AMBER and board[Field.AL] == Amphipod.AMBER:
        return  # already where we are supposed to be
    yield from get_moves(Field.LF, {Field.LN})
    yield from get_moves(Field.LN)
    yield from get_moves(Field.AB)
    yield from get_moves(Field.BC, {Field.AB})
    yield from get_moves(Field.CD, {Field.BC, Field.AB})
    yield from get_moves(Field.RN, {Field.CD, Field.BC, Field.AB})
    yield from get_moves(Field.RF, {Field.RN, Field.CD, Field.BC, Field.AB})


@move_producer(Field.AL)
@blocking_moves_producer
def get_possible_al_moves(
    board: Board, source_field: Field, amphipod: Amphipod, get_moves: GetMovesCallback
) -> Iterable[Move]:
    if amphipod == Amphipod.AMBER:
        return  # we are already where we are supposed to be
    yield from get_moves(Field.LF, {Field.LN, Field.AH})
    yield from get_moves(Field.LN, {Field.AH})
    yield from get_moves(Field.AB, {Field.AH})
    yield from get_moves(Field.BC, {Field.AB, Field.AH})
    yield from get_moves(Field.CD, {Field.BC, Field.AB, Field.AH})
    yield from get_moves(Field.RN, {Field.CD, Field.BC, Field.AB, Field.AH})
    yield from get_moves(Field.RF, {Field.RN, Field.CD, Field.BC, Field.AB, Field.AH})


@move_producer(Field.BH)
@blocking_moves_producer
def get_possible_bh_moves(
    board: Board, source_field: Field, amphipod: Amphipod, get_moves: GetMovesCallback
) -> Iterable[Move]:
    if amphipod == Amphipod.BRONZE and board[Field.BL] == Amphipod.BRONZE:
        return  # already where we are supposed to be
    yield from get_moves(Field.LF, {Field.LN, Field.AB})
    yield from get_moves(Field.LN, {Field.AB})
    yield from get_moves(Field.AB)
    yield from get_moves(Field.BC)
    yield from get_moves(Field.CD, {Field.BC})
    yield from get_moves(Field.RN, {Field.CD, Field.BC})
    yield from get_moves(Field.RF, {Field.RN, Field.CD, Field.BC})


@move_producer(Field.BL)
@blocking_moves_producer
def get_possible_bl_moves(
    board: Board, source_field: Field, amphipod: Amphipod, get_moves: GetMovesCallback
) -> Iterable[Move]:
    if amphipod == Amphipod.BRONZE:
        return  # we are already where we are supposed to be
    yield from get_moves(Field.LF, {Field.LN, Field.AB, Field.BH})
    yield from get_moves(Field.LN, {Field.AB, Field.BH})
    yield from get_moves(Field.AB, {Field.BH})
    yield from get_moves(Field.BC, {Field.BH})
    yield from get_moves(Field.CD, {Field.BC, Field.BH})
    yield from get_moves(Field.RN, {Field.CD, Field.BC, Field.BH})
    yield from get_moves(Field.RF, {Field.RN, Field.CD, Field.BC, Field.BH})


@move_producer(Field.CH)
@blocking_moves_producer
def get_possible_ch_moves(
    board: Board, source_field: Field, amphipod: Amphipod, get_moves: GetMovesCallback
) -> Iterable[Move]:
    if amphipod == Amphipod.COPPER and board[Field.CL] == Amphipod.COPPER:
        return  # already where we are supposed to be
    yield from get_moves(Field.LF, {Field.LN, Field.BC, Field.AB})
    yield from get_moves(Field.LN, {Field.BC, Field.AB})
    yield from get_moves(Field.AB, {Field.BC})
    yield from get_moves(Field.BC)
    yield from get_moves(Field.CD)
    yield from get_moves(Field.RN, {Field.CD})
    yield from get_moves(Field.RF, {Field.RN, Field.CD})


@move_producer(Field.CL)
@blocking_moves_producer
def get_possible_cl_moves(
    board: Board, source_field: Field, amphipod: Amphipod, get_moves: GetMovesCallback
) -> Iterable[Move]:
    if amphipod == Amphipod.COPPER:
        return  # we are already where we are supposed to be
    yield from get_moves(Field.LF, {Field.LN, Field.BC, Field.AB, Field.CH})
    yield from get_moves(Field.LN, {Field.BC, Field.AB, Field.CH})
    yield from get_moves(Field.AB, {Field.BC, Field.CH})
    yield from get_moves(Field.BC, {Field.CH})
    yield from get_moves(Field.CD, {Field.CH})
    yield from get_moves(Field.RN, {Field.CD, Field.CH})
    yield from get_moves(Field.RF, {Field.RN, Field.CD, Field.CH})


@move_producer(Field.DH)
@blocking_moves_producer
def get_possible_dh_moves(
    board: Board, source_field: Field, amphipod: Amphipod, get_moves: GetMovesCallback
) -> Iterable[Move]:
    if amphipod == Amphipod.DESERT and board[Field.DL] == Amphipod.DESERT:
        return  # already where we are supposed to be
    yield from get_moves(Field.LF, {Field.LN, Field.CD, Field.BC, Field.AB})
    yield from get_moves(Field.LN, {Field.CD, Field.BC, Field.AB})
    yield from get_moves(Field.AB, {Field.CD, Field.BC})
    yield from get_moves(Field.BC, {Field.CD})
    yield from get_moves(Field.CD)
    yield from get_moves(Field.RN)
    yield from get_moves(Field.RF, {Field.RN})


@move_producer(Field.DL)
@blocking_moves_producer
def get_possible_dl_moves(
    board: Board, source_field: Field, amphipod: Amphipod, get_moves: GetMovesCallback
) -> Iterable[Move]:
    if amphipod == Amphipod.DESERT:
        return  # we are already where we are supposed to be
    yield from get_moves(Field.LF, {Field.LN, Field.CD, Field.BC, Field.AB, Field.DH})
    yield from get_moves(Field.LN, {Field.CD, Field.BC, Field.AB, Field.DH})
    yield from get_moves(Field.AB, {Field.CD, Field.BC, Field.DH})
    yield from get_moves(Field.BC, {Field.CD, Field.DH})
    yield from get_moves(Field.CD, {Field.DH})
    yield from get_moves(Field.RN, {Field.DH})
    yield from get_moves(Field.RF, {Field.RN, Field.DH})


def get_possible_moves(board: Board) -> Iterable[Move]:
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


@dataclass
class DFSSearcher:
    best_energy: float = float("inf")
    boards_seen: Set[str] = field(default_factory=set)

    def register_state_seen(self, board: Board) -> None:
        self.boards_seen.add(board.id())

    def is_terminal(self, board: Board) -> bool:
        return board == TARGET_BOARD

    def handle_terminal_stage(
        self, current_moves: List[Move], current_energy: int
    ) -> Tuple[List[Move], int]:
        if current_energy < self.best_energy:
            logger.debug("Found best terminal state with energy %d", current_energy)
            self.best_energy = current_energy
        else:
            logger.debug("Garbage terminal state %d", current_energy)
        return current_moves, current_energy

    def __call__(
        self, current_board: Board, current_moves: List[Move], current_energy: int
    ) -> Optional[Tuple[List[Move], int]]:
        self.register_state_seen(current_board)

        if self.is_terminal(current_board):
            return self.handle_terminal_stage(current_moves, current_energy)
        else:
            return self.handle_nonterminal_stage(
                current_board, current_moves, current_energy
            )

    def get_prioritized_possible_moves(
        self, board: Board
    ) -> Iterable[Tuple[Move, int]]:
        possibilities = [
            (possible_move, get_move_energy(board, possible_move))
            for possible_move in get_possible_moves(board)
        ]

        # Explore the state space based on current move cost heuristic
        possibilities.sort(key=operator.itemgetter(1))
        return possibilities

    def is_move_not_hopeless(
        self, move_energy: Tuple[Move, int], current_energy: int
    ) -> bool:
        move, energy = move_energy
        return current_energy + energy < self.best_energy

    def prune_hopeless_moves(
        self, possible_moves: Iterable[Tuple[Move, int]], current_energy: int
    ) -> Iterable[Tuple[Move, int]]:
        return filter(
            partial(self.is_move_not_hopeless, current_energy=current_energy),
            possible_moves,
        )

    def explore_moves(
        self,
        current_board: Board,
        current_moves: List[Move],
        current_energy: int,
        possibile_moves: Iterable[Tuple[Move, int]],
    ) -> List[Tuple[List[Move], int]]:
        results: List[Tuple[List[Move], int]] = []
        for possible_move, move_energy in possibile_moves:
            possible_board = move(current_board, possible_move)
            possible_board_id = possible_board.id()

            if possible_board_id in self.boards_seen:
                # logger.debug("Target state already visited")
                continue  # We've seen this state
            # State to explore
            result = self(
                possible_board,
                current_moves + [possible_move],
                current_energy + move_energy,
            )
            if result is None:
                continue

            results.append(result)

        return results

    def choose_best_result(
        self, results: List[Tuple[List[Move], int]]
    ) -> Optional[Tuple[List[Move], int]]:
        if not results:
            return None
        else:
            results.sort(key=operator.itemgetter(1))
            best_result, *_ = results
            return best_result

    def handle_nonterminal_stage(
        self, current_board: Board, current_moves: List[Move], current_energy: int
    ) -> Optional[Tuple[List[Move], int]]:
        possible_moves = self.get_prioritized_possible_moves(current_board)
        moves_to_consider = self.prune_hopeless_moves(possible_moves, current_energy)
        results = self.explore_moves(
            current_board, current_moves, current_energy, moves_to_consider
        )
        return self.choose_best_result(results)


def dfs(starting_board: Board) -> Tuple[List[Move], int]:
    searcher = DFSSearcher()
    result = searcher(starting_board, [], 0)
    assert result is not None
    return result


def _dfs(starting_board: Board) -> Tuple[List[Move], int]:
    best_energy = float("inf")
    boards_seen: Set[str] = set()

    def recursive_search(
        current_board: Board, moves: List[Move], stack_energy: int
    ) -> Optional[Tuple[List[Move], int]]:
        nonlocal best_energy

        tabs = " " * len(moves)

        def log(msg: str, *args: Any) -> None:
            formatted_message = f"{tabs} {msg}"
            logger.debug(formatted_message, *args)

        boards_seen.add(current_board.id())  # might be too memory intensive
        if current_board == TARGET_BOARD:
            # Terminal state
            if stack_energy < best_energy:
                log("Found best terminal state with energy %d", stack_energy)
                best_energy = stack_energy
            else:
                log("Garbage terminal state %d", stack_energy)
            return moves, stack_energy
        else:
            possibilities: List[Tuple[Move, int]] = []
            for possible_move in get_possible_moves(current_board):
                move_energy = get_move_energy(current_board, possible_move)
                if stack_energy + move_energy >= best_energy:
                    log("Unpromising move %d + %d pruned", stack_energy, move_energy)
                    continue  # This state is already worse than the current best
                possibilities.append((possible_move, move_energy))
            # Explore the state space based on current move cost heuristic
            possibilities.sort(key=operator.itemgetter(1))
            log("Found %d possible moves", len(possibilities))
            result_possibilities: List[Tuple[List[Move], int]] = []
            for possible_move, move_energy in possibilities:
                possible_board = move(current_board, possible_move)
                possible_board_id = possible_board.id()

                if possible_board_id in boards_seen:
                    log("Target state already visited")
                    continue  # We've seen this state
                else:  # State to explore
                    recursive_result = recursive_search(
                        possible_board,
                        moves + [possible_move],
                        stack_energy + move_energy,
                    )
                    if recursive_result is None:
                        log("Move brings no conculusions")
                        continue
                    else:
                        result_possibilities.append(recursive_result)
            log("Processed %d results", len(result_possibilities))
            if not result_possibilities:
                log("No result possibilities found")
                return None  # No valid moves from here
            else:
                result_possibilities.sort(key=operator.itemgetter(1))
                return result_possibilities[0]

    best_result = recursive_search(starting_board, [], 0)
    assert best_result is not None
    logger.debug(
        "Found best result with energy %d after visiting %d states",
        best_result[1],
        len(boards_seen),
    )
    return best_result


def main(input: TextIO) -> str:
    starting_board = read_board(input)
    moves, energy = _dfs(starting_board)
    logger.info("Best solution with %d moves and energy %d", len(moves), energy)
    board = starting_board
    for best_move in moves:
        from_field, to_field = best_move
        amphipod = board[from_field]
        assert amphipod is not None
        logger.info(
            "Step: %s %s -> %s", amphipod.name, from_field.value, to_field.value
        )
        board = move(board, best_move)
        logger.info("\n%r", board)
    return f"{energy}"


if __name__ == "__main__":
    sys.setrecursionlimit(sys.getrecursionlimit() * 10)
    run_with_file_argument(main)
