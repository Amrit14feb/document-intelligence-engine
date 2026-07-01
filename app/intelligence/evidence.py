"""Evidence assembly: citations + confidence as one reusable unit (follow-up #8).

The QA path (``rag_engine``) already appends a Sources block and a confidence
figure. The report and summary generators should carry the same grounding, but
each builds its own context and we do not want to duplicate the
citation/confidence wiring in three places.

This module folds both concerns into a single reusable step:

    * pure core  -- :func:`assemble_evidence` takes already-retrieved candidates
      and returns an :class:`Evidence` value (fully unit-testable, no I/O);
    * thin wrapper -- :func:`gather_evidence` performs the retrieval and calls
      the pure core (used at runtime);
    * :func:`attach_evidence` appends a formatted evidence appendix to any
      generated text (the one-liner the generators call).

Retrieval / entity-detection imports are done lazily inside the wrapper so this
module (and its tests) import cleanly without ChromaDB present.

Design philosophy (CLAUDE.md): single responsibility, reuse existing modules
(``hybrid_scorer``, ``citation_generator``, ``confidence_scorer``) instead of
duplicating, loosely coupled, readable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from app.retrieval.hybrid_scorer import hybrid_rank, ScoredChunk
from app.intelligence.citation_generator import (
    generate_citations,
    format_sources,
    Citation,
)
from app.intelligence.confidence_scorer import (
    confidence_from_scored_chunks,
    format_confidence,
    ConfidenceResult,
)


@dataclass
class Evidence:
    """Grounding for a generated output: ranked chunks, citations, confidence."""

    ranked_chunks: list[ScoredChunk]
    citations: list[Citation]
    confidence: ConfidenceResult

    @property
    def sources_block(self) -> str:
        return format_sources(self.citations)

    @property
    def confidence_block(self) -> str:
        return format_confidence(self.confidence)

    def appendix(self) -> str:
        """A ready-to-append block combining confidence and sources."""

        return f"{self.confidence_block}\n\n{self.sources_block}"


def assemble_evidence(
    candidates: Sequence[dict],
    entities: Sequence[str],
    query: str,
    chunk_records: Sequence[dict],
    num_graph_relationships: int = 0,
    top_k: int = 5,
) -> Evidence:
    """Build :class:`Evidence` from already-retrieved candidates (pure).

    Args:
        candidates: dicts with ``"text"`` and optional ``"semantic_score"``
            (as returned by ``search_chunks_with_scores``).
        entities: detected/expanded entities for the hybrid entity signal.
        query: the user/report query for the keyword signal and citations.
        chunk_records: source chunk dicts (``chunk_id``/``page_number``/``text``).
        num_graph_relationships: graph facts that fed the context (for confidence).
        top_k: how many ranked chunks to cite / score.

    Returns:
        An :class:`Evidence` value combining ranking, citations, and confidence.
    """

    ranked = hybrid_rank(candidates, entities=entities, query=query, top_k=top_k)
    texts = [sc.text for sc in ranked]

    citations = generate_citations(texts, chunk_records)
    confidence = confidence_from_scored_chunks(
        ranked,
        num_graph_relationships=num_graph_relationships,
    )

    return Evidence(ranked_chunks=ranked, citations=citations, confidence=confidence)


def gather_evidence(
    query: str,
    n_results: int = 20,
    top_k: int = 5,
) -> Evidence:
    """Retrieve for ``query`` and assemble evidence (thin I/O wrapper).

    Imports the retrieval/entity modules lazily so this module stays importable
    (and testable) without ChromaDB installed.
    """

    from app.retrieval.semantic_retriever import search_chunks_with_scores
    from app.retrieval.multi_entity_detector import detect_entities
    from app.intelligence.citation_generator import load_chunk_records

    candidates = search_chunks_with_scores(query, n_results=n_results)
    entities = detect_entities(query)
    chunk_records = load_chunk_records()

    return assemble_evidence(
        candidates,
        entities=entities,
        query=query,
        chunk_records=chunk_records,
        top_k=top_k,
    )


def attach_evidence(text: str, query: str, top_k: int = 5) -> str:
    """Append a confidence + sources appendix to a generated text block.

    This is the one-line helper the report/summary generators call to fold in
    grounding without duplicating retrieval logic.
    """

    evidence = gather_evidence(query, top_k=top_k)
    return f"{text}\n\n{'=' * 60}\n{evidence.appendix()}"
