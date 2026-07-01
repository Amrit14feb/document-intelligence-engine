"""Unit tests for app.intelligence.confidence_scorer (self-contained)."""

from app.retrieval.hybrid_scorer import ScoredChunk
from app.intelligence.confidence_scorer import (
    compute_confidence,
    confidence_from_scored_chunks,
    format_confidence,
)


def test_no_evidence_is_zero():
    result = compute_confidence([], [], num_graph_relationships=0)
    assert result.percentage == 0.0


def test_strong_consistent_evidence_is_high():
    result = compute_confidence(
        fused_scores=[0.9, 0.88, 0.87, 0.86, 0.85],
        entity_coverages=[1.0, 1.0, 1.0, 0.8, 0.8],
        num_graph_relationships=3,
    )
    assert result.percentage >= 75.0


def test_weak_evidence_is_low():
    result = compute_confidence(
        fused_scores=[0.1],
        entity_coverages=[0.0],
        num_graph_relationships=0,
    )
    assert result.percentage <= 30.0


def test_percentage_bounded():
    result = compute_confidence([2.0, 2.0], [2.0, 2.0], num_graph_relationships=99)
    assert 0.0 <= result.percentage <= 100.0


def test_agreement_penalizes_spread():
    consistent = compute_confidence([0.8, 0.8, 0.8], [0.5, 0.5, 0.5])
    spread = compute_confidence([0.8, 0.2, 0.8], [0.5, 0.5, 0.5])
    assert consistent.factors["agreement"] > spread.factors["agreement"]


def test_support_counts_are_reported():
    result = compute_confidence([0.5, 0.5], [0.5, 0.5], num_graph_relationships=2)
    assert result.supporting_chunks == 2
    assert result.supporting_relationships == 2


def test_confidence_from_scored_chunks_wrapper():
    chunks = [
        ScoredChunk(text="a", score=0.9, components={"entity": 1.0}),
        ScoredChunk(text="b", score=0.8, components={"entity": 0.5}),
    ]
    result = confidence_from_scored_chunks(chunks, num_graph_relationships=1)
    assert result.supporting_chunks == 2
    assert 0.0 < result.percentage <= 100.0


def test_format_confidence_readable():
    result = compute_confidence([0.7], [0.6], num_graph_relationships=1)
    text = format_confidence(result)
    assert "Confidence" in text
    assert "%" in text


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
