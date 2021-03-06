from enum import Enum
from typing import Dict, Generic, Iterable, List, Optional, Set, Tuple, TypeVar

import networkx as nx
from networkx.algorithms.shortest_paths import generic as nx_algo
from pydantic.generics import GenericModel
from returns.curry import partial

from .enums import Amphipod

FieldType = TypeVar("FieldType", bound=Enum)


class MoveType(Enum):
    ENTER_ROOM = "enter"
    LEAVE_ROOM = "leave"


class PossibleMove(GenericModel, Generic[FieldType]):
    from_field: FieldType
    """Source field of the move."""

    to_field: FieldType
    """Destination field of the move."""

    through_fields: Set[FieldType]
    """
    Fields that the amphipod needs to traverse on the way from source to destination.
    """

    move_type: MoveType
    """Type of move."""

    room_owner: Amphipod
    """The type of amphipods that are supposed to leave in the room."""

    room_neighbours: Set[FieldType]
    """Other fields in the room that are not in the way."""

    @property
    def distance(self) -> int:
        """The distance an amphipod needs to travel between source and destination."""
        return len(self.through_fields) + 1


def get_possible_moves(
    nodes: Iterable[FieldType],
    edges: Iterable[Tuple[FieldType, FieldType]],
    rooms: Dict[Amphipod, Set[FieldType]],
    hallway: Set[FieldType],
) -> List[PossibleMove[FieldType]]:
    graph = nx.Graph()
    for field in nodes:
        graph.add_node(field)

    for node_a, node_b in edges:
        graph.add_edge(node_a, node_b)

    def get_shortest_path(from_field: FieldType, to_field: FieldType) -> Set[FieldType]:
        path: Iterable[FieldType] = nx_algo.shortest_path(graph, from_field, to_field)
        start, *through, end = path
        assert start == from_field
        assert end == to_field
        return set(through)

    possible_moves: List[PossibleMove[FieldType]] = []

    # from rooms into hallway
    for to_field in hallway:
        for amphipod, room in rooms.items():
            for from_field in room:
                through_fields = get_shortest_path(from_field, to_field)
                required_same_type_neighbours = room - {from_field} - through_fields
                possible_moves.append(
                    PossibleMove(
                        from_field=from_field,
                        to_field=to_field,
                        through_fields=through_fields,
                        # The requirement describes the requirement that needs
                        # to be False for move to be available
                        move_type=MoveType.LEAVE_ROOM,
                        room_owner=amphipod,
                        room_neighbours=required_same_type_neighbours,
                    )
                )

    # from hallway into rooms
    for from_field in hallway:
        for amphipod, room in rooms.items():
            for to_field in room:
                through_fields = get_shortest_path(from_field, to_field)
                # we require that all OTHER fields in the room NOT on the path are
                # filled with the same type of creature
                required_same_type_neighbours = room - {to_field} - through_fields
                possible_moves.append(
                    PossibleMove(
                        from_field=from_field,
                        to_field=to_field,
                        through_fields=through_fields,
                        # The requirement describes the requirement that needs
                        # to be True for move to be available
                        move_type=MoveType.ENTER_ROOM,
                        room_owner=amphipod,
                        room_neighbours=required_same_type_neighbours,
                    )
                )

    return possible_moves


def move(
    board: Dict[FieldType, Optional[Amphipod]], move: PossibleMove[FieldType]
) -> Dict[FieldType, Optional[Amphipod]]:
    return {**board, move.to_field: board[move.from_field], move.from_field: None}


def is_allowed_enter_room_move(
    board: Dict[FieldType, Optional[Amphipod]],
    possible_move: PossibleMove[FieldType],
    amphipod: Amphipod,
) -> bool:
    if amphipod != possible_move.room_owner:
        # wrong type of amphipod cannot make the move
        return False
    if any(
        board[neighbour_field] != possible_move.room_owner
        for neighbour_field in possible_move.room_neighbours
    ):
        # move cannot be made because neighbours are not present yet
        return False

    return True


def is_allowed_leave_room_move(
    board: Dict[FieldType, Optional[Amphipod]],
    possible_move: PossibleMove[FieldType],
    amphipod: Amphipod,
) -> bool:
    if amphipod != possible_move.room_owner:
        # this room is for a different type of amphipods, so this one can leave
        return True
    if not possible_move.room_neighbours:
        # The correct amphipod is on the right place already
        # and does not depend on neighbours
        return False
    # now we know that the required type of amphipod wants to move into the room.
    # we need to check though if all neighbours are already also of the same type.
    # if at least one is not, the move cannot complete (need to wait for neighbours).
    if all(
        board[neighbour_field] == possible_move.room_owner
        for neighbour_field in possible_move.room_neighbours
    ):
        # the neighbours are present already, we cannot leave
        return False

    # Neighbours are not present yet
    return True


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

    if possible_move.move_type == MoveType.ENTER_ROOM:
        return is_allowed_enter_room_move(board, possible_move, amphipod)
    else:
        assert possible_move.move_type == MoveType.LEAVE_ROOM
        return is_allowed_leave_room_move(board, possible_move, amphipod)


def get_allowed_moves(
    board: Dict[FieldType, Optional[Amphipod]],
    possible_moves: List[PossibleMove[FieldType]],
) -> Iterable[PossibleMove[FieldType]]:
    return filter(partial(is_allowed_move, board), possible_moves)


def get_blank_board(nodes: Iterable[FieldType]) -> Dict[FieldType, Optional[Amphipod]]:
    return {node: None for node in nodes}


def get_target_board(
    rooms: Dict[Amphipod, Set[FieldType]]
) -> Dict[FieldType, Optional[Amphipod]]:
    return {field: amphipod for amphipod, room in rooms.items() for field in room}


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


def format_amphipod(amphipod: Optional[Amphipod]) -> str:
    return amphipod.value if amphipod is not None else " "
