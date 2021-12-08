import logging
from collections import defaultdict
from typing import Dict, FrozenSet, List, Set, TextIO

from ..cli import run_with_file_argument
from .task_1 import EASY_DIGITS, Digit, GarbledSegment, SegmentCount, read_data

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
    search_space = garbled_by_length[SegmentCount(6)]
    for garbled in search_space:
        common_part = resolved_digits[Digit(1)] & garbled
        if len(common_part) == 1:
            # we found 6
            resolved_digits[Digit(6)] = garbled
            search_space.remove(garbled)
            # We can also resolve segments C and F
            (f_segment,) = common_part
            (c_segment,) = resolved_digits[Digit(1)] - common_part
            break
    else:
        raise AssertionError("6 not found")

    # From 5-segment digits (2, 3, 5) only 3 will have 2 common parts with 1.
    # Thus we can figure out which signal is 3.
    search_space = garbled_by_length[SegmentCount(5)]
    for garbled in search_space:
        common_part = resolved_digits[Digit(1)] & garbled
        if len(common_part) == 2:
            # we cound 3
            resolved_digits[Digit(3)] = garbled
            search_space.remove(garbled)
            break
    else:
        raise AssertionError("3 not found")

    # From remaining 5-segment digits (2, 5) only 2 will have C-segment lit up.
    # We can use that to figure out 2 and 5.
    search_space = garbled_by_length[SegmentCount(5)]
    for garbled in search_space:
        if c_segment in garbled:
            # We found 2
            resolved_digits[Digit(2)] = garbled
            search_space.remove(garbled)
            # That means that the ramaining one will be 5
            (resolved_digits[Digit(5)],) = search_space
            break
    else:
        raise AssertionError("2 not found")

    # We can also now figure out the E segment
    (e_segment,) = resolved_digits[Digit(2)] - resolved_digits[Digit(3)]

    # The last assignment is to distinguish between remaining 6-segment digits (0 and 9)
    # From those only 0 will have segment E lit up.
    search_space = garbled_by_length[SegmentCount(6)]
    for garbled in search_space:
        if e_segment in garbled:
            # we have found 0
            resolved_digits[Digit(0)] = garbled
            search_space.remove(garbled)
            # the remaining one will be 9 then
            (resolved_digits[Digit(9)],) = search_space
            break
    else:
        raise AssertionError("0 not found")

    # invert the mapping so that we can get digit from garbled signal
    resolved_garbled = {garbled: digit for digit, garbled in resolved_digits.items()}

    # We have resolved all the digits, so we can use them to decipher the outputs
    return [resolved_garbled[garbled] for garbled in outputs]


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
