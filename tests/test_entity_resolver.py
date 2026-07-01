"""Unit tests for app.knowledge_extraction.entity_resolver (self-contained)."""

from app.knowledge_extraction.entity_resolver import (
    normalize_entity,
    flatten_entities,
    build_canonical_index,
    resolve_entity,
    resolve_all,
    deduplicate_entities,
)

CANONICAL = ["FPGA", "RISC-V", "LEON3 processor", "OBDH/OBC modules", "SAToC"]
ALIASES = {"satoc": "SAToC", "fpga": "FPGA", "risc-v": "RISC-V"}


def _index():
    return build_canonical_index(CANONICAL)


def test_normalize_collapses_punctuation_and_case():
    assert normalize_entity("OBDH/OBC modules") == "obdh obc modules"
    assert normalize_entity("RISC-V") == "risc v"


def test_flatten_entities_from_mapping():
    mapping = {"tech": ["FPGA", "VHDL"], "org": ["UFSC"]}
    assert flatten_entities(mapping) == ["FPGA", "VHDL", "UFSC"]


def test_flatten_entities_dedupes():
    assert flatten_entities(["A", "B", "A"]) == ["A", "B"]


def test_resolve_via_alias():
    result = resolve_entity("satoc", _index(), ALIASES)
    assert result.canonical == "SAToC"
    assert result.method == "alias"


def test_resolve_exact_normalized():
    # Different punctuation but same normalized key -> exact match.
    result = resolve_entity("risc v", _index(), aliases=None)
    assert result.canonical == "RISC-V"
    assert result.method == "exact"


def test_resolve_subset_variant():
    # "LEON3" is an abbreviation of the fuller canonical "LEON3 processor".
    result = resolve_entity("LEON3", _index(), aliases=None)
    assert result.canonical == "LEON3 processor"
    assert result.method == "subset"


def test_resolve_fuzzy_typo():
    # A genuine typo resolves via char-ratio fuzzy matching.
    result = resolve_entity("FPGAA", _index(), aliases=None)
    assert result.canonical == "FPGA"
    assert result.method == "fuzzy"
    assert result.score >= 0.86


def test_resolve_unresolved_returns_original():
    result = resolve_entity("CompletelyUnrelatedThing", _index(), aliases=None)
    assert result.method == "unresolved"
    assert result.canonical == "CompletelyUnrelatedThing"


def test_resolve_all_dedupes_to_canonical():
    mentions = ["satoc", "SAToC", "fpga", "FPGA"]
    assert resolve_all(mentions, _index(), ALIASES) == ["SAToC", "FPGA"]


def test_deduplicate_entities_merges_variants():
    mapping = deduplicate_entities(["LEON3", "LEON3 processor", "FPGA"])
    # LEON3 variants collapse onto the longer representative.
    assert mapping["LEON3"] == "LEON3 processor"
    assert mapping["LEON3 processor"] == "LEON3 processor"
    assert mapping["FPGA"] == "FPGA"


def test_deduplicate_keeps_distinct_entities_apart():
    mapping = deduplicate_entities(["FPGA", "VHDL"])
    assert mapping["FPGA"] == "FPGA"
    assert mapping["VHDL"] == "VHDL"


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
