from typing import Iterable, TextIO

import numpy as np
import numpy.typing as npt


def get_lines(input: TextIO) -> Iterable[str]:
    stripped_lines = map(str.strip, input)
    non_empty_lines = filter(None, stripped_lines)
    return non_empty_lines


def read_empty_line(input: TextIO) -> None:
    assert input.readline().strip() == ""  # expect empty line


def read_numbers_array(input: TextIO) -> npt.NDArray[int]:
    return np.array([list(map(int, line)) for line in get_lines(input)], dtype=int)
