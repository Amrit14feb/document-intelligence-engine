"""Unit tests for app.intelligence.citation_generator (self-contained)."""

from app.intelligence.citation_generator import (
    generate_citations,
    format_sources,
    build_chunk_lookup,
)

CHUNKS = [
    {"chunk_id": "CHUNK_1", "page_number": 1, "text": "The objective of SAToC is deep-space endurance."},
    {"chunk_id": "CHUNK_2", "page_number": 3, "text": "COTS components reduce cost significantly."},
]


def test_build_lookup_normalizes_whitespace():
    lookup = build_chunk_lookup(CHUNKS)
    assert "the objective of satoc is deep-space endurance." in lookup


def test_generate_citations_exact_match():
    citations = generate_citations([CHUNKS[0]["text"]], CHUNKS)
    assert len(citations) == 1
    assert citations[0].chunk_id == "CHUNK_1"
    assert citations[0].page_number == 1
    assert citations[0].index == 1


def test_generate_citations_matches_despite_whitespace():
    padded = "  The objective of SAToC   is deep-space endurance.  "
    citations = generate_citations([padded], CHUNKS)
    assert citations[0].chunk_id == "CHUNK_1"


def test_generate_citations_prefix_match():
    # Retrieved text is a truncated prefix of the stored chunk.
    truncated = "COTS components reduce"
    citations = generate_citations([truncated], CHUNKS)
    assert citations[0].chunk_id == "CHUNK_2"


def test_generate_citations_unmatched_still_counted():
    citations = generate_citations(["totally different text"], CHUNKS)
    assert citations[0].chunk_id.startswith("UNMATCHED_")
    assert citations[0].page_number is None


def test_generate_citations_numbering_is_sequential():
    citations = generate_citations([CHUNKS[0]["text"], CHUNKS[1]["text"]], CHUNKS)
    assert [c.index for c in citations] == [1, 2]


def test_format_sources_contains_markers_and_pages():
    citations = generate_citations([CHUNKS[0]["text"]], CHUNKS)
    rendered = format_sources(citations)
    assert "[1]" in rendered
    assert "CHUNK_1" in rendered
    assert "page 1" in rendered


def test_format_sources_empty():
    assert "No supporting chunks" in format_sources([])


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
