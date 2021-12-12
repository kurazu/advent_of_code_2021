import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import (Dict, Iterable, List, NewType, Optional, Protocol,
                    Sequence, Set, TextIO)

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)

Node = NewType("Node", str)


class IGraph(Protocol):
    def is_big(self, node: Node) -> bool:
        """Check whether the node is a "big" cave"""

    def get_edges(self, node: Node) -> Set[Node]:
        """Return all edges (target nodes) that are starting in given node."""


START_NODE = Node("start")
END_NODE = Node("end")


@dataclass
class Graph:
    # node name -> whether the cave is "big"
    nodes: Dict[Node, bool] = field(init=False, default_factory=dict)
    edges: Dict[Node, Set[Node]] = field(
        init=False, default_factory=lambda: defaultdict(set)
    )

    def determine_big(self, node: Node) -> bool:
        return node.upper() == node

    def add_edge(self, node_a: Node, node_b: Node) -> None:
        self.nodes[node_a] = self.determine_big(node_a)
        self.nodes[node_b] = self.determine_big(node_b)
        self.edges[node_a].add(node_b)
        self.edges[node_b].add(node_a)

    def is_big(self, node: Node) -> bool:
        return self.nodes[node]

    def get_edges(self, node: Node) -> Set[Node]:
        return self.edges[node]


def read_graph(input: TextIO) -> IGraph:
    graph = Graph()
    for line in get_lines(input):
        node_a, node_b = line.split("-")
        graph.add_edge(Node(node_a), Node(node_b))
    return graph


def get_paths(graph: IGraph) -> Iterable[Sequence[Node]]:
    pass


def main(input: TextIO) -> str:
    graph = read_graph(input)
    paths = 0
    for path in get_paths(graph):
        paths += 1
    return f"{paths}"


if __name__ == "__main__":
    run_with_file_argument(main)
