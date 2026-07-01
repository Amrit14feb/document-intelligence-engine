import json
import os


# ===================================
# LOAD ENTITIES
# ===================================

with open(
    "data/knowledge/entities.json",
    "r",
    encoding="utf-8"
) as f:

    entities = json.load(f)


# ===================================
# LOAD RELATIONSHIPS
# ===================================

with open(
    "data/knowledge/relationships.json",
    "r",
    encoding="utf-8"
) as f:

    relationships = json.load(f)


# ===================================
# LOAD CONCEPTS
# ===================================

with open(
    "data/knowledge/concepts.json",
    "r",
    encoding="utf-8"
) as f:

    concepts = json.load(f)


# ===================================
# BUILD KNOWLEDGE GRAPH
# ===================================

knowledge_graph = {

    "entities": entities,

    "relationships": relationships,

    "concepts": concepts

}


# ===================================
# SAVE
# ===================================

os.makedirs(
    "data/knowledge",
    exist_ok=True
)

with open(
    "data/knowledge/knowledge_graph.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        knowledge_graph,
        f,
        indent=4,
        ensure_ascii=False
    )


print("\n===================================")
print("KNOWLEDGE GRAPH CREATED")
print("Saved:")
print("data/knowledge/knowledge_graph.json")
print("===================================\n")