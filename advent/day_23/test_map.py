from typing import Dict, List, Optional, Tuple

import pytest

from .enums import Amphipod
from .map import MoveType, PossibleMove, is_allowed_move
from .task_1 import Field

IS_ALLOWED_MOVE_SAMPLE: List[
    Tuple[Dict[Field, Optional[Amphipod]], PossibleMove[Field], bool]
] = [
    (
        {
            Field.LF: None,
            Field.LN: Amphipod.AMBER,
            Field.AB: Amphipod.BRONZE,
            Field.BC: None,
            Field.CD: None,
            Field.RN: None,
            Field.RF: None,
            Field.AX: None,
            Field.BX: None,
            Field.CX: None,
            Field.DX: None,
            Field.AH: None,
            Field.AL: None,
            Field.BH: Amphipod.COPPER,
            Field.BL: Amphipod.DESERT,
            Field.CH: Amphipod.BRONZE,
            Field.CL: Amphipod.COPPER,
            Field.DH: Amphipod.DESERT,
            Field.DL: Amphipod.AMBER,
        },
        PossibleMove(
            from_field=Field.LN,
            to_field=Field.AL,
            through_fields={Field.AX, Field.AH},
            move_type=MoveType.ENTER_ROOM,
            room_owner=Amphipod.AMBER,
            room_neighbours=set(),
        ),
        True,
    ),
    (
        {
            Field.LF: None,
            Field.LN: None,
            Field.AB: Amphipod.BRONZE,
            Field.BC: None,
            Field.CD: None,
            Field.RN: None,
            Field.RF: None,
            Field.AX: None,
            Field.BX: None,
            Field.CX: None,
            Field.DX: None,
            Field.AH: None,
            Field.AL: Amphipod.AMBER,
            Field.BH: Amphipod.COPPER,
            Field.BL: Amphipod.DESERT,
            Field.CH: Amphipod.BRONZE,
            Field.CL: Amphipod.COPPER,
            Field.DH: Amphipod.DESERT,
            Field.DL: Amphipod.AMBER,
        },
        PossibleMove(
            from_field=Field.AL,
            to_field=Field.LN,
            through_fields={Field.AX, Field.AH},
            move_type=MoveType.LEAVE_ROOM,
            room_owner=Amphipod.AMBER,
            room_neighbours=set(),
        ),
        False,
    ),
    (
        {
            Field.BX: None,
            Field.AB: Amphipod.BRONZE,
            Field.LF: None,
            Field.LN: None,
            Field.BC: None,
            Field.CD: Amphipod.BRONZE,
            Field.RN: None,
            Field.RF: None,
            Field.AX: None,
            Field.CX: None,
            Field.DX: None,
            Field.AH: None,
            Field.AL: Amphipod.AMBER,
            Field.BH: None,
            Field.BL: Amphipod.DESERT,
            Field.CH: Amphipod.COPPER,
            Field.CL: Amphipod.COPPER,
            Field.DH: Amphipod.DESERT,
            Field.DL: Amphipod.AMBER,
        },
        PossibleMove(
            from_field=Field.CH,
            to_field=Field.BC,
            through_fields={Field.CX},
            move_type=MoveType.LEAVE_ROOM,
            room_owner=Amphipod.COPPER,
            room_neighbours={Field.CL},
        ),
        False,
    ),
    (
        {
            Field.BX: None,
            Field.AB: Amphipod.BRONZE,
            Field.LF: None,
            Field.LN: None,
            Field.BC: Amphipod.COPPER,
            Field.CD: Amphipod.BRONZE,
            Field.RN: None,
            Field.RF: None,
            Field.AX: None,
            Field.CX: None,
            Field.DX: None,
            Field.AH: None,
            Field.AL: Amphipod.AMBER,
            Field.BH: None,
            Field.BL: Amphipod.DESERT,
            Field.CH: None,
            Field.CL: Amphipod.COPPER,
            Field.DH: Amphipod.DESERT,
            Field.DL: Amphipod.AMBER,
        },
        PossibleMove(
            from_field=Field.BC,
            to_field=Field.CH,
            through_fields={Field.CX},
            move_type=MoveType.ENTER_ROOM,
            room_owner=Amphipod.COPPER,
            room_neighbours={Field.CL},
        ),
        True,
    ),
]


@pytest.mark.parametrize("board,move,expected_allowed", IS_ALLOWED_MOVE_SAMPLE)
def test_is_allowed_move(
    board: Dict[Field, Optional[Amphipod]],
    move: PossibleMove[Field],
    expected_allowed: bool,
) -> None:
    try:
        assert is_allowed_move(board, move) == expected_allowed
    except AssertionError:
        breakpoint()
        is_allowed_move(board, move)
