import itertools
import logging
import multiprocessing
from functools import partial
from typing import Iterable, List, Optional, TextIO, Tuple

from tqdm import tqdm

from ..cli import run_with_file_argument
from .parser import compile_program

logger = logging.getLogger(__name__)

CHUNK_SIZE = 100_000


def check_number(program, inputs: List[int]) -> Optional[int]:
    w, x, y, z = program(inputs)
    if z == 0:
        return int("".join(map(str, inputs)))


def main(input: TextIO) -> str:
    program = compile_program(input)
    numbers = range(9, 1 - 1, -1)
    possible_inputs: Iterable[List[int]] = tqdm(
        map(list, itertools.product(*([numbers] * 14))), total=9 ** 14
    )
    with multiprocessing.Pool() as pool:
        results = pool.imap(partial(check_number, program), possible_inputs, 100_000)
        matching_results = filter(None, results)
        for number in matching_results:
            return f"{number}"
        else:
            raise AssertionError("Not found")


if __name__ == "__main__":
    run_with_file_argument(main)
