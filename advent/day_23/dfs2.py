from __future__ import annotations

import logging
import operator
from typing import (Callable, Dict, Hashable, Iterable, List, Optional, Set,
                    Tuple, TypeVar)

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
    ALMOST_INFINITY = 2 ** 31
    best_energy = ALMOST_INFINITY

    score_sort_key = operator.itemgetter(1)

    def get_moves(
        current_board: Dict[FieldType, Optional[Amphipod]], current_energy: int
    ) -> Iterable[Tuple[PossibleMove[FieldType], int]]:
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
        return sorted(promising_moves, key=score_sort_key)

    def recursive_search(
        current_board: Dict[FieldType, Optional[Amphipod]],
        current_energy: int,
        moves_so_far: List[PossibleMove[FieldType]],
    ) -> Tuple[List[PossibleMove[FieldType]], int]:
        """Returns a tuple: (moves to terminal stage, energy to terminal stage)."""
        if len(moves_so_far) == 50:
            breakpoint()
        nonlocal best_energy
        if current_board == target_board:
            if current_energy < best_energy:
                logger.debug("Found best terminal state %d", current_energy)
                best_energy = current_energy
            return [], 0

        results: List[Tuple[List[PossibleMove[FieldType]], int]] = []
        for possible_move, move_energy in get_moves(current_board, current_energy):
            possible_board = move(current_board, possible_move)
            result_moves, result_energy = recursive_search(
                possible_board,
                current_energy + move_energy,
                moves_so_far + [possible_move],
            )
            results.append((result_moves, result_energy + move_energy))
        if not results:
            # blind alley
            return [], ALMOST_INFINITY
        results.sort(key=score_sort_key)

        best_possibility, *other_possibilities = results
        best_possibility_moves, best_possibility_score = best_possibility
        if current_energy + best_possibility_score < best_energy:
            logger.debug("Found best state %d", current_energy + best_possibility_score)
            best_energy = current_energy + best_possibility_score
        return best_possibility_moves, current_energy + best_possibility_score

    return recursive_search(starting_board, 0, [])
