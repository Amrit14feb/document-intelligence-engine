"""Citation generation (project priority #5).

Every generated answer should be traceable to the document chunks that support
it. The retrieval pipeline passes chunk *text* around (ChromaDB documents), so
this module matches retrieved text back to the source chunk records
(``chunk_id`` + ``page_number`` from ``chunked_document.json``) and formats a
"Sources" section.

Matching strategy:
    1. exact text match (fast path),
    2. normalized-prefix match (handles whitespace/truncation differences).

The module is pure -- callers pass in the chunk records -- so it is testable
without the vector store or the LLM. A thin loader is provided.

Design philosophy (CLAUDE.md): single responsibility (citations only, no
retrieval, no reasoning), reusable, readable.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Sequence

_WS_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class Citation:
    """A resolved reference from an answer back to a source chunk."""

    index: int  # 1-based citation marker, e.g. [1]
    chunk_id: str
    page_number: int | None
    snippet: str  # short preview of the cited text


def _normalize(text: str) -> str:
    return _WS_RE.sub(" ", text.strip()).lower()


def build_chunk_lookup(chunk_records: Sequence[dict]) -> dict[str, dict]:
    """Index chunk records by their normalized text for fast matching."""

    lookup: dict[str, dict] = {}
    for record in chunk_records:
        lookup.setdefault(_normalize(record.get("text", "")), record)
    return lookup


def _match_record(text: str, lookup: dict[str, dict]) -> dict | None:
    """Find the source record for a retrieved chunk text."""

    norm = _normalize(text)
    if norm in lookup:
        return lookup[norm]

    # Fall back to prefix matching: retrieved text may be truncated or padded.
    for key, record in lookup.items():
        if key.startswith(norm) or norm.startswith(key):
            return record
    return None


def generate_citations(
    retrieved_texts: Sequence[str],
    chunk_records: Sequence[dict],
    snippet_length: int = 160,
) -> list[Citation]:
    """Build ordered citations for the retrieved chunks actually used.

    Args:
        retrieved_texts: chunk texts sent to the LLM, in ranked order.
        chunk_records: the source chunk dicts (``chunk_id``, ``page_number``,
            ``text``) from ``chunked_document.json``.
        snippet_length: characters of preview text to keep per citation.

    Returns:
        A list of :class:`Citation`, one per retrieved chunk, numbered from 1.
        Unmatched chunks still get a citation (with a synthetic id) so the
        answer's evidence count stays accurate.
    """

    lookup = build_chunk_lookup(chunk_records)
    citations: list[Citation] = []

    for position, text in enumerate(retrieved_texts, start=1):
        record = _match_record(text, lookup)
        snippet = _WS_RE.sub(" ", text.strip())[:snippet_length]

        if record is not None:
            citations.append(
                Citation(
                    index=position,
                    chunk_id=record.get("chunk_id", f"UNKNOWN_{position}"),
                    page_number=record.get("page_number"),
                    snippet=snippet,
                )
            )
        else:
            citations.append(
                Citation(
                    index=position,
                    chunk_id=f"UNMATCHED_{position}",
                    page_number=None,
                    snippet=snippet,
                )
            )

    return citations


def format_sources(citations: Sequence[Citation]) -> str:
    """Render citations as a human-readable "Sources" block.

    Example::

        Sources

        [1] CHUNK_12 (page 18): The primary objective of the design ...
        [2] CHUNK_27 (page 21): COTS components were selected because ...
    """

    if not citations:
        return "Sources\n\n(No supporting chunks were retrieved.)"

    lines = ["Sources", ""]
    for citation in citations:
        page = (
            f" (page {citation.page_number})"
            if citation.page_number is not None
            else ""
        )
        lines.append(f"[{citation.index}] {citation.chunk_id}{page}: {citation.snippet}")
    return "\n".join(lines)


# ------------------------------------------------------------------
# Optional thin loader.
# ------------------------------------------------------------------

def load_chunk_records(
    path: str = "data/normalized/chunked_document.json",
) -> list[dict]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    # Support both {"chunks": [...]} and a bare list of chunk dicts.
    if isinstance(data, dict):
        return data.get("chunks", [])
    return data
