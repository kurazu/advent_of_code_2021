import logging
from typing import List, Optional, TextIO

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)


class IllegalCharacter(Exception):
    def __init__(self, expected: Optional[str], found: str) -> None:
        super().__init__()
        self.expected = expected
        self.found = found


class IncompleteSyntax(Exception):
    pass


SYNTAX = {
    "(": ")",
    "[": "]",
    "<": ">",
    "{": "}",
}


def parse_line(line: str) -> None:
    stack: List[str] = []
    for char in line:
        if char in SYNTAX:
            stack.append(SYNTAX[char])
        elif stack and char == stack[-1]:
            stack.pop()
        else:
            raise IllegalCharacter(expected=stack[-1] if stack else None, found=char)
    if stack:
        raise IncompleteSyntax()


def get_score(exc: IllegalCharacter) -> int:
    return {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }[exc.found]


def main(input: TextIO) -> str:
    score = 0
    for line in get_lines(input):
        try:
            parse_line(line)
        except IllegalCharacter as ex:
            line_score = get_score(ex)
            logger.info(
                "%r expected %r, found %r, score %d",
                line,
                ex.expected,
                ex.found,
                line_score,
            )
            score += line_score
        except IncompleteSyntax:
            logger.info("%r incomplete", line)
        else:
            logger.info("%r OK", line)
    return f"{score}"


if __name__ == "__main__":
    run_with_file_argument(main)
