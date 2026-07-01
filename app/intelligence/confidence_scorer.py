"""Confidence scoring (project priority #6).

Produces a single confidence figure (0-100%) for an answer, derived from the
retrieval signals that already exist after hybrid ranking. It reuses the
component breakdown attached to each :class:`~app.retrieval.hybrid_scorer.ScoredChunk`
(semantic / entity / keyword) and combines it with corroborating evidence:

    * strength     -- mean fused score of the top chunks (are the hits strong?),
    * agreement    -- how consistent the top scores are (do sources agree?),
    * coverage     -- entity coverage of the top chunks (is the query on-topic?),
    * support      -- volume of evidence (chunks + graph relationships).

The function is pure and dependency-free. Inputs are plain floats / small
objects, so it is fully unit-testable without retrieval or the LLM.

Design philosophy (CLAUDE.md): single responsibility (scoring only), reusable,
readable over clever.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean, pstdev
from typing import Sequence

# How each factor contributes to the final confidence. Strength dominates;
# the others temper over/under-confidence.
DEFAULT_FACTOR_WEIGHTS: dict[str, float] = {
    "strength": 0.45,
    "agreement": 0.20,
    "coverage": 0.20,
    "support": 0.15,
}

# Evidence volume that counts as "fully supported" (saturates the support term).
FULL_SUPPORT_CHUNKS = 5
FULL_SUPPORT_RELATIONS = 3


@dataclass(frozen=True)
class ConfidenceResult:
    """Confidence percentage plus the factor breakdown behind it."""

    percentage: float  # 0.0 - 100.0
    factors: dict[str, float]  # each in [0, 1]
    supporting_chunks: int
    supporting_relationships: int


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def compute_confidence(
    fused_scores: Sequence[float],
    entity_coverages: Sequence[float],
    num_graph_relationships: int = 0,
    weights: dict[str, float] | None = None,
) -> ConfidenceResult:
    """Compute answer confidence from top-ranked retrieval signals.

    Args:
        fused_scores: fused hybrid scores of the chunks used (``ScoredChunk.score``),
            best first. Expected roughly in [0, 1] but not required to be.
        entity_coverages: per-chunk entity coverage (``components["entity"]``),
            aligned with ``fused_scores``.
        num_graph_relationships: number of graph relationships that fed the
            answer's context (extra corroboration).
        weights: optional override of :data:`DEFAULT_FACTOR_WEIGHTS`.

    Returns:
        A :class:`ConfidenceResult`. With no evidence at all, confidence is 0.
    """

    weights = weights or DEFAULT_FACTOR_WEIGHTS
    num_chunks = len(fused_scores)

    if num_chunks == 0 and num_graph_relationships == 0:
        return ConfidenceResult(0.0, {k: 0.0 for k in weights}, 0, 0)

    if num_chunks:
        strength = _clamp01(fmean(fused_scores))
        # Agreement: low spread among top scores -> sources are consistent.
        spread = pstdev(fused_scores) if num_chunks > 1 else 0.0
        agreement = _clamp01(1.0 - spread)
        coverage = _clamp01(fmean(entity_coverages)) if entity_coverages else 0.0
    else:
        strength = agreement = coverage = 0.0

    # Support saturates once enough independent evidence is present.
    chunk_support = min(num_chunks, FULL_SUPPORT_CHUNKS) / FULL_SUPPORT_CHUNKS
    relation_support = (
        min(num_graph_relationships, FULL_SUPPORT_RELATIONS) / FULL_SUPPORT_RELATIONS
    )
    support = _clamp01(0.5 * chunk_support + 0.5 * relation_support)

    factors = {
        "strength": strength,
        "agreement": agreement,
        "coverage": coverage,
        "support": support,
    }

    combined = sum(weights[name] * value for name, value in factors.items())
    percentage = round(_clamp01(combined) * 100.0, 1)

    return ConfidenceResult(
        percentage=percentage,
        factors=factors,
        supporting_chunks=num_chunks,
        supporting_relationships=num_graph_relationships,
    )


def confidence_from_scored_chunks(
    scored_chunks: Sequence,
    num_graph_relationships: int = 0,
    weights: dict[str, float] | None = None,
) -> ConfidenceResult:
    """Convenience wrapper: derive confidence directly from ``ScoredChunk`` objects.

    Accepts the output of :func:`app.retrieval.hybrid_scorer.hybrid_rank`.
    """

    fused_scores = [sc.score for sc in scored_chunks]
    entity_coverages = [sc.components.get("entity", 0.0) for sc in scored_chunks]
    return compute_confidence(
        fused_scores,
        entity_coverages,
        num_graph_relationships,
        weights,
    )


def format_confidence(result: ConfidenceResult) -> str:
    """Render a short, human-readable confidence block."""

    return (
        f"Confidence: {result.percentage:.0f}%\n"
        f"Retrieved from {result.supporting_chunks} document chunk(s) "
        f"and {result.supporting_relationships} graph relationship(s)."
    )
