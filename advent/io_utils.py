from typing import Iterable, TextIO


def get_lines(input: TextIO) -> Iterable[str]:
    stripped_lines = map(str.strip, input)
    non_empty_lines = filter(None, stripped_lines)
    return non_empty_lines


def read_empty_line(input: TextIO) -> None:
    assert input.readline().strip() == ""  # expect empty line
