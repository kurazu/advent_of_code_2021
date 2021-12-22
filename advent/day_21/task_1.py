from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from itertools import cycle
from typing import Iterator, TextIO

from ..cli import run_with_file_argument
from ..io_utils import read_line

logger = logging.getLogger(__name__)

PATTERN = re.compile(r"^Player (?P<number>\d) starting position: (?P<position>\d+)$")


@dataclass
class Die:
    numbers: Iterator[int]
    rolls: int = field(default=0, init=False)

    def roll(self) -> int:
        self.rolls += 1
        return next(self.numbers)


@dataclass
class Player:
    number: int
    position: int
    score: int = field(default=0, init=False)


def read_player(input: TextIO) -> Player:
    line = read_line(input)
    match = PATTERN.match(line)
    assert match is not None
    position = int(match.group("position"))
    number = int(match.group("number"))
    return Player(position=position, number=number)


MAX_SCORE = 1000
BOARD_SIZE = 10
ROLLS_PER_TURN = 3


def move(die: Die, player: Player) -> None:
    die_value = sum(die.roll() for _ in range(ROLLS_PER_TURN))
    player.position = ((player.position - 1 + die_value) % BOARD_SIZE) + 1
    player.score += player.position
    logger.info(
        "Player %d rolled %d. Position %d. Score %d",
        player.number,
        die_value,
        player.position,
        player.score,
    )


def main(input: TextIO) -> str:
    die = Die(numbers=cycle(range(1, 100 + 1)))
    players = [
        read_player(input),
        read_player(input),
    ]
    for player in players:
        logger.info(
            "Player %d. Position %d. Score %d",
            player.number,
            player.position,
            player.score,
        )
    for current_player in cycle(players):
        move(die, current_player)
        if current_player.score >= MAX_SCORE:
            (losing_player,) = [
                player for player in players if player is not current_player
            ]
            logger.info(
                "End of game. Winner %d with %d points. Loser %d with %d points",
                current_player.number,
                current_player.score,
                losing_player.number,
                losing_player.score,
            )
            break
    else:
        raise AssertionError()
    logger.info("Die rolled %d times", die.rolls)
    return f"{losing_player.score * die.rolls}"


if __name__ == "__main__":
    run_with_file_argument(main)
