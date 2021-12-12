from pathlib import Path
from typing import Set, TextIO, Tuple

import click
import pydot

from .graph import read_graph
from .interfaces import END_NODE, START_NODE, Node


@click.command()
@click.option("--input", type=click.File("r", encoding="utf-8"), required=True)
@click.option(
    "--output",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, path_type=Path),
    required=True,
)
def main(input: TextIO, output: Path) -> None:
    source_graph = read_graph(input)
    graph = pydot.Dot("Sample", graph_type="graph")

    for node, big in source_graph.nodes.items():
        shape: str
        color: str
        if node == START_NODE:
            shape = "circle"
            color = "gray"
        elif node == END_NODE:
            shape = "doublecircle"
            color = "gray"
        elif big:
            shape = "oval"
            color = "green"
        else:
            shape = "circle"
            color = "red"
        graph.add_node(pydot.Node(node, shape=shape, color=color))

    edges_to_skip: Set[Tuple[Node, Node]] = set()
    for source, targets in source_graph.edges.items():
        for target in targets:
            if (source, target) in edges_to_skip:
                continue
            graph.add_edge(pydot.Edge(source, target))
            edges_to_skip.add((target, source))

    graph.write_png(output)


if __name__ == "__main__":
    main()
