import json


# ==========================================
# LOAD RELATIONSHIPS
# ==========================================

with open(
    "data/knowledge/relationships.json",
    "r",
    encoding="utf-8"
) as f:

    RELATIONSHIPS = json.load(f)


# ==========================================
# GRAPH EXPANSION
# ==========================================

def expand_entities(
    entities,
    hops=1
):
    """
    Expand entities using graph neighbors.
    """

    expanded = set(entities)

    current = set(entities)

    for _ in range(hops):

        new_nodes = set()

        for rel in RELATIONSHIPS:

            source = rel["source"]
            target = rel["target"]

            if source in current:
                new_nodes.add(target)

            if target in current:
                new_nodes.add(source)

        expanded.update(new_nodes)

        current = new_nodes

    # --------------------------
    # FILTER
    # --------------------------

    filtered = []

    for item in expanded:

        if len(item) < 40:
            filtered.append(item)

    filtered = sorted(
        filtered,
        key=len
    )

    return filtered[:20]