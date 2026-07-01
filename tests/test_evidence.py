"""Unit tests for app.intelligence.evidence (self-contained).

Only the pure core (`assemble_evidence`) and `Evidence` formatting are tested
here; `gather_evidence`/`attach_evidence` perform live retrieval (ChromaDB/LLM)
and are exercised at runtime, not in unit tests.
"""

from app.intelligence.evidence import assemble_evidence, Evidence

CANDIDATES = [
    {"text": "The objective of SAToC is deep-space endurance.", "semantic_score": 0.95},
    {"text": "COTS components reduce cost significantly.", "semantic_score": 0.60},
    {"text": "Unrelated boilerplate about formatting.", "semantic_score": 0.10},
]

CHUNK_RECORDS = [
    {"chunk_id": "CHUNK_1", "page_number": 1, "text": "The objective of SAToC is deep-space endurance."},
    {"chunk_id": "CHUNK_2", "page_number": 3, "text": "COTS components reduce cost significantly."},
    {"chunk_id": "CHUNK_9", "page_number": 9, "text": "Unrelated boilerplate about formatting."},
]


def _evidence(top_k=3, rels=2):
    return assemble_evidence(
        CANDIDATES,
        entities=["SAToC"],
        query="What is the objective of SAToC",
        chunk_records=CHUNK_RECORDS,
        num_graph_relationships=rels,
        top_k=top_k,
    )


def test_assemble_returns_evidence():
    assert isinstance(_evidence(), Evidence)


def test_top_k_limits_ranked_and_citations():
    ev = _evidence(top_k=2)
    assert len(ev.ranked_chunks) == 2
    assert len(ev.citations) == 2


def test_best_chunk_is_cited_first():
    ev = _evidence()
    # SAToC objective chunk is strongest (semantic + entity + keyword) -> [1].
    assert ev.citations[0].chunk_id == "CHUNK_1"
    assert ev.citations[0].index == 1


def test_citations_recover_page_numbers():
    ev = _evidence()
    assert ev.citations[0].page_number == 1


def test_confidence_reflects_graph_support():
    with_rels = _evidence(rels=3).confidence.percentage
    without_rels = _evidence(rels=0).confidence.percentage
    assert with_rels >= without_rels


def test_appendix_contains_both_blocks():
    ev = _evidence()
    appendix = ev.appendix()
    assert "Confidence" in appendix
    assert "Sources" in appendix
    assert "CHUNK_1" in appendix


def test_sources_and_confidence_blocks_available():
    ev = _evidence()
    assert "[1]" in ev.sources_block
    assert "%" in ev.confidence_block


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
