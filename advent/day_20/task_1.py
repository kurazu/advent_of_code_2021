from __future__ import annotations

import logging
from typing import Dict, Iterable, List, TextIO, Tuple

import numpy as np
import numpy.typing as npt

from ..cli import run_with_file_argument
from ..io_utils import get_lines, read_empty_line, read_line

logger = logging.getLogger(__name__)

CHAR_MAPPING = {"#": 1, ".": 0}
INVERSE_MAPPING = {v: k for k, v in CHAR_MAPPING.items()}


def map_line(line: str) -> npt.NDArray[int]:
    integers = map(CHAR_MAPPING.__getitem__, line)
    return np.array(list(integers), dtype=int)


def get_algorithm(input: TextIO) -> npt.NDArray[int]:
    algorithm = map_line(read_line(input))
    assert algorithm.shape == (2 ** 9,)
    return algorithm


def read_image(input: TextIO) -> npt.NDArray[int]:
    return np.array(list(map(map_line, get_lines(input))), dtype=int)


def format_image(image: npt.NDArray[int]) -> str:
    return "\n".join(
        map(lambda line: "".join(map(INVERSE_MAPPING.__getitem__, line)), image)
    )


def enhance_image(image: npt.NDArray[int], algorithm: npt.NDArray[int]) -> npt.NDArray:
    return image


def main(input: TextIO) -> str:
    algorithm = get_algorithm(input)
    read_empty_line(input)
    image = read_image(input)
    logger.info("Input image:\n%s", format_image(image))

    image = enhance_image(image, algorithm)
    logger.info("Enhanced image:\n%s", format_image(image))

    image = enhance_image(image, algorithm)
    logger.info("Twice enhanced image:\n%s", format_image(image))

    breakpoint()
    pixels_lit = 0
    return f"{pixels_lit}"


if __name__ == "__main__":
    run_with_file_argument(main)
