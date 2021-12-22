from __future__ import annotations

import logging
from collections import Counter, defaultdict
from typing import (Dict, Iterable, Iterator, Literal, NamedTuple, TextIO,
                    Tuple, Union)

from tqdm import tqdm

from ..cli import run_with_file_argument
from ..io_utils import read_line
from .task_1 import BOARD_SIZE, PATTERN

logger = logging.getLogger(__name__)


DIE_POSSIBILITIES = [1, 2, 3]


def get_3_roll_possibilities() -> Iterable[int]:
    for roll_1 in DIE_POSSIBILITIES:
        for roll_2 in DIE_POSSIBILITIES:
            for roll_3 in DIE_POSSIBILITIES:
                yield roll_1 + roll_2 + roll_3


THREE_ROLLS_POSSIBILITIES = Counter(get_3_roll_possibilities())


def read_position(input: TextIO) -> int:
    line = read_line(input)
    match = PATTERN.match(line)
    assert match is not None
    position = int(match.group("position"))
    return position


MAX_SCORE = 5

WinningPlayer = Union[Literal[1], Literal[2]]
Outcome = Tuple[WinningPlayer, int]


class Player(NamedTuple):
    id: WinningPlayer
    position: int
    score: int

    def move(self, die_value: int) -> Player:
        position = ((self.position - 1 + die_value) % BOARD_SIZE) + 1
        score = self.score + position
        return Player(id=self.id, position=position, score=score)


def get_outcomes(
    *, current_player: Player, other_player: Player, universes: int
) -> Iterable[Outcome]:
    for outcome, number_of_universes in THREE_ROLLS_POSSIBILITIES.items():
        universe_branches = universes + number_of_universes
        new_current_player = current_player.move(outcome)
        logger.debug(
            "Player %d rolled %d in %d new universes. He moved from %d to %d and his score jumped from %d to %d.",
            current_player.id,
            outcome,
            number_of_universes,
            current_player.position,
            new_current_player.position,
            current_player.score,
            new_current_player.score,
        )
        if new_current_player.score >= MAX_SCORE:
            # terminal stage
            logger.debug(
                "Game ends in %d universes with player %d winning",
                universe_branches,
                new_current_player.id,
            )
            yield new_current_player.id, universe_branches
        else:
            yield from get_outcomes(
                current_player=other_player,
                other_player=new_current_player,
                universes=universe_branches,
            )


def main(input: TextIO) -> str:
    results: Dict[WinningPlayer, int] = defaultdict(int)
    for winning_player, number_of_universes in tqdm(
        get_outcomes(
            current_player=Player(id=1, position=read_position(input), score=0),
            other_player=Player(id=2, position=read_position(input), score=0),
            universes=0,
        )
    ):
        results[winning_player] += number_of_universes

    player_1_wins = results[1]
    logger.info("Player 1 wins in %d universes", player_1_wins)
    player_2_wins = results[2]
    logger.info("Player 2 wins in %d universes", player_2_wins)

    return f"{max(player_1_wins, player_2_wins)}"


if __name__ == "__main__":
    run_with_file_argument(main)
