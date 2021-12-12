import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import (Dict, Iterable, List, NewType, Optional, Protocol,
                    Sequence, Set, TextIO)

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)


def get_paths(graph: IGraph) -> Iterable[Sequence[Node]]:
    path = [START_NODE]


def main(input: TextIO) -> str:
    graph = read_graph(input)
    paths = 0
    for path in get_paths(graph):
        paths += 1
    return f"{paths}"


if __name__ == "__main__":
    run_with_file_argument(main)
