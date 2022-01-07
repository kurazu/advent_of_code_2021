from __future__ import annotations

import logging
import operator
import re
import sys
from enum import Enum
from typing import Dict, Iterable, List, Optional, Set, TextIO, Tuple

from returns.curry import partial

from ..cli import run_with_file_argument
from .enums import Amphipod
from .map import FieldType, PossibleMove, get_possible_moves

logger = logging.getLogger(__name__)


PATTERN = re.compile(
    r"^\#\#\#\#\#\#\#\#\#\#\#\#\#\n"
    r"\#\.\.\.\.\.\.\.\.\.\.\.\#\n"
    r"\#\#\#(?P<AH>[A-D])\#(?P<BH>[A-D])\#(?P<CH>[A-D])\#(?P<DH>[A-D])\#\#\#\n"
    r"\s\s\#(?P<AL>[A-D])\#(?P<BL>[A-D])\#(?P<CL>[A-D])\#(?P<DL>[A-D])\#\n"
    r"\s\s\#\#\#\#\#\#\#\#\#$"
)


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


def format_amphipod(amphipod: Optional[Amphipod]) -> str:
    return amphipod.value if amphipod is not None else " "


def read_board(input: TextIO) -> Dict[str, Optional[Amphipod]]:
    text = input.read()
    match = PATTERN.match(text)
    assert match
    match_groups = match.groupdict()
    return {key: Amphipod(value) for key, value in match_groups.items()}


MOVE_COSTS: Dict[Amphipod, int] = {
    Amphipod.AMBER: 1,
    Amphipod.BRONZE: 10,
    Amphipod.COPPER: 100,
    Amphipod.DESERT: 1000,
}


def get_move_energy(
    board: Dict[FieldType, Optional[Amphipod]], move: PossibleMove[FieldType]
) -> int:
    amphipod = board[move.from_field]
    assert amphipod is not None

    distance = move.distance
    cost = MOVE_COSTS[amphipod]
    return distance * cost


def move(
    board: Dict[FieldType, Optional[Amphipod]], move: PossibleMove[FieldType]
) -> Dict[FieldType, Optional[Amphipod]]:
    return {**board, move.to_field: board[move.from_field], move.from_field: None}


def is_allowed_move(
    board: Dict[FieldType, Optional[Amphipod]], possible_move: PossibleMove[FieldType]
) -> bool:
    amphipod = board[possible_move.from_field]
    if amphipod is None:
        # move cannot be made because there is no creature at the start point
        return False
    if board[possible_move.to_field] is not None:
        # move cannot be made because there is a creature at the end point
        return False
    if any(
        board[through_field] is not None
        for through_field in possible_move.through_fields
    ):
        # move cannot be made because there is a creature blocking the way
        return False
    required_amphipod = possible_move.required_amphipod
    if required_amphipod is not None:
        if amphipod != required_amphipod:
            # wrong type of amphipod cannot make the move
            return False
        if any(
            board[neighbour_field] != required_amphipod
            for neighbour_field in possible_move.required_same_type_neighbours
        ):
            # move cannot be made because neighbours are not present yet
            return False

    return True


def get_allowed_moves(
    board: Dict[FieldType, Optional[Amphipod]],
    possible_moves: List[PossibleMove[FieldType]],
) -> Iterable[PossibleMove[FieldType]]:
    return filter(partial(is_allowed_move, board), possible_moves)


def get_board_id(
    nodes: Iterable[FieldType], board: Dict[FieldType, Optional[Amphipod]]
) -> str:
    return "".join(format_amphipod(board[node]) for node in nodes)


def dfs(
    *,
    nodes: Iterable[FieldType],
    starting_board: Dict[FieldType, Optional[Amphipod]],
    target_board: Dict[FieldType, Optional[Amphipod]],
    possible_moves: List[PossibleMove[FieldType]],
) -> Tuple[List[PossibleMove[FieldType]], int]:
    best_energy = float("inf")
    cache: Dict[str, Optional[Tuple[List[PossibleMove[FieldType]], int]]] = {}

    def recursive_search(
        boards_seen: Set[str],
        current_board: Dict[FieldType, Optional[Amphipod]],
        current_energy: int,
    ) -> Optional[Tuple[List[PossibleMove[FieldType]], int]]:
        nonlocal best_energy

        current_board_id = get_board_id(nodes, current_board)
        if current_board_id in cache:
            return cache[current_board_id]
        if current_board == target_board:
            logger.debug("Found terminal state")
            # Terminal state
            if current_energy < best_energy:
                best_energy = current_energy
            # No more effort needed
            return [], 0
        else:
            allowed_moves = get_allowed_moves(current_board, possible_moves)
            moves_with_energy = (
                (allowed_move, get_move_energy(current_board, allowed_move))
                for allowed_move in allowed_moves
            )
            promising_moves = (
                (possible_move, move_energy)
                for possible_move, move_energy in moves_with_energy
                if current_energy + move_energy < best_energy
            )
            # Explore the state space based on current move cost heuristic
            possibilities = sorted(promising_moves, key=operator.itemgetter(1))

            result_possibilities: List[Tuple[List[PossibleMove[FieldType]], int]] = []
            for possible_move, move_energy in possibilities:
                possible_board = move(current_board, possible_move)
                possible_board_id = get_board_id(nodes, possible_board)

                if possible_board_id in boards_seen:
                    continue  # We've been to this state
                else:  # State to explore
                    recursive_result = recursive_search(
                        boards_seen | {current_board_id},
                        possible_board,
                        current_energy + move_energy,
                    )
                    if recursive_result is None:
                        continue
                    else:
                        recursive_moves, recursive_energy = recursive_result
                        result_possibilities.append(
                            (
                                [possible_move] + recursive_moves,
                                move_energy + recursive_energy,
                            )
                        )
            if not result_possibilities:
                cache[current_board_id] = None
                return None  # No valid moves from here
            else:
                result_possibilities.sort(key=operator.itemgetter(1))
                best_possibility, *_ = result_possibilities
                cache[current_board_id] = best_possibility
                return best_possibility

    best_result = recursive_search(
        {get_board_id(nodes, starting_board)}, starting_board, 0
    )
    assert best_result is not None
    return best_result


def get_blank_board(nodes: Iterable[FieldType]) -> Dict[FieldType, Optional[Amphipod]]:
    return {node: None for node in nodes}


def get_target_board(
    rooms: Dict[Amphipod, Set[FieldType]]
) -> Dict[FieldType, Optional[Amphipod]]:
    return {field: amphipod for amphipod, room in rooms.items() for field in room}


def format_board(board: Dict[Field, Optional[Amphipod]]) -> str:
    f = format_amphipod

    return f"""#############
#{f(board[Field.LF])}{f(board[Field.LN])} {f(board[Field.AB])} {f(board[Field.BC])} {f(board[Field.CD])} {f(board[Field.RN])}{f(board[Field.RF])}#
###{f(board[Field.AH])}#{f(board[Field.BH])}#{f(board[Field.CH])}#{f(board[Field.DH])}###
  #{f(board[Field.AL])}#{f(board[Field.BL])}#{f(board[Field.CL])}#{f(board[Field.DL])}#
  #########"""


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
    sys.setrecursionlimit(sys.getrecursionlimit() * 10)
    run_with_file_argument(main)
