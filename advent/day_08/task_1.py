import enum
import logging
from collections import defaultdict
from typing import Dict, FrozenSet, List, NewType, Set, TextIO, Tuple

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


class GarbledSegment(str, enum.Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"


#  aaa
# b   c
# b   c
#  ddd
# e   f
# e   f
#  ggg
# Segments lit up to display each digit
SEGMENTS_BY_DIGIT: Dict[Digit, Set[Segment]] = {
    Digit(0): {Segment.A, Segment.B, Segment.C, Segment.E, Segment.F, Segment.G},
    Digit(1): {Segment.C, Segment.F},
    Digit(2): {Segment.A, Segment.C, Segment.D, Segment.E, Segment.G},
    Digit(3): {Segment.A, Segment.C, Segment.D, Segment.F, Segment.G},
    Digit(4): {Segment.B, Segment.C, Segment.D, Segment.F},
    Digit(5): {Segment.A, Segment.B, Segment.D, Segment.F, Segment.G},
    Digit(6): {Segment.A, Segment.B, Segment.D, Segment.E, Segment.F, Segment.G},
    Digit(7): {Segment.A, Segment.C, Segment.F},
    Digit(8): {
        Segment.A,
        Segment.B,
        Segment.C,
        Segment.D,
        Segment.E,
        Segment.F,
        Segment.G,
    },
    Digit(9): {Segment.A, Segment.B, Segment.C, Segment.D, Segment.F, Segment.G},
}


# How many segments are needed to display a given digit
SEGMENTS_COUNT_BY_DIGIT: Dict[Digit, SegmentCount] = {
    digit: SegmentCount(len(segments)) for digit, segments in SEGMENTS_BY_DIGIT.items()
}

# Which digit can it be if that many segments are supposed to be lit up.
DIGIT_BY_SEGMENT_COUNT: Dict[SegmentCount, Set[Digit]] = defaultdict(set)
for digit, count in SEGMENTS_COUNT_BY_DIGIT.items():
    DIGIT_BY_SEGMENT_COUNT[count].add(digit)


# Digits that can be directly guessed from the number of segments lit up
EASY_DIGITS = {
    count: next(iter(digits))
    for count, digits in DIGIT_BY_SEGMENT_COUNT.items()
    if len(digits) == 1
}


def read_data(
    input: TextIO,
) -> Tuple[
    List[List[FrozenSet[GarbledSegment]]], List[List[FrozenSet[GarbledSegment]]]
]:
    stripped_lines = (line.strip() for line in input)
    non_empty_stripped_lines = filter(None, stripped_lines)
    all_signals: List[List[FrozenSet[GarbledSegment]]] = []
    all_outputs: List[List[FrozenSet[GarbledSegment]]] = []
    for line in non_empty_stripped_lines:
        _signals, _outputs = line.split(" | ")
        signals = _signals.split(" ")
        outputs = _outputs.split(" ")
        assert len(signals) == 10
        assert len(outputs) == 4
        all_signals.append(
            [frozenset(GarbledSegment(s) for s in signal) for signal in signals]
        )
        all_outputs.append(
            [frozenset(GarbledSegment(o) for o in output) for output in outputs]
        )
    return all_signals, all_outputs


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
