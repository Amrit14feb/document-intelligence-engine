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
# PREPARE SAMPLE TEXT
# ==========================================

sample_text = ""

for chunk in document["chunks"][:20]:

    sample_text += chunk["text"]
    sample_text += "\n\n"


# ==========================================
# PROMPT
# ==========================================

prompt = f"""
You are an expert research analyst.

Analyze the document and identify the major concepts,
themes and research areas discussed.

Return ONLY valid JSON.

Format:

{{
    "core_concepts": []
}}

Rules:

1. Extract concepts, not entities.
2. Extract research themes.
3. Remove duplicates.
4. Keep concepts concise.
5. Return JSON only.

Example:

{{
    "core_concepts": [
        "Artificial Intelligence",
        "Machine Learning",
        "Computer Vision"
    ]
}}

DOCUMENT:

{sample_text}
"""


# ==========================================
# CALL LLM
# ==========================================

print("\nExtracting concepts...\n")

response = llm.invoke(prompt)

raw_output = response.content.strip()

print(raw_output)

# -----------------------------
# REMOVE MARKDOWN WRAPPERS
# -----------------------------

if raw_output.startswith("```json"):
    raw_output = raw_output.replace("```json", "")

if raw_output.startswith("```"):
    raw_output = raw_output.replace("```", "")

if raw_output.endswith("```"):
    raw_output = raw_output[:-3]

raw_output = raw_output.strip()

# -----------------------------
# PARSE JSON
# -----------------------------

try:

    concepts = json.loads(raw_output)

except Exception as e:

    print("\nJSON ERROR\n")
    print(e)

    print("\nRAW OUTPUT:\n")
    print(raw_output)

    exit()


# ==========================================
# SAVE
# ==========================================

os.makedirs(
    "data/knowledge",
    exist_ok=True
)

with open(
    "data/knowledge/concepts.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        concepts,
        f,
        indent=4,
        ensure_ascii=False
    )


print("\n===================================")
print("CONCEPT EXTRACTION COMPLETE")
print("Saved:")
print("data/knowledge/concepts.json")
print("===================================")