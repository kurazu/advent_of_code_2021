import itertools
import logging
from typing import TextIO, Tuple

from ..cli import run_with_file_argument
from .parser import compile_program

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    program = compile_program(input)
    numbers = range(9, 1 - 1, -1)
    inputs: Tuple[int, ...]
    for inputs in itertools.product(*([numbers] * 14)):
        w, x, y, z = program(list(inputs))
        if z == 0:
            number = "".join(map(str, inputs))
            return number
    else:
        raise AssertionError("Not found")


if __name__ == "__main__":
    run_with_file_argument(main)
