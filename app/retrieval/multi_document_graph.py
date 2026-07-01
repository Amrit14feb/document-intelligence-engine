"""Multi-document GraphRAG (project priority #7).

The engine currently reasons over a single document's knowledge graph. This
module is the foundation for cross-document reasoning: it merges the
relationship graphs of several documents into one global graph while preserving
*provenance* (which document each edge came from) and applying entity resolution
so the same entity across documents becomes a single node.

It is deliberately additive and pure: it operates on in-memory relationship
lists tagged with a ``doc_id`` and does not disturb the single-document
pipeline. Thin loaders help assemble inputs from disk.

Design philosophy (CLAUDE.md): new capability as a new module, loosely coupled,
reuses :mod:`app.knowledge_extraction.entity_resolver` rather than duplicating
resolution logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Iterable, Sequence

from app.knowledge_extraction.entity_resolver import (
    build_canonical_index,
    resolve_entity,
)


@dataclass(frozen=True)
class GlobalEdge:
    """A relationship in the merged graph, tagged with its source documents."""

    source: str
    relationship: str
    target: str
    doc_ids: frozenset[str]


@dataclass
class GlobalGraph:
    """Merged multi-document graph with provenance and adjacency."""

    edges: list[GlobalEdge] = field(default_factory=list)
    adjacency: dict[str, list[GlobalEdge]] = field(default_factory=dict)

    def documents_for(self, entity: str) -> set[str]:
        """Return the set of document ids that mention ``entity``."""

        docs: set[str] = set()
        for edge in self.adjacency.get(entity, []):
            docs.update(edge.doc_ids)
        return docs

    def cross_document_entities(self) -> list[str]:
        """Entities that appear in more than one document (bridge nodes)."""

        return sorted(
            entity
            for entity in self.adjacency
            if len(self.documents_for(entity)) > 1
        )


def _resolve(name: str, canonical_index, aliases) -> str:
    if not canonical_index and not aliases:
        return name.strip()
    return resolve_entity(name, canonical_index, aliases).canonical


def merge_documents(
    documents: Sequence[dict],
    canonical_entities: Iterable[str] | None = None,
    aliases: dict[str, str] | None = None,
) -> GlobalGraph:
    """Merge per-document relationships into a single provenance-aware graph.

    Args:
        documents: each dict has ``"doc_id"`` and ``"relationships"`` (a list of
            ``{"source", "relationship", "target"}`` dicts).
        canonical_entities: optional global entity list used to unify entities
            across documents via :mod:`entity_resolver`. If omitted, entity
            names are only stripped (no cross-doc unification).
        aliases: optional alias -> canonical map.

    Returns:
        A :class:`GlobalGraph`. Identical (source, relationship, target) triples
        from different documents are merged into one edge whose ``doc_ids``
        records every contributing document.
    """

    canonical_index = (
        build_canonical_index(canonical_entities) if canonical_entities else {}
    )
    aliases = aliases or {}

    # Deduplicate edges by their resolved triple; accumulate provenance.
    merged: dict[tuple[str, str, str], set[str]] = {}

    for document in documents:
        doc_id = document.get("doc_id", "UNKNOWN")
        for rel in document.get("relationships", []):
            source = _resolve(rel["source"], canonical_index, aliases)
            target = _resolve(rel["target"], canonical_index, aliases)
            label = rel.get("relationship", "related_to")
            key = (source, label, target)
            merged.setdefault(key, set()).add(doc_id)

    graph = GlobalGraph()
    for (source, label, target), doc_ids in merged.items():
        edge = GlobalEdge(source, label, target, frozenset(doc_ids))
        graph.edges.append(edge)
        graph.adjacency.setdefault(source, []).append(edge)
        graph.adjacency.setdefault(target, []).append(edge)

    return graph


def get_global_entity_context(entity: str, graph: GlobalGraph) -> str:
    """Render an entity's relationships across all documents, with provenance.

    Mirrors the single-document ``graph_retriever.get_entity_context`` output but
    annotates each fact with the documents that support it, which is what makes
    cross-document answers explainable.
    """

    lines: list[str] = []
    seen: set[tuple[str, str, str]] = set()

    for edge in graph.adjacency.get(entity, []):
        triple = (edge.source, edge.relationship, edge.target)
        if triple in seen:
            continue
        seen.add(triple)
        docs = ", ".join(sorted(edge.doc_ids))
        lines.append(
            f"{edge.source} {edge.relationship} {edge.target} [{docs}]"
        )

    return "\n".join(lines)


# ------------------------------------------------------------------
# Optional thin loaders.
# ------------------------------------------------------------------

def load_document_relationships(doc_id: str, path: str) -> dict:
    """Load one document's relationships into the merge-ready shape."""

    with open(path, "r", encoding="utf-8") as handle:
        relationships = json.load(handle)
    return {"doc_id": doc_id, "relationships": relationships}
