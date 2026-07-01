"""Unit tests for app.retrieval.graph_traversal (self-contained)."""

from app.retrieval.graph_traversal import (
    build_adjacency,
    neighbors,
    bfs_expand,
    rank_expanded_entities,
    find_shortest_path,
)

# A small graph:  A -r1- B -r2- C ,  A -r3- D
RELATIONSHIPS = [
    {"source": "A", "relationship": "r1", "target": "B"},
    {"source": "B", "relationship": "r2", "target": "C"},
    {"source": "A", "relationship": "r3", "target": "D"},
]


def _adj():
    return build_adjacency(RELATIONSHIPS)


def test_build_adjacency_is_undirected():
    adj = _adj()
    assert set(neighbors("A", adj)) == {"B", "D"}
    assert "A" in neighbors("B", adj)  # reverse edge exists


def test_neighbors_unknown_entity_is_empty():
    assert neighbors("Z", _adj()) == []


def test_bfs_records_distance():
    expanded = bfs_expand(["A"], _adj(), max_hops=2)
    by_name = {e.name: e for e in expanded}
    assert by_name["A"].distance == 0
    assert by_name["B"].distance == 1
    assert by_name["D"].distance == 1
    assert by_name["C"].distance == 2  # A -> B -> C


def test_bfs_respects_max_hops():
    expanded = bfs_expand(["A"], _adj(), max_hops=1)
    names = {e.name for e in expanded}
    assert "C" not in names  # C is 2 hops away


def test_bfs_weight_decreases_with_distance():
    expanded = bfs_expand(["A"], _adj(), max_hops=2)
    by_name = {e.name: e for e in expanded}
    assert by_name["B"].weight > by_name["C"].weight


def test_rank_expanded_excludes_seeds_by_default():
    ranked = rank_expanded_entities(["A"], _adj(), max_hops=2, top_k=10)
    assert "A" not in ranked
    # Closest neighbours (B, D) rank ahead of the 2-hop node C.
    assert ranked.index("B") < ranked.index("C")


def test_rank_expanded_top_k_limits():
    ranked = rank_expanded_entities(["A"], _adj(), max_hops=2, top_k=1)
    assert len(ranked) == 1


def test_find_shortest_path_returns_edges():
    path = find_shortest_path("A", "C", _adj())
    assert [e.relationship for e in path] == ["r1", "r2"]


def test_find_shortest_path_same_node_is_empty():
    assert find_shortest_path("A", "A", _adj()) == []


def test_find_shortest_path_no_path():
    adj = build_adjacency(RELATIONSHIPS + [{"source": "X", "relationship": "r", "target": "Y"}])
    assert find_shortest_path("A", "Y", adj) == []


if __name__ == "__main__":
    import sys

    module = sys.modules[__name__]
    tests = [n for n in dir(module) if n.startswith("test_")]
    failures = 0
    for name in tests:
        try:
            getattr(module, name)()
            print(f"PASS  {name}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"FAIL  {name}: {exc!r}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    sys.exit(1 if failures else 0)
