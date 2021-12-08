import logging
from collections import defaultdict
from typing import Dict, FrozenSet, List, Set, TextIO

import numpy as np

from ..cli import run_with_file_argument
from .task_1 import (DIGIT_BY_SEGMENT_COUNT, EASY_DIGITS, SEGMENTS_BY_DIGIT,
                     Digit, GarbledSegment, Segment, SegmentCount, read_data)

logger = logging.getLogger(__name__)


def resolve(
    signals: List[FrozenSet[GarbledSegment]], outputs: List[FrozenSet[GarbledSegment]]
) -> List[Digit]:
    # First group the garbed signals by their length
    garbled_by_length: Dict[SegmentCount, Set[FrozenSet[GarbledSegment]]] = defaultdict(
        set
    )
    for signal in signals:
        segment_count = SegmentCount(len(signal))
        garbled_by_length[segment_count].add(signal)
    # This should enable us to figure out the easy digits
    resolved_digits: Dict[Digit, FrozenSet[GarbledSegment]] = {}
    for count, digit in EASY_DIGITS.items():
        (garbled,) = garbled_by_length[count]
        resolved_digits[digit] = garbled
    # Now based on the resolved easy digits and differences between digits on an
    # actual 7-segment display we can slowly figure out the rest.

    # 7 and 1 differ by the top segment, so we can figure out the assignment
    # of the top segment (A)
    (a_segment,) = resolved_digits[Digit(7)] - resolved_digits[Digit(1)]

    # From 6-segment digits (0, 9 and 6) only 6 will not have 2 common parts with 1.
    # Thus we can figure out which signal is 6.
    for garbled in garbled_by_length[SegmentCount(6)]:
        common_part = resolved_digits[Digit(1)] & garbled
        if len(common_part) == 1:
            # we found 6
            resolved_digits[Digit(6)] = garbled
            garbled_by_length[SegmentCount(6)].remove(garbled)
            # We can also resolve segments C and F
            (f_segment,) = common_part
            (c_segment,) = resolved_digits[Digit(1)] - common_part
            break
    else:
        raise AssertionError("6 not found")

    # From 5-segment digits (2, 3, 5) only 3 will have 2 common parts with 1.
    # Thus we can figure out which signal is 3.
    for garbled in garbled_by_length[SegmentCount(5)]:
        common_part = resolved_digits[Digit(1)] & garbled
        if len(common_part) == 2:
            # we cound 3
            resolved_digits[Digit(3)] = garbled
            garbled_by_length[SegmentCount(5)].remove(garbled)
            break
    else:
        raise AssertionError("3 not found")
    breakpoint()
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
