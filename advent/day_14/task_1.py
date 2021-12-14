import collections
import logging
import re
from typing import Dict, Iterable, List, NewType, TextIO, Tuple, TypeVar

from returns.curry import partial

from ..cli import run_with_file_argument
from ..io_utils import get_lines, read_empty_line

logger = logging.getLogger(__name__)

Element = NewType("Element", str)


def get_polymer(input: TextIO) -> List[Element]:
    return [Element(element) for element in input.readline().strip()]


RULE_PATTERN = re.compile(
    r"^(?P<start>[A-Z])(?P<end>[A-Z])\s\-\>\s(?P<insertion>[A-Z])$"
)

RulesDict = Dict[Tuple[Element, Element], Element]


def get_rules(input: TextIO) -> RulesDict:
    rules: Dict[Tuple[Element, Element], Element] = {}
    for line in get_lines(input):
        match = RULE_PATTERN.match(line)
        assert match is not None
        start = Element(match.group("start"))
        end = Element(match.group("end"))
        insertion = Element(match.group("insertion"))
        key = start, end
        assert key not in rules
        rules[key] = insertion
    return rules


ItemType = TypeVar("ItemType")


def rolling_window(input: Iterable[ItemType]) -> Iterable[Tuple[ItemType, ItemType]]:
    iterator = iter(input)
    prev = next(iterator)
    for elem in iterator:
        yield prev, elem
        prev = elem


def grow_polymer(polymer: Iterable[Element], rules: RulesDict) -> Iterable[Element]:
    for start, end in rolling_window(polymer):
        insertion = rules[start, end]
        yield start
        yield insertion
    yield end


def main(input: TextIO, steps: int) -> str:
    polymer: Iterable[Element] = get_polymer(input)
    logger.info("Initial polymer %s", "".join(polymer))

    read_empty_line(input)

    rules = get_rules(input)

    for step in range(steps):
        polymer = grow_polymer(polymer, rules)

    counter = collections.Counter(polymer)
    (
        (most_common_element, most_common_count),
        *_,
        (least_common_element, least_common_count),
    ) = counter.most_common()
    logger.info(
        "Most common element %s, count %d", most_common_element, most_common_count
    )
    logger.info(
        "Least common element %s, count %d", least_common_element, least_common_count
    )
    return f"{most_common_count - least_common_count}"


if __name__ == "__main__":
    run_with_file_argument(partial(main, steps=10))
