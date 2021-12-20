from __future__ import annotations

import logging
import math
import re
from collections import Counter
from itertools import combinations, starmap
from typing import Dict, Iterable, List, TextIO, Tuple

import networkx as nx
import numpy as np
import numpy.typing as npt
from networkx.drawing.nx_pydot import write_dot

from ..cli import run_with_file_argument
from ..io_utils import read_line

logger = logging.getLogger(__name__)

HEADER_PATTERN = re.compile(r"^\-\-\-\sscanner\s\d+\s\-\-\-$")


def read_beacons(input: TextIO) -> Iterable[npt.NDArray]:
    while True:
        header = read_line(input)
        if not header:
            break
        beacons: List[Tuple[int, int, int]] = []
        assert HEADER_PATTERN.match(header) is not None
        while line := read_line(input):
            x, y, z = map(int, line.split(","))
            beacons.append((x, y, z))
        yield np.array(beacons)


def distance(a: npt.NDArray[int], b: npt.NDArray[int]) -> float:
    dist: float = np.linalg.norm(a - b)
    return dist


def get_edges(beacons: npt.NDArray[int]) -> Dict[float, Tuple[int, int]]:
    enumerated_beacons = enumerate(beacons)
    result: Dict[float, Tuple[int, int]] = {}
    for (a_idx, a_beacon), (b_idx, b_beacon) in combinations(enumerated_beacons, 2):
        dist = distance(a_beacon, b_beacon)
        assert dist not in result
        result[dist] = a_idx, b_idx
    return result


def resolve_scanner(
    source_beacons: npt.NDArray[int], target_beacons: npt.NDArray[int]
) -> npt.NDArray[int]:
    # find common edges
    source_edges = get_edges(source_beacons)
    target_edges = get_edges(target_beacons)
    common_edges = set(source_edges) & set(target_edges)

    # Now pick 2 nodes at random, then one more and find their equivalents
    first_edge, second_edge, *_ = common_edges
    source_node_a, source_node_b = source_edges[first_edge]
    other_source_nodes = source_edges[
        second_edge
    ]  # at least one is guaranteed to be neither a nor b
    source_node_c, *_ = set(other_source_nodes) - {source_node_a, source_node_b}
    source_a_to_b = distance(
        source_beacons[source_node_a], source_beacons[source_node_b]
    )
    source_a_to_c = distance(
        source_beacons[source_node_a], source_beacons[source_node_c]
    )
    source_b_to_c = distance(
        source_beacons[source_node_b], source_beacons[source_node_c]
    )

    target_nodes_a_or_b = target_edges[first_edge]
    target_nodes_c_or_d = target_edges[second_edge]
    assert (
        distance(
            target_beacons[target_nodes_a_or_b[0]],
            target_beacons[target_nodes_a_or_b[1]],
        )
        == source_a_to_b
    )

    # Figure out which nodes are which (map A, B, C from source to target)
    if (
        distance(
            target_beacons[target_nodes_a_or_b[0]],
            target_beacons[target_nodes_c_or_d[0]],
        )
        == source_a_to_c
    ):
        target_node_a, target_node_b = target_nodes_a_or_b
        target_node_c, target_node_d = target_nodes_c_or_d
    elif (
        distance(
            target_beacons[target_nodes_a_or_b[1]],
            target_beacons[target_nodes_c_or_d[0]],
        )
        == source_a_to_c
    ):
        target_node_b, target_node_a = target_nodes_a_or_b
        target_node_c, target_node_d = target_nodes_c_or_d
    elif (
        distance(
            target_beacons[target_nodes_a_or_b[0]],
            target_beacons[target_nodes_c_or_d[1]],
        )
        == source_a_to_c
    ):
        target_node_a, target_node_b = target_nodes_a_or_b
        target_node_d, target_node_c = target_nodes_c_or_d
    else:
        assert (
            distance(
                target_beacons[target_nodes_a_or_b[1]],
                target_beacons[target_nodes_c_or_d[1]],
            )
            == source_a_to_c
        )
        target_node_b, target_node_a = target_nodes_a_or_b
        target_node_d, target_node_c = target_nodes_c_or_d

    # make sure that our triangle is correct
    assert (
        distance(target_beacons[target_node_a], target_beacons[target_node_b])
        == source_a_to_b
    )
    assert (
        distance(target_beacons[target_node_a], target_beacons[target_node_c])
        == source_a_to_c
    )
    assert (
        distance(target_beacons[target_node_b], target_beacons[target_node_c])
        == source_b_to_c
    )
    breakpoint()


def main(input: TextIO) -> str:
    scanners = list(read_beacons(input))

    # First we verify that there are no repeating  distances within
    # each scanner's beacons - thanks to this we will be able to identify
    # graph edges in an unique way.
    has_repeating_distances = False
    for i, beacons in enumerate(scanners):
        distances = starmap(distance, combinations(beacons, 2))
        counter = Counter(distances)
        repeating_distances = (
            count for dist, count in counter.most_common() if count > 2
        )
        for count in repeating_distances:
            logger.info("Scanner %d repeated distance %d", i, count)
            has_repeating_distances = True
        logger.info("Scanner %d done", i)
    assert not has_repeating_distances

    # Then we build a graph of adjacency between scanners.
    # We require a fully conncted clique of size 12 to be common
    # between graphs.
    # We will use this adjacency graph to resolve the scanners in order.
    neighbourhood_graph = nx.Graph()
    for idx, _ in enumerate(scanners):
        neighbourhood_graph.add_node(idx)

    min_edges = math.comb(12, 2)
    for (a_idx, a_beacons), (b_idx, b_beacons) in combinations(enumerate(scanners), 2):
        a_edges = get_edges(a_beacons)
        b_edges = get_edges(b_beacons)
        common_edges = set(a_edges) & set(b_edges)
        if len(common_edges) >= min_edges:
            logger.info(
                "Scanner %d and %d have %d common edges",
                a_idx,
                b_idx,
                len(common_edges),
            )
            neighbourhood_graph.add_edge(a_idx, b_idx)

    nx.nx_pydot.to_pydot(neighbourhood_graph).write_png("neighbourhood_graph.png")

    # We need to start resolving our graphs
    source_scanner_idx = 0
    target_scanner_idx = next(iter(neighbourhood_graph.neighbors(source_scanner_idx)))
    resolved_scanner = resolve_scanner(
        scanners[source_scanner_idx], scanners[target_scanner_idx]
    )

    number_of_beacons = 0
    return f"{number_of_beacons}"


if __name__ == "__main__":
    run_with_file_argument(main)
