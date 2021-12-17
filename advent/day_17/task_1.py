import functools
import io
import logging
import operator
import re
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Protocol, TextIO

from ..cli import run_with_file_argument
from ..io_utils import read_line

logger = logging.getLogger(__name__)


TARGET_SPEC_PATTERN = re.compile(
    r"^target area: x=(?P<min_x>\d+)\.\.(?P<max_x>\d+), "
    r"y=(?P<min_y>\-\d+)..(?P<max_y>-\d+)$"
)


def main(input: TextIO) -> str:
    # read the map
    target_spec = read_line(input)
    match = TARGET_SPEC_PATTERN.match(target_spec)
    assert match is not None

    min_x = int(match.group("min_x"))
    max_x = int(match.group("max_x"))
    min_y = int(match.group("min_y"))
    max_y = int(match.group("max_y"))

    logger.info("Target area: x=%d..%d, y=%d..%d", min_x, max_x, min_y, max_y)

    top_y = 0
    return f"{top_y}"


if __name__ == "__main__":
    run_with_file_argument(main)
