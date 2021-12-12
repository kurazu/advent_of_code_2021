import logging
from collections import defaultdict
from typing import (Dict, Iterable, List, NewType, Optional, Protocol,
                    Sequence, Set, TextIO)

from ..cli import run_with_file_argument
from .graph import read_graph
from .interfaces import END_NODE, START_NODE, IGraph, Node

logger = logging.getLogger(__name__)


def get_paths(graph: IGraph, current_path: Sequence[Node]) -> Iterable[Sequence[Node]]:
    last_node = current_path[-1]
    for next_node in graph.get_edges(last_node):
        next_is_big = graph.is_big(next_node)
        new_path = [*current_path, next_node]
        if next_node == END_NODE:
            yield new_path
        elif next_is_big:
            # no restrictions on stepping back into big nodes
            yield from get_paths(graph, new_path)
        elif next_node in current_path:
            continue  # cannot step twice into same small node
        else:
            # can step first time into a small node
            yield from get_paths(graph, new_path)


def main(input: TextIO) -> str:
    graph: IGraph = read_graph(input)
    paths = 0
    for path in get_paths(graph, [START_NODE]):
        logger.info("Found path %s", ", ".join(path))
        paths += 1
    return f"{paths}"


if __name__ == "__main__":
    run_with_file_argument(main)
