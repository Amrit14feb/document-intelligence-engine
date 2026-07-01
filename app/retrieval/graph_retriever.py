import json


# ==========================
# LOAD RELATIONSHIPS
# ==========================

with open(
    "data/knowledge/relationships.json",
    "r",
    encoding="utf-8"
) as f:

    relationships = json.load(f)


# ==========================
# GRAPH SEARCH
# ==========================

def get_entity_context(entity):

    results = []

    for rel in relationships:

        source_match = (
            entity.lower()
            in rel["source"].lower()
        )

        target_match = (
            entity.lower()
            in rel["target"].lower()
        )

        if source_match or target_match:

            results.append(
                f"{rel['source']} "
                f"{rel['relationship']} "
                f"{rel['target']}"
            )
    return "\n".join(results)