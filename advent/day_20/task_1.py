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


POSITION_DECODER = 2 ** (np.arange(9)[::-1])


def enhance_pixel(square: npt.NDArray[int], algorithm: npt.NDArray[int]) -> int:
    assert square.shape == (3, 3)
    index = np.sum(np.ravel(square) * POSITION_DECODER)
    pixel_value: int = algorithm[index]
    return pixel_value


def enhance_image(
    image: npt.NDArray[int], algorithm: npt.NDArray[int], fill_value: int
) -> npt.NDArray[int]:
    height, width = image.shape
    padding = 1
    # We pad the image so that we can take points also around the edge pixels
    extruded_image = np.pad(
        image,
        [(padding * 2, padding * 2), (padding * 2, padding * 2)],
        mode="constant",
        constant_values=fill_value,
    )

    target_image_height = height + 2 * padding
    target_image_width = width + 2 * padding
    target_image = np.zeros((target_image_height, target_image_width), dtype=int)

    for y in range(target_image_height):
        for x in range(target_image_width):
            square = extruded_image[
                y + padding - 1 : y + padding + 2, x + padding - 1 : x + padding + 2
            ]
            target_image[y, x] = enhance_pixel(square, algorithm)
    return target_image


def main(input: TextIO) -> str:
    algorithm = get_algorithm(input)
    read_empty_line(input)
    image = read_image(input)
    logger.info("Input image:\n%s", format_image(image))

    image = enhance_image(image, algorithm, 0)
    logger.info("Enhanced image:\n%s", format_image(image))

    image = enhance_image(image, algorithm, 1)
    logger.info("Twice enhanced image:\n%s", format_image(image))

    pixels_lit = np.sum(image)
    return f"{pixels_lit}"


if __name__ == "__main__":
    run_with_file_argument(main)
