import collections
import logging
import operator
import re
from collections import defaultdict
from typing import Dict, Iterable, List, NewType, TextIO, Tuple, TypeVar

from returns.curry import partial

from ..cli import run_with_file_argument
from ..io_utils import read_empty_line
from .task_1 import Element, RulesDict, get_polymer, get_rules, rolling_window

logger = logging.getLogger(__name__)

ElementCounts = Dict[Element, int]


def sum_counts(a: ElementCounts, b: ElementCounts) -> ElementCounts:
    return {key: a.get(key, 0) + b.get(key, 0) for key in a | b}


def grow_polymer(
    polymer: Iterable[Element], rules: RulesDict, steps: int
) -> ElementCounts:
    cache: Dict[Tuple[Element, Element, int], ElementCounts] = {}

    def recursive_growth(start: Element, end: Element, depth: int) -> ElementCounts:
        cache_key = start, end, depth
        if cache_key in cache:
            return cache[cache_key]
        insertion = rules[start, end]
        counts: ElementCounts
        if depth == 1:
            counts = sum_counts({start: 1}, {insertion: 1})
        else:
            counts = sum_counts(
                recursive_growth(start, insertion, depth - 1),
                recursive_growth(insertion, end, depth - 1),
            )
        cache[cache_key] = counts
        return counts

    result: ElementCounts = {}
    for start, end in rolling_window(polymer):
        result = sum_counts(result, recursive_growth(start, end, steps))
    result = sum_counts(result, {end: 1})
    return result


def main(input: TextIO, steps: int) -> str:
    polymer: Iterable[Element] = get_polymer(input)
    logger.info("Initial polymer %s", "".join(polymer))

    read_empty_line(input)

    rules = get_rules(input)

    counts = grow_polymer(polymer, rules, steps)
    most_common_element, *_, least_common_element = sorted(
        counts, key=counts.__getitem__, reverse=True
    )
    most_common_count = counts[most_common_element]
    least_common_count = counts[least_common_element]
    logger.info(
        "Most common element %s, count %d", most_common_element, most_common_count
    )
    logger.info(
        "Least common element %s, count %d", least_common_element, least_common_count
    )
    return f"{most_common_count - least_common_count}"


if __name__ == "__main__":
    run_with_file_argument(partial(main, steps=40))
