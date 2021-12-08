import logging
from typing import TextIO

import numpy as np

from ..cli import run_with_file_argument
from .task_1 import (DIGIT_BY_SEGMENTS, EASY_DIGITS, SEGMENTS_BY_DIGIT,
                     Segment, read_data)

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    logging.info("Easy digits: %s", EASY_DIGITS)

    all_signals, all_outputs = read_data(input)

    # calculation
    occurrences = sum(
        1 for outputs in all_outputs for output in outputs if len(output) in EASY_DIGITS
    )
    return f"{occurrences}"


if __name__ == "__main__":
    run_with_file_argument(main)
