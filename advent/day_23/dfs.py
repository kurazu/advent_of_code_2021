from __future__ import annotations

import logging
import operator
from typing import (Callable, Dict, Hashable, List, Optional, Set, Tuple,
                    TypeVar)

from .enums import Amphipod
from .map import (FieldType, PossibleMove, get_allowed_moves, get_move_energy,
                  move)

logger = logging.getLogger(__name__)

IDType = TypeVar("IDType", bound=Hashable)


def dfs(
    *,
    starting_board: Dict[FieldType, Optional[Amphipod]],
    target_board: Dict[FieldType, Optional[Amphipod]],
    possible_moves: List[PossibleMove[FieldType]],
    board_hasher: Callable[[Dict[FieldType, Optional[Amphipod]]], IDType]
) -> Tuple[List[PossibleMove[FieldType]], int]:
    best_energy = float("inf")
    cache: Dict[IDType, Optional[Tuple[List[PossibleMove[FieldType]], int]]] = {}
    score_sort_key = operator.itemgetter(1)

    def recursive_search(
        boards_seen: Set[IDType],
        current_board: Dict[FieldType, Optional[Amphipod]],
        current_energy: int,
    ) -> Optional[Tuple[List[PossibleMove[FieldType]], int]]:
        nonlocal best_energy

        current_board_id = board_hasher(current_board)
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
            possibilities = sorted(promising_moves, key=score_sort_key)

            recursive_boards_seen = boards_seen | {current_board_id}
            result_possibilities: List[Tuple[List[PossibleMove[FieldType]], int]] = []
            for possible_move, move_energy in possibilities:
                possible_board = move(current_board, possible_move)
                possible_board_id = board_hasher(possible_board)

                if possible_board_id in boards_seen:
                    continue  # We've been to this state
                else:  # State to explore
                    recursive_result = recursive_search(
                        recursive_boards_seen,
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
                result_possibilities.sort(key=score_sort_key)
                best_possibility, *_ = result_possibilities
                best_possibility_moves, best_possibility_score = best_possibility
                # TODO ADD best_poss
                cache[current_board_id] = best_possibility
                return best_possibility

    best_result = recursive_search({board_hasher(starting_board)}, starting_board, 0)
    assert best_result is not None
    return best_result
