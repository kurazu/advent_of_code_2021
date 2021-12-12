from typing import NewType, Protocol, Set

Node = NewType("Node", str)


class IGraph(Protocol):
    def is_big(self, node: Node) -> bool:
        """Check whether the node is a "big" cave"""

    def get_edges(self, node: Node) -> Set[Node]:
        """Return all edges (target nodes) that are starting in given node."""


START_NODE = Node("start")
END_NODE = Node("end")
