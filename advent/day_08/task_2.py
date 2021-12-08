import logging
from collections import defaultdict
from typing import Dict, List, Set, TextIO

import numpy as np

from ..cli import run_with_file_argument
from .task_1 import (DIGIT_BY_SEGMENT_COUNT, EASY_DIGITS, SEGMENTS_BY_DIGIT,
                     Digit, GarbledSegment, Segment, SegmentCount, read_data)

logger = logging.getLogger(__name__)


def resolve(
    signals: List[Set[GarbledSegment]], outputs: List[Set[GarbledSegment]]
) -> List[Digit]:
    return [Digit(0), Digit(0), Digit(0), Digit(0)]


def main(input: TextIO) -> str:
    logging.info("Easy digits: %s", EASY_DIGITS)

    all_signals, all_outputs = read_data(input)

    resolved_sum: int = 0
    for signals, outputs in zip(all_signals, all_outputs):
        resolved_output = resolve(signals, outputs)
        resolved = sum(
            value * (10 ** power)
            for value, power in zip(
                reversed(resolved_output), range(len(resolved_output))
            )
        )
        resolved_sum += resolved

    return f"{resolved_sum}"


if __name__ == "__main__":
    run_with_file_argument(main)
