import logging
from typing import List, TextIO

from ..cli import run_with_file_argument
from ..io_utils import get_lines
from .task_1 import SYNTAX, IllegalCharacter

logger = logging.getLogger(__name__)


def parse_line(line: str) -> List[str]:
    stack: List[str] = []
    for char in line:
        if char in SYNTAX:
            stack.append(SYNTAX[char])
        elif stack and char == stack[-1]:
            stack.pop()
        else:
            raise IllegalCharacter(expected=stack[-1] if stack else None, found=char)
    return stack


SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def main(input: TextIO) -> str:
    scores: List[int] = []
    for line in get_lines(input):
        try:
            completion = parse_line(line)
        except IllegalCharacter:
            logger.info(
                "%r illegal",
                line,
            )
            continue  # ignore the line
        else:
            score = 0
            for char in reversed(completion):
                score *= 5
                score += SCORES[char]
            logger.info("%r completion %d", line, score)
            scores.append(score)
    assert len(scores) % 2
    scores.sort()
    middle_score = scores[len(scores) // 2]
    return f"{middle_score}"


if __name__ == "__main__":
    run_with_file_argument(main)
