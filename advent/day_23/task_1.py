from __future__ import annotations

import logging
import multiprocessing
import random
import sys
from enum import Enum
from typing import Any, Callable, Dict, Iterable, List, Optional, TextIO, Tuple

from returns.curry import partial

from ..cli import run_with_file_argument
from .dfs import dfs
from .dfs2 import dfs as dfs2
from .enums import Amphipod
from .input_parsing import read_board
from .map import (FieldType, MoveType, PossibleMove, format_amphipod,
                  get_blank_board, get_possible_moves, get_target_board,
                  is_allowed_move, move)

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
    AL = "AL"

    BH = "BH"
    BL = "BL"

    CH = "CH"
    CL = "CL"

    DH = "DH"
    DL = "DL"


IDType = str


def get_board_id(
    nodes: Iterable[FieldType], board: Dict[FieldType, Optional[Amphipod]]
) -> IDType:
    return "".join(format_amphipod(board[node]) for node in nodes)


def format_board(board: Dict[Field, Optional[Amphipod]]) -> str:
    f = format_amphipod

    return f"""#############
#{f(board[Field.LF])}{f(board[Field.LN])} {f(board[Field.AB])} {f(board[Field.BC])} {f(board[Field.CD])} {f(board[Field.RN])}{f(board[Field.RF])}#
###{f(board[Field.AH])}#{f(board[Field.BH])}#{f(board[Field.CH])}#{f(board[Field.DH])}###
  #{f(board[Field.AL])}#{f(board[Field.BL])}#{f(board[Field.CL])}#{f(board[Field.DL])}#
  #########"""


def run_dfs(
    starting_board: Dict[FieldType, Optional[Amphipod]],
    target_board: Dict[FieldType, Optional[Amphipod]],
    possible_moves: List[PossibleMove[FieldType]],
    board_hasher: Callable[[Dict[FieldType, Optional[Amphipod]]], IDType],
    _: Any,
) -> Tuple[List[PossibleMove[FieldType]], int]:
    random.shuffle(possible_moves)
    return dfs2(
        starting_board=starting_board,
        target_board=target_board,
        possible_moves=possible_moves,
        board_hasher=board_hasher,
    )


def main(input: TextIO) -> str:
    blank_board = get_blank_board(Field)

    input_board = {Field(key): amphipod for key, amphipod in read_board(input).items()}
    starting_board: Dict[Field, Optional[Amphipod]] = {**blank_board, **input_board}
    rooms = {
        Amphipod.AMBER: {Field.AH, Field.AL},
        Amphipod.BRONZE: {Field.BH, Field.BL},
        Amphipod.COPPER: {Field.CH, Field.CL},
        Amphipod.DESERT: {Field.DH, Field.DL},
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
            (Field.AH, Field.AL),
            (Field.AX, Field.AB),
            (Field.AB, Field.BX),
            (Field.BX, Field.BH),
            (Field.BH, Field.BL),
            (Field.BX, Field.BC),
            (Field.BC, Field.CX),
            (Field.CX, Field.CH),
            (Field.CH, Field.CL),
            (Field.CX, Field.CD),
            (Field.CD, Field.DX),
            (Field.DX, Field.DH),
            (Field.DH, Field.DL),
            (Field.DX, Field.RN),
            (Field.RN, Field.RF),
        ],
        rooms=rooms,
        hallway={Field.LF, Field.LN, Field.AB, Field.BC, Field.CD, Field.RN, Field.RF},
    )
    board_hasher = partial(get_board_id, Field)
    logger.info("Found %d possible moves", len(possible_moves))

    moves, energy = dfs2(
        starting_board=starting_board,
        target_board=target_board,
        possible_moves=possible_moves,
        board_hasher=board_hasher,
    )
    # tries = 5
    # with multiprocessing.Pool() as pool:
    #     results = pool.map(
    #         partial(
    #             run_dfs,
    #             starting_board,
    #             target_board,
    #             possible_moves,
    #             board_hasher,
    #         ),
    #         range(tries),
    #     )

    # for moves, energy in results:
    logger.info("Best solution with %d moves and energy %d", len(moves), energy)
    board = starting_board
    # logger.info("Starting board\n%s", format_board(board))
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
        # logger.info("Board\n%s", format_board(board))
    return f"{energy}"


if __name__ == "__main__":
    sys.setrecursionlimit(sys.getrecursionlimit() * 10)
    run_with_file_argument(main)
