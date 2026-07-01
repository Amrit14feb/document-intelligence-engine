"""Unit tests for app.retrieval.multi_document_graph (self-contained)."""

from app.retrieval.multi_document_graph import (
    merge_documents,
    get_global_entity_context,
)

DOC1 = {
    "doc_id": "DOC001",
    "relationships": [
        {"source": "SAToC", "relationship": "uses", "target": "FPGA"},
        {"source": "SAToC", "relationship": "developed_by", "target": "UFSC"},
    ],
}
DOC2 = {
    "doc_id": "DOC002",
    "relationships": [
        {"source": "satoc", "relationship": "uses", "target": "FPGA"},  # dup (after resolution)
        {"source": "FPGA", "relationship": "programmed_in", "target": "VHDL"},
    ],
}

CANONICAL = ["SAToC", "FPGA", "UFSC", "VHDL"]
ALIASES = {"satoc": "SAToC"}


def test_merge_deduplicates_edges_and_tracks_provenance():
    graph = merge_documents([DOC1, DOC2], CANONICAL, ALIASES)
    # SAToC-uses-FPGA appears in both docs -> single edge, two doc ids.
    uses_edges = [e for e in graph.edges if e.relationship == "uses"]
    assert len(uses_edges) == 1
    assert uses_edges[0].doc_ids == frozenset({"DOC001", "DOC002"})


def test_entity_resolution_unifies_across_documents():
    graph = merge_documents([DOC1, DOC2], CANONICAL, ALIASES)
    # "satoc" from DOC2 resolves to canonical "SAToC" from DOC1.
    assert "SAToC" in graph.adjacency
    assert "satoc" not in graph.adjacency


def test_documents_for_entity():
    graph = merge_documents([DOC1, DOC2], CANONICAL, ALIASES)
    assert graph.documents_for("FPGA") == {"DOC001", "DOC002"}
    assert graph.documents_for("UFSC") == {"DOC001"}


def test_cross_document_entities_are_bridges():
    graph = merge_documents([DOC1, DOC2], CANONICAL, ALIASES)
    bridges = graph.cross_document_entities()
    assert "FPGA" in bridges  # in both docs
    assert "SAToC" in bridges
    assert "VHDL" not in bridges  # only DOC002


def test_global_entity_context_includes_provenance():
    graph = merge_documents([DOC1, DOC2], CANONICAL, ALIASES)
    context = get_global_entity_context("FPGA", graph)
    assert "FPGA" in context
    assert "DOC001" in context or "DOC002" in context


def test_merge_without_resolution_only_strips():
    graph = merge_documents([DOC1, DOC2])  # no canonical / aliases
    # Without resolution, "satoc" and "SAToC" remain distinct nodes.
    assert "satoc" in graph.adjacency
    assert "SAToC" in graph.adjacency


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
