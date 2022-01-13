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
    no_moves: List[PossibleMove[FieldType]] = []

    score_sort_key = operator.itemgetter(1)

    cache: Dict[IDType, Tuple[List[PossibleMove[FieldType]], int]] = {}

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
        # moves_so_far: List[PossibleMove[FieldType]],
    ) -> Tuple[List[PossibleMove[FieldType]], int]:
        """Returns a tuple: (moves to terminal stage, energy to terminal stage)."""
        nonlocal best_energy
        if current_board == target_board:
            if current_energy < best_energy:
                logger.debug("Found best terminal state %d", current_energy)
                best_energy = current_energy
            return no_moves, 0

        current_board_id = board_hasher(current_board)
        if current_board_id in cache:
            return cache[current_board_id]

        results: List[Tuple[List[PossibleMove[FieldType]], int]] = []
        for possible_move, move_energy in get_moves(current_board, current_energy):
            possible_board = move(current_board, possible_move)
            result_moves, result_energy = recursive_search(
                possible_board,
                current_energy + move_energy,
                # moves_so_far + [possible_move],
            )
            results.append(
                ([possible_move] + result_moves, result_energy + move_energy)
            )
        if not results:
            # blind alley
            solution = no_moves, ALMOST_INFINITY
            cache[current_board_id] = solution
            return solution
        results.sort(key=score_sort_key)

        (best_possibility_moves, best_possibility_score), *other_possibilities = results
        if current_energy + best_possibility_score < best_energy:
            logger.debug("Found best state %d", current_energy + best_possibility_score)
            best_energy = current_energy + best_possibility_score

        solution = (best_possibility_moves, best_possibility_score)
        cache[current_board_id] = solution
        return solution

    return recursive_search(starting_board, 0)
