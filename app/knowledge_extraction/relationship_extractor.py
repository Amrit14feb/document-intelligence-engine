import json
import os
import time

from app.reasoning.llm import llm

# ==========================================
# LOAD CHUNKS
# ==========================================

with open(
    "data/normalized/chunked_document.json",
    "r",
    encoding="utf-8"
) as f:

    document = json.load(f)

# ==========================================
# LOAD ENTITIES
# ==========================================

with open(
    "data/knowledge/entities.json",
    "r",
    encoding="utf-8"
) as f:

    entities = json.load(f)

# ==========================================
# STORAGE
# ==========================================

all_relationships = []

chunks = document["chunks"]

print(f"\nTotal chunks: {len(chunks)}\n")

# ==========================================
# PROCESS EACH CHUNK
# ==========================================

for idx, chunk in enumerate(chunks):

    print(f"\nProcessing Chunk {idx+1}/{len(chunks)}")

    prompt = f"""
You are an expert knowledge graph extraction system.

Extract relationships from this chunk.

Known entities:

{json.dumps(entities, indent=2)}

Return ONLY valid JSON.

Format:

[
    {{
        "source": "",
        "relationship": "",
        "target": ""
    }}
]

Rules:

1. Extract factual relationships only.
2. Use concise relationship names.
3. No explanations.
4. No markdown.
5. Return JSON only.
6. If no relationship exists return []

CHUNK:

{chunk["text"]}
"""

    try:

        response = llm.invoke(prompt)

        raw_output = response.content.strip()

        relationships = json.loads(raw_output)

        all_relationships.extend(
            relationships
        )

        print(
            f"Relationships found: {len(relationships)}"
        )

    except Exception as e:

        print(
            f"Error in chunk {idx+1}: {e}"
        )

    time.sleep(1)

# ==========================================
# DEDUPLICATE
# ==========================================

unique = {}

for rel in all_relationships:

    key = (
        rel.get("source", "").strip().lower(),
        rel.get("relationship", "").strip().lower(),
        rel.get("target", "").strip().lower()
    )

    unique[key] = rel

final_relationships = list(
    unique.values()
)

# ==========================================
# SAVE
# ==========================================

os.makedirs(
    "data/knowledge",
    exist_ok=True
)

with open(
    "data/knowledge/relationships.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        final_relationships,
        f,
        indent=4,
        ensure_ascii=False
    )

# ==========================================
# DONE
# ==========================================

print("\n===================================")
print(
    f"TOTAL RELATIONSHIPS: {len(final_relationships)}"
)
print("Saved:")
print("data/knowledge/relationships.json")
print("===================================")