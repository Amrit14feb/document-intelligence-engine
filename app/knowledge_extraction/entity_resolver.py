"""Entity resolution (project priority #3).

Maps surface entity mentions to a single canonical form so the same real-world
entity is not scattered across near-duplicate nodes (e.g. ``"LEON3"`` vs
``"LEON3 processor"``, ``"satoc"`` vs ``"SAToC"``, ``"OBDH"`` vs
``"OBDH/OBC modules"``). Cleaner entities directly improve graph traversal,
graph retrieval, and hybrid ranking downstream.

Resolution proceeds in three stages, cheapest first:

1. Alias lookup       -- explicit alias -> canonical map (authoritative).
2. Exact normalized   -- case/punctuation/whitespace-insensitive equality.
3. Fuzzy match        -- ``difflib`` ratio above a threshold (stdlib only).

The module is pure: callers supply the known entity list and alias map, so it
is fully testable without touching disk. Thin loaders are provided for
convenience but are optional.

Design philosophy (CLAUDE.md): single responsibility, no external deps,
reusable pure functions, readable over clever.
"""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
import json
import re
from typing import Iterable, Mapping

# Default fuzzy-match acceptance threshold. Chosen conservatively so that only
# genuine variants merge; unrelated short strings ("FPGA" vs "VHDL") stay apart.
DEFAULT_FUZZY_THRESHOLD = 0.86

_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class ResolutionResult:
    """Outcome of resolving a single mention."""

    canonical: str
    method: str  # one of: "alias", "exact", "fuzzy", "unresolved"
    score: float  # 1.0 for alias/exact, ratio for fuzzy, 0.0 for unresolved


def normalize_entity(text: str) -> str:
    """Return a comparison key: lowercased, punctuation/space collapsed.

    ``"OBDH/OBC modules"`` -> ``"obdh obc modules"`` (spaces normalized), which
    lets exact-normalized matching ignore incidental punctuation differences.
    """

    lowered = text.lower().strip()
    collapsed = _NORMALIZE_RE.sub(" ", lowered)
    return collapsed.strip()


def _tokens(text: str) -> set[str]:
    """Normalized token set of an entity name."""

    return set(normalize_entity(text).split())


def is_token_subset(short: str, long: str) -> bool:
    """True if ``short``'s tokens are a proper subset of ``long``'s tokens.

    Captures abbreviation/expansion pairs that character-ratio fuzzy matching
    misses, e.g. ``"LEON3"`` ⊆ ``"LEON3 processor"`` and ``"OBDH"`` ⊆
    ``"OBDH OBC modules"``. Requires a proper subset so identical names are left
    to exact matching and unrelated names never merge.
    """

    short_tokens = _tokens(short)
    long_tokens = _tokens(long)
    if not short_tokens or short_tokens == long_tokens:
        return False
    return short_tokens < long_tokens


def flatten_entities(entities: Iterable | Mapping) -> list[str]:
    """Flatten the categorized entities structure into a flat unique list.

    Accepts either the ``{category: [names]}`` mapping used in
    ``entities.json`` or an already-flat iterable of names.
    """

    names: list[str] = []

    if isinstance(entities, Mapping):
        for category_values in entities.values():
            names.extend(category_values)
    else:
        names.extend(entities)

    # Preserve first-seen order while de-duplicating.
    seen: set[str] = set()
    unique: list[str] = []
    for name in names:
        if name not in seen:
            seen.add(name)
            unique.append(name)
    return unique


def build_canonical_index(canonical_entities: Iterable[str]) -> dict[str, str]:
    """Build a normalized-key -> canonical-name index for exact matching."""

    index: dict[str, str] = {}
    for name in canonical_entities:
        index.setdefault(normalize_entity(name), name)
    return index


def resolve_entity(
    mention: str,
    canonical_index: Mapping[str, str],
    aliases: Mapping[str, str] | None = None,
    fuzzy_threshold: float = DEFAULT_FUZZY_THRESHOLD,
) -> ResolutionResult:
    """Resolve a single mention to a canonical entity.

    Args:
        mention: the raw surface form to resolve.
        canonical_index: normalized-key -> canonical-name (see
            :func:`build_canonical_index`).
        aliases: optional alias -> canonical map (keys matched case-insensitively).
        fuzzy_threshold: minimum ``difflib`` ratio to accept a fuzzy match.

    Returns:
        A :class:`ResolutionResult`. If nothing matches, ``canonical`` is the
        original (stripped) mention and ``method`` is ``"unresolved"`` so callers
        never lose data.
    """

    stripped = mention.strip()
    key = normalize_entity(mention)

    # 1) Alias lookup (authoritative).
    if aliases:
        alias_hit = aliases.get(stripped.lower()) or aliases.get(key)
        if alias_hit:
            return ResolutionResult(alias_hit, "alias", 1.0)

    # 2) Exact normalized match.
    exact = canonical_index.get(key)
    if exact:
        return ResolutionResult(exact, "exact", 1.0)

    # 3) Token-subset match (abbreviation -> fuller canonical name).
    # Prefer the tightest superset (fewest extra tokens) to avoid over-merging.
    subset_best: str | None = None
    subset_extra = None
    for cand_name in canonical_index.values():
        if is_token_subset(mention, cand_name):
            extra = len(_tokens(cand_name)) - len(_tokens(mention))
            if subset_extra is None or extra < subset_extra:
                subset_extra = extra
                subset_best = cand_name
    if subset_best is not None:
        return ResolutionResult(subset_best, "subset", 1.0)

    # 4) Fuzzy match against known canonical keys.
    best_name = stripped
    best_score = 0.0
    for cand_key, cand_name in canonical_index.items():
        ratio = SequenceMatcher(None, key, cand_key).ratio()
        if ratio > best_score:
            best_score = ratio
            best_name = cand_name

    if best_score >= fuzzy_threshold:
        return ResolutionResult(best_name, "fuzzy", best_score)

    return ResolutionResult(stripped, "unresolved", 0.0)


def resolve_all(
    mentions: Iterable[str],
    canonical_index: Mapping[str, str],
    aliases: Mapping[str, str] | None = None,
    fuzzy_threshold: float = DEFAULT_FUZZY_THRESHOLD,
) -> list[str]:
    """Resolve many mentions to canonical forms, de-duplicated, order-preserving."""

    resolved: list[str] = []
    seen: set[str] = set()
    for mention in mentions:
        result = resolve_entity(mention, canonical_index, aliases, fuzzy_threshold)
        if result.canonical not in seen:
            seen.add(result.canonical)
            resolved.append(result.canonical)
    return resolved


def deduplicate_entities(
    entities: Iterable[str],
    fuzzy_threshold: float = DEFAULT_FUZZY_THRESHOLD,
) -> dict[str, str]:
    """Collapse near-duplicate entities into representatives.

    Returns a mapping ``{original -> representative}``. The longest surviving
    variant is kept as the representative (it usually carries the most context,
    e.g. ``"LEON3 processor"`` over ``"LEON3"``).
    """

    ordered = flatten_entities(entities)
    # Longer names first so they become representatives.
    ordered_sorted = sorted(ordered, key=len, reverse=True)

    representatives: list[str] = []
    mapping: dict[str, str] = {}

    for name in ordered_sorted:
        key = normalize_entity(name)
        match = None
        for rep in representatives:
            ratio = SequenceMatcher(None, key, normalize_entity(rep)).ratio()
            # Merge on high char-similarity OR abbreviation/expansion containment.
            if ratio >= fuzzy_threshold or is_token_subset(name, rep):
                match = rep
                break
        if match is None:
            representatives.append(name)
            mapping[name] = name
        else:
            mapping[name] = match

    return mapping


# ------------------------------------------------------------------
# Optional thin loaders (I/O kept out of the pure functions above).
# ------------------------------------------------------------------

def load_entities(path: str = "data/knowledge/entities.json") -> list[str]:
    with open(path, "r", encoding="utf-8") as handle:
        return flatten_entities(json.load(handle))


def load_aliases(path: str = "data/knowledge/entity_aliases.json") -> dict[str, str]:
    with open(path, "r", encoding="utf-8") as handle:
        raw = json.load(handle)
    # Normalize alias keys to lowercase for case-insensitive lookup.
    return {alias.lower(): canonical for alias, canonical in raw.items()}
