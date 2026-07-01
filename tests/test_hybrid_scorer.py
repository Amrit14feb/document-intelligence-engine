"""Unit tests for app.retrieval.hybrid_scorer.

These tests are fully self-contained: no ChromaDB, no LLM, no prebuilt data.
They can be run with either pytest or plain python:

    python -m pytest tests/test_hybrid_scorer.py
    python -m tests.test_hybrid_scorer
"""

from app.retrieval.hybrid_scorer import (
    ScoredChunk,
    DEFAULT_WEIGHTS,
    tokenize,
    min_max_normalize,
    entity_coverage_score,
    keyword_overlap_score,
    hybrid_rank,
    reciprocal_rank_fusion,
)


# ------------------------------------------------------------------
# tokenize
# ------------------------------------------------------------------

def test_tokenize_lowercases_and_drops_stopwords():
    assert tokenize("The FPGA IS a Device") == ["fpga", "device"]


def test_tokenize_keeps_alphanumerics():
    assert tokenize("SAToC-2024 v3") == ["satoc", "2024", "v3"]


# ------------------------------------------------------------------
# min_max_normalize
# ------------------------------------------------------------------

def test_min_max_normalize_scales_to_unit_range():
    assert min_max_normalize([1.0, 2.0, 3.0]) == [0.0, 0.5, 1.0]


def test_min_max_normalize_handles_constant_input():
    # No variance -> neutral 0.5 so the signal does not skew ranking.
    assert min_max_normalize([5.0, 5.0, 5.0]) == [0.5, 0.5, 0.5]


def test_min_max_normalize_empty():
    assert min_max_normalize([]) == []


# ------------------------------------------------------------------
# entity_coverage_score
# ------------------------------------------------------------------

def test_entity_coverage_is_fraction_of_distinct_entities():
    chunk = "The FPGA connects to the DSP core."
    assert entity_coverage_score(chunk, ["FPGA", "DSP", "GPU"]) == 2 / 3


def test_entity_coverage_ignores_repetition():
    # Repeating one entity must not exceed coverage of a single distinct entity.
    chunk = "FPGA FPGA FPGA FPGA"
    assert entity_coverage_score(chunk, ["FPGA", "DSP"]) == 0.5


def test_entity_coverage_no_entities_is_zero():
    assert entity_coverage_score("anything", []) == 0.0


# ------------------------------------------------------------------
# keyword_overlap_score
# ------------------------------------------------------------------

def test_keyword_overlap_fraction_of_query_terms():
    # query terms after stopword removal: {objective, satoc, architecture}
    chunk = "The SAToC architecture defines modules."
    assert keyword_overlap_score(chunk, "What is the objective of SAToC architecture") == 2 / 3


def test_keyword_overlap_empty_query_is_zero():
    assert keyword_overlap_score("text", "the of a") == 0.0


# ------------------------------------------------------------------
# hybrid_rank
# ------------------------------------------------------------------

def test_hybrid_rank_empty():
    assert hybrid_rank([], entities=[], query="q") == []


def test_hybrid_rank_returns_scored_chunks_sorted_desc():
    candidates = [
        {"text": "irrelevant text about weather", "semantic_score": 0.10},
        {"text": "the SAToC architecture objective", "semantic_score": 0.90},
    ]
    ranked = hybrid_rank(candidates, entities=["SAToC"], query="SAToC objective")

    assert all(isinstance(r, ScoredChunk) for r in ranked)
    assert ranked[0].text == "the SAToC architecture objective"
    assert ranked[0].score > ranked[1].score


def test_hybrid_rank_semantic_signal_dominates_ties():
    # Same entity/keyword content; only semantic score differs.
    candidates = [
        {"text": "SAToC architecture", "semantic_score": 0.2},
        {"text": "SAToC architecture", "semantic_score": 0.8},
    ]
    ranked = hybrid_rank(candidates, entities=["SAToC"], query="SAToC architecture")
    assert ranked[0].components["semantic"] == 1.0


def test_hybrid_rank_beats_pure_lexical_ordering():
    """Regression test for the core defect this module fixes.

    The old ranker sorted purely by entity substring count, so a weakly
    relevant chunk that merely repeats an entity name would outrank the true
    top semantic hit. Hybrid fusion must NOT do that.
    """
    candidates = [
        # Top semantic hit; mentions the entity once.
        {"text": "The primary objective of the FPGA design is low latency.",
         "semantic_score": 0.95},
        # Entity spammed but semantically weak.
        {"text": "FPGA FPGA FPGA FPGA FPGA FPGA FPGA FPGA",
         "semantic_score": 0.05},
    ]
    ranked = hybrid_rank(candidates, entities=["FPGA"], query="objective of FPGA design")
    assert ranked[0].text.startswith("The primary objective")


def test_hybrid_rank_top_k_limits_results():
    candidates = [{"text": f"chunk {i}", "semantic_score": i / 10} for i in range(10)]
    ranked = hybrid_rank(candidates, entities=[], query="chunk", top_k=3)
    assert len(ranked) == 3


def test_hybrid_rank_missing_semantic_score_defaults_to_zero():
    candidates = [{"text": "no score here"}]
    ranked = hybrid_rank(candidates, entities=[], query="anything")
    assert len(ranked) == 1  # must not raise


def test_hybrid_rank_weights_sum_reasonable():
    # Sanity: default weights are a convex combination (sum to 1.0).
    assert abs(sum(DEFAULT_WEIGHTS.values()) - 1.0) < 1e-9


# ------------------------------------------------------------------
# reciprocal_rank_fusion
# ------------------------------------------------------------------

def test_rrf_rewards_agreement_across_lists():
    semantic = ["A", "B", "C"]
    graph = ["B", "A", "D"]
    fused = reciprocal_rank_fusion([semantic, graph])
    texts = [sc.text for sc in fused]
    # A and B appear near the top of both lists -> they should lead.
    assert set(texts[:2]) == {"A", "B"}


def test_rrf_deterministic_tie_break():
    # Two items with identical RRF scores fall back to first-seen order.
    fused = reciprocal_rank_fusion([["X"], ["Y"]])
    assert [sc.text for sc in fused] == ["X", "Y"]


def test_rrf_top_k():
    fused = reciprocal_rank_fusion([["A", "B", "C", "D"]], top_k=2)
    assert len(fused) == 2


# ------------------------------------------------------------------
# Allow running without pytest.
# ------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    failures = 0
    module = sys.modules[__name__]
    tests = [name for name in dir(module) if name.startswith("test_")]

    for name in tests:
        try:
            getattr(module, name)()
            print(f"PASS  {name}")
        except AssertionError as exc:
            failures += 1
            print(f"FAIL  {name}: {exc}")
        except Exception as exc:  # noqa: BLE001 - surface any error in standalone mode
            failures += 1
            print(f"ERROR {name}: {exc!r}")

    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    sys.exit(1 if failures else 0)
