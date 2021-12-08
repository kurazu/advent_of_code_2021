import enum
import logging
from collections import defaultdict
from typing import Dict, List, NewType, Set, TextIO

import numpy as np

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)

Digit = NewType("Digit", int)
SegmentCount = NewType("SegmentCount", int)


class Segment(str, enum.Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"


# How many segments are needed to display a given digit
SEGMENTS_BY_DIGIT: Dict[Digit, SegmentCount] = {
    Digit(0): SegmentCount(6),
    Digit(1): SegmentCount(2),
    Digit(2): SegmentCount(5),
    Digit(3): SegmentCount(5),
    Digit(4): SegmentCount(4),
    Digit(5): SegmentCount(5),
    Digit(6): SegmentCount(6),
    Digit(7): SegmentCount(3),
    Digit(8): SegmentCount(7),
    Digit(9): SegmentCount(6),
}


DIGIT_BY_SEGMENTS: Dict[SegmentCount, Set[Digit]] = defaultdict(set)
for digit, count in SEGMENTS_BY_DIGIT.items():
    DIGIT_BY_SEGMENTS[count].add(digit)

EASY_DIGITS = {
    count: next(iter(digits))
    for count, digits in DIGIT_BY_SEGMENTS.items()
    if len(digits) == 1
}


def main(input: TextIO) -> str:
    logging.info("Easy digits: %s", EASY_DIGITS)

    # input parsing
    stripped_lines = (line.strip() for line in input)
    non_empty_stripped_lines = filter(None, stripped_lines)
    all_signals: List[List[Set[Segment]]] = []
    all_outputs: List[List[Set[Segment]]] = []
    for line in non_empty_stripped_lines:
        _signals, _outputs = line.split(" | ")
        signals = _signals.split(" ")
        outputs = _outputs.split(" ")
        assert len(signals) == 10
        assert len(outputs) == 4
        all_signals.append([{Segment(s) for s in signal} for signal in signals])
        all_outputs.append([{Segment(o) for o in output} for output in outputs])
    del signals
    del outputs

    # calculation
    occurrences = sum(
        1 for outputs in all_outputs for output in outputs if len(output) in EASY_DIGITS
    )
    return f"{occurrences}"


if __name__ == "__main__":
    run_with_file_argument(main)
