"""Hybrid scoring and fusion for retrieval.

This module improves retrieval quality and hybrid ranking (project priorities
#1 and #2) by combining three complementary relevance signals into a single
ranked list:

1. Semantic similarity  -- from the vector store (ChromaDB).
2. Entity coverage       -- fraction of detected/expanded entities present in a chunk.
3. Keyword overlap       -- overlap between query terms and chunk terms.

The previous `hybrid_ranker` re-ranked chunks *only* by raw entity substring
counts, discarding the semantic ordering produced by the vector store. That is
not a hybrid ranking -- it is pure lexical matching, and it can push a weakly
relevant chunk (that merely repeats an entity name) above the best semantic hit.

This module is intentionally free of I/O: every function is pure and therefore
independently testable without ChromaDB, the LLM, or any prebuilt data. Callers
pass in the semantic scores they already obtained from the retriever.

Design philosophy (see CLAUDE.md):
    * single responsibility -- scoring/fusion only, no retrieval, no reasoning
    * reusable, loosely coupled pure functions
    * readable over clever
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Iterable, Sequence


# ------------------------------------------------------------------
# Default fusion weights
# ------------------------------------------------------------------
# Semantic relevance is the strongest single signal, so it dominates.
# Entity coverage and keyword overlap refine ties and reward chunks that
# actually mention what the user asked about.
DEFAULT_WEIGHTS: dict[str, float] = {
    "semantic": 0.60,
    "entity": 0.25,
    "keyword": 0.15,
}

# Stopwords kept deliberately small: just enough to stop trivial terms from
# inflating keyword overlap. This is not meant to be a linguistic resource.
_STOPWORDS: frozenset[str] = frozenset(
    {
        "the", "a", "an", "of", "to", "in", "on", "for", "and", "or", "is",
        "are", "was", "were", "be", "by", "with", "as", "at", "it", "this",
        "that", "these", "those", "what", "which", "who", "how", "does", "do",
        "from", "into", "about",
    }
)

_TOKEN_RE = re.compile(r"[a-z0-9]+")


@dataclass
class ScoredChunk:
    """A retrieved chunk with its fused score and a breakdown of components.

    The component breakdown is deliberately preserved (rather than collapsed to
    a single float) so that downstream features on the roadmap -- citation
    generation and confidence scoring -- can explain *why* a chunk ranked where
    it did.
    """

    text: str
    score: float
    components: dict[str, float] = field(default_factory=dict)


def tokenize(text: str) -> list[str]:
    """Lowercase, split into alphanumeric tokens, and drop stopwords."""

    return [
        token
        for token in _TOKEN_RE.findall(text.lower())
        if token not in _STOPWORDS
    ]


def min_max_normalize(scores: Sequence[float]) -> list[float]:
    """Scale scores into [0, 1] using min-max normalization.

    If every score is equal (or the list is empty), returns a neutral value so
    that a signal with no discriminating power neither helps nor hurts ranking.
    """

    if not scores:
        return []

    lowest = min(scores)
    highest = max(scores)
    span = highest - lowest

    if span == 0:
        # No variance -> the signal carries no ranking information.
        return [0.5 for _ in scores]

    return [(score - lowest) / span for score in scores]


def entity_coverage_score(chunk: str, entities: Iterable[str]) -> float:
    """Fraction of distinct entities that appear in the chunk (0..1).

    Coverage is used instead of a raw count so that a chunk repeating a single
    entity many times cannot dominate a chunk that mentions several distinct
    relevant entities once each.
    """

    unique_entities = {e.lower() for e in entities if e and e.strip()}

    if not unique_entities:
        return 0.0

    chunk_lower = chunk.lower()
    matched = sum(1 for entity in unique_entities if entity in chunk_lower)

    return matched / len(unique_entities)


def keyword_overlap_score(chunk: str, query: str) -> float:
    """Fraction of distinct query terms present in the chunk (0..1)."""

    query_terms = set(tokenize(query))

    if not query_terms:
        return 0.0

    chunk_terms = set(tokenize(chunk))
    matched = query_terms & chunk_terms

    return len(matched) / len(query_terms)


def hybrid_rank(
    candidates: Sequence[dict],
    entities: Iterable[str],
    query: str,
    weights: dict[str, float] | None = None,
    top_k: int | None = None,
) -> list[ScoredChunk]:
    """Fuse semantic, entity, and keyword signals into one ranked list.

    Args:
        candidates: sequence of dicts, each with a ``"text"`` key and an optional
            ``"semantic_score"`` key (higher == more similar). Missing semantic
            scores default to 0 before normalization.
        entities: detected/expanded entities used for the entity-coverage signal.
        query: the (original) user question used for the keyword-overlap signal.
        weights: optional override of :data:`DEFAULT_WEIGHTS`.
        top_k: if given, return only the best ``top_k`` chunks.

    Returns:
        A list of :class:`ScoredChunk`, sorted by fused score (descending).
        Original candidate order is preserved for ties (stable sort), so a
        higher-ranked semantic hit wins when all else is equal.
    """

    weights = weights or DEFAULT_WEIGHTS
    entities = list(entities)

    if not candidates:
        return []

    raw_semantic = [float(c.get("semantic_score", 0.0)) for c in candidates]
    normalized_semantic = min_max_normalize(raw_semantic)

    scored: list[ScoredChunk] = []

    for candidate, semantic in zip(candidates, normalized_semantic):
        text = candidate["text"]

        entity_score = entity_coverage_score(text, entities)
        keyword_score = keyword_overlap_score(text, query)

        fused = (
            weights["semantic"] * semantic
            + weights["entity"] * entity_score
            + weights["keyword"] * keyword_score
        )

        scored.append(
            ScoredChunk(
                text=text,
                score=fused,
                components={
                    "semantic": semantic,
                    "entity": entity_score,
                    "keyword": keyword_score,
                },
            )
        )

    # Stable sort keeps the semantic ordering as the tie-breaker.
    scored.sort(key=lambda sc: sc.score, reverse=True)

    if top_k is not None:
        scored = scored[:top_k]

    return scored


def reciprocal_rank_fusion(
    ranked_lists: Sequence[Sequence[str]],
    k: int = 60,
    top_k: int | None = None,
) -> list[ScoredChunk]:
    """Combine several ranked lists of chunks with Reciprocal Rank Fusion.

    RRF is a robust rank-based combiner that needs no score normalization, which
    makes it a good default when fusing lists that carry incomparable scores
    (e.g. semantic distances vs. graph relevance). Each list contributes
    ``1 / (k + rank)`` per item, where ``rank`` is 0-based.

    Args:
        ranked_lists: each inner sequence is an ordered list of chunk texts,
            best first.
        k: RRF damping constant (larger => flatter contribution of top ranks).
        top_k: if given, return only the best ``top_k`` fused chunks.

    Returns:
        Fused chunks sorted by RRF score (descending).
    """

    fused_scores: dict[str, float] = {}
    first_seen: dict[str, int] = {}
    order = 0

    for ranked in ranked_lists:
        for rank, text in enumerate(ranked):
            fused_scores[text] = fused_scores.get(text, 0.0) + 1.0 / (k + rank)
            if text not in first_seen:
                first_seen[text] = order
                order += 1

    scored = [
        ScoredChunk(text=text, score=score, components={"rrf": score})
        for text, score in fused_scores.items()
    ]

    # Sort by fused score, breaking ties by first appearance for determinism.
    scored.sort(key=lambda sc: (-sc.score, first_seen[sc.text]))

    if top_k is not None:
        scored = scored[:top_k]

    return scored
