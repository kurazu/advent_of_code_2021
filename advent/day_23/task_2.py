from __future__ import annotations

import logging
import sys
from enum import Enum
from typing import Dict, Optional, TextIO

from ..cli import run_with_file_argument
from .enums import Amphipod
from .map import get_possible_moves
from .task_1 import (dfs, format_amphipod, get_blank_board, get_target_board,
                     move, read_board)

logger = logging.getLogger(__name__)


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

    # Connectors
    AX = "AX"
    BX = "BX"
    CX = "CX"
    DX = "DX"

    # Rooms
    AH = "AH"
    A1 = "A1"
    A2 = "A2"
    AL = "AL"

    BH = "BH"
    B1 = "B1"
    B2 = "B2"
    BL = "BL"

    CH = "CH"
    C1 = "C1"
    C2 = "C2"
    CL = "CL"

    DH = "DH"
    D1 = "D1"
    D2 = "D2"
    DL = "DL"


def format_board(board: Dict[Field, Optional[Amphipod]]) -> str:
    f = format_amphipod

    return f"""#############
#{f(board[Field.LF])}{f(board[Field.LN])} {f(board[Field.AB])} {f(board[Field.BC])} {f(board[Field.CD])} {f(board[Field.RN])}{f(board[Field.RF])}#
###{f(board[Field.AH])}#{f(board[Field.BH])}#{f(board[Field.CH])}#{f(board[Field.DH])}###
  #{f(board[Field.A1])}#{f(board[Field.B1])}#{f(board[Field.C1])}#{f(board[Field.D1])}#
  #{f(board[Field.A2])}#{f(board[Field.B2])}#{f(board[Field.C2])}#{f(board[Field.D2])}#
  #{f(board[Field.AL])}#{f(board[Field.BL])}#{f(board[Field.CL])}#{f(board[Field.DL])}#
  #########"""


def main(input: TextIO) -> str:
    blank_board = get_blank_board(Field)

    input_board = {Field(key): amphipod for key, amphipod in read_board(input).items()}
    hidden_board = {
        Field.A1: Amphipod.DESERT,
        Field.B1: Amphipod.COPPER,
        Field.C1: Amphipod.BRONZE,
        Field.C2: Amphipod.AMBER,
        Field.A2: Amphipod.DESERT,
        Field.B2: Amphipod.BRONZE,
        Field.C2: Amphipod.AMBER,
        Field.D2: Amphipod.COPPER,
    }
    starting_board: Dict[Field, Optional[Amphipod]] = {
        **blank_board,
        **input_board,
        **hidden_board,
    }
    rooms = {
        Amphipod.AMBER: {Field.AH, Field.AL, Field.A1, Field.A2},
        Amphipod.BRONZE: {Field.BH, Field.BL, Field.B1, Field.B2},
        Amphipod.COPPER: {Field.CH, Field.CL, Field.C1, Field.C2},
        Amphipod.DESERT: {Field.DH, Field.DL, Field.D1, Field.D2},
    }
    target_board: Dict[Field, Optional[Amphipod]] = {
        **blank_board,
        **get_target_board(rooms),
    }
    possible_moves = get_possible_moves(
        nodes=Field,
        edges=[
            (Field.LF, Field.LN),
            (Field.LN, Field.AX),
            (Field.AX, Field.AH),
            (Field.AH, Field.A1),
            (Field.A1, Field.A2),
            (Field.A2, Field.AL),
            (Field.AX, Field.AB),
            (Field.AB, Field.BX),
            (Field.BX, Field.BH),
            (Field.BH, Field.B1),
            (Field.B1, Field.B2),
            (Field.B2, Field.BL),
            (Field.BX, Field.BC),
            (Field.BC, Field.CX),
            (Field.CX, Field.CH),
            (Field.CH, Field.C1),
            (Field.C1, Field.C2),
            (Field.C2, Field.CL),
            (Field.CX, Field.CD),
            (Field.CD, Field.DX),
            (Field.DX, Field.DH),
            (Field.DH, Field.D1),
            (Field.D1, Field.D2),
            (Field.D2, Field.DL),
            (Field.DX, Field.RN),
            (Field.RN, Field.RF),
        ],
        rooms=rooms,
        hallway={Field.LF, Field.LN, Field.AB, Field.BC, Field.CD, Field.RN, Field.RF},
    )
    logger.info("Found %d possible moves", len(possible_moves))
    moves, energy = dfs(
        nodes=Field,
        starting_board=starting_board,
        target_board=target_board,
        possible_moves=possible_moves,
    )
    logger.info("Best solution with %d moves and energy %d", len(moves), energy)
    board = starting_board
    logger.info("Starting board\n%s", format_board(board))
    for best_move in moves:
        amphipod = board[best_move.from_field]
        assert amphipod is not None
        logger.info(
            "Step: %s %s -> %s",
            amphipod.name,
            best_move.from_field.value,
            best_move.to_field.value,
        )
        board = move(board, best_move)
        logger.info("Board\n%s", format_board(board))
    return f"{energy}"


if __name__ == "__main__":
    sys.setrecursionlimit(sys.getrecursionlimit() * 100)
    run_with_file_argument(main)
