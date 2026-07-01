import json
import os

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
# PREPARE SAMPLE TEXT
# ==========================================

sample_text = ""

for chunk in document["chunks"][:15]:

    sample_text += chunk["text"]
    sample_text += "\n\n"


# ==========================================
# PROMPT
# ==========================================

prompt = f"""
You are an expert knowledge graph extraction system.

Extract relationships between entities.

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

Examples:

[
    {{
        "source": "SpaceLab",
        "relationship": "developed",
        "target": "FloripaSat-1"
    }},
    {{
        "source": "ESA",
        "relationship": "funded",
        "target": "Mission"
    }}
]

Rules:

1. Extract factual relationships only.
2. No explanations.
3. No markdown.
4. Return JSON only.
5. Avoid duplicates.

DOCUMENT:

{sample_text}
"""


# ==========================================
# CALL LLM
# ==========================================

print("\nExtracting relationships...\n")

response = llm.invoke(prompt)

raw_output = response.content.strip()

print(raw_output)


# ==========================================
# PARSE JSON
# ==========================================

try:

    relationships = json.loads(raw_output)

except Exception as e:

    print("\nJSON ERROR\n")
    print(e)
    exit()


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
        relationships,
        f,
        indent=4,
        ensure_ascii=False
    )


print("\n===================================")
print("RELATIONSHIP EXTRACTION COMPLETE")
print("Saved:")
print("data/knowledge/relationships.json")
print("===================================")