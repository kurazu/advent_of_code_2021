from enum import Enum
from typing import Dict, Generic, Iterable, List, Optional, Set, Tuple, TypeVar

import networkx as nx
from networkx.algorithms.shortest_paths import generic as nx_algo
from pydantic.generics import GenericModel

from .enums import Amphipod

FieldType = TypeVar("FieldType", bound=Enum)


class PossibleMove(GenericModel, Generic[FieldType]):
    from_field: FieldType
    to_field: FieldType
    through_fields: Set[FieldType]
    required_amphipod: Optional[Amphipod]
    required_same_type_neighbours: Set[FieldType]

    @property
    def distance(self) -> int:
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
        for room in rooms.values():
            for from_field in room:
                through_fields = get_shortest_path(from_field, to_field)
                possible_moves.append(
                    PossibleMove(
                        from_field=from_field,
                        to_field=to_field,
                        through_fields=through_fields,
                        required_amphipod=None,
                        required_same_type_neighbours=set(),
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
                        required_amphipod=amphipod,
                        required_same_type_neighbours=required_same_type_neighbours,
                    )
                )

    return possible_moves
