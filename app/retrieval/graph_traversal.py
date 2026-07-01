"""Graph traversal (project priority #4).

The existing ``graph_expansion`` does a flat set-union of one-hop neighbours and
then keeps 20 entities sorted by string length -- it loses hop distance, cannot
find paths, and its "ranking" (by length) is arbitrary.

This module adds a proper traversal layer over the relationship list:

    * an adjacency index built once,
    * breadth-first traversal that records hop distance,
    * distance-weighted ranking of expanded entities (closer == more relevant),
    * shortest-path discovery between two entities (for explainable reasoning).

It is pure and testable: every function takes the relationships (a list of
``{"source", "relationship", "target"}`` dicts) as input. A thin loader is
provided for convenience.

Design philosophy (CLAUDE.md): single responsibility (traversal only, no
semantic retrieval), reusable, loosely coupled, readable.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import json
from typing import Iterable, Sequence


@dataclass(frozen=True)
class ExpandedEntity:
    """An entity reached during traversal, with its hop distance and weight."""

    name: str
    distance: int
    weight: float  # 1 / (1 + distance): closer neighbours score higher


@dataclass(frozen=True)
class Edge:
    """A directed, labelled relationship used when reconstructing paths."""

    source: str
    relationship: str
    target: str


def build_adjacency(relationships: Sequence[dict]) -> dict[str, list[Edge]]:
    """Build an undirected adjacency index from the relationship list.

    Edges are stored in both directions so traversal can move along a
    relationship regardless of which end the query started from, while the
    original direction/label is preserved on each :class:`Edge` for path
    reconstruction.
    """

    adjacency: dict[str, list[Edge]] = {}

    for rel in relationships:
        source = rel["source"]
        target = rel["target"]
        label = rel.get("relationship", "related_to")
        edge = Edge(source, label, target)

        adjacency.setdefault(source, []).append(edge)
        adjacency.setdefault(target, []).append(edge)

    return adjacency


def neighbors(entity: str, adjacency: dict[str, list[Edge]]) -> list[str]:
    """Return the immediate neighbours of ``entity`` (empty if unknown)."""

    result: list[str] = []
    seen: set[str] = set()
    for edge in adjacency.get(entity, []):
        other = edge.target if edge.source == entity else edge.source
        if other != entity and other not in seen:
            seen.add(other)
            result.append(other)
    return result


def bfs_expand(
    seeds: Iterable[str],
    adjacency: dict[str, list[Edge]],
    max_hops: int = 2,
) -> list[ExpandedEntity]:
    """Breadth-first expansion from ``seeds`` up to ``max_hops`` away.

    Each reachable entity is returned once, at its *shortest* hop distance, with
    a weight of ``1 / (1 + distance)``. Seeds themselves are distance 0.
    Results are sorted by weight (descending), then name for determinism.
    """

    distances: dict[str, int] = {}
    queue: deque[tuple[str, int]] = deque()

    for seed in seeds:
        if seed not in distances:
            distances[seed] = 0
            queue.append((seed, 0))

    while queue:
        node, dist = queue.popleft()
        if dist >= max_hops:
            continue
        for other in neighbors(node, adjacency):
            if other not in distances:
                distances[other] = dist + 1
                queue.append((other, dist + 1))

    expanded = [
        ExpandedEntity(name=name, distance=dist, weight=1.0 / (1.0 + dist))
        for name, dist in distances.items()
    ]
    expanded.sort(key=lambda e: (-e.weight, e.name))
    return expanded


def rank_expanded_entities(
    seeds: Iterable[str],
    adjacency: dict[str, list[Edge]],
    max_hops: int = 2,
    top_k: int = 20,
    include_seeds: bool = False,
) -> list[str]:
    """Return traversal-ranked neighbour names (a drop-in for graph expansion).

    Unlike the legacy length-based cap, this keeps the ``top_k`` *closest*
    entities, which are the most relevant for query expansion.
    """

    expanded = bfs_expand(seeds, adjacency, max_hops)
    seed_set = {s for s in seeds}

    names = [
        e.name
        for e in expanded
        if include_seeds or e.name not in seed_set
    ]
    return names[:top_k]


def find_shortest_path(
    source: str,
    target: str,
    adjacency: dict[str, list[Edge]],
    max_hops: int = 4,
) -> list[Edge]:
    """Find a shortest labelled path between two entities.

    Returns the list of edges connecting ``source`` to ``target`` (empty if no
    path exists within ``max_hops``, or if source == target). Useful for
    explaining *why* two entities are related.
    """

    if source == target:
        return []

    # BFS tracking the edge used to reach each node.
    came_from: dict[str, tuple[str, Edge]] = {}
    visited: set[str] = {source}
    queue: deque[tuple[str, int]] = deque([(source, 0)])

    while queue:
        node, dist = queue.popleft()
        if dist >= max_hops:
            continue
        for edge in adjacency.get(node, []):
            other = edge.target if edge.source == node else edge.source
            if other in visited:
                continue
            visited.add(other)
            came_from[other] = (node, edge)
            if other == target:
                return _reconstruct_path(came_from, source, target)
            queue.append((other, dist + 1))

    return []


def _reconstruct_path(
    came_from: dict[str, tuple[str, Edge]],
    source: str,
    target: str,
) -> list[Edge]:
    """Walk ``came_from`` backwards to build the edge path source -> target."""

    path: list[Edge] = []
    node = target
    while node != source:
        prev, edge = came_from[node]
        path.append(edge)
        node = prev
    path.reverse()
    return path


# ------------------------------------------------------------------
# Optional thin loader.
# ------------------------------------------------------------------

def load_relationships(
    path: str = "data/knowledge/relationships.json",
) -> list[dict]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)
