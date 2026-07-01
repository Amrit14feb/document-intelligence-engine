import json
import os

from app.reasoning.llm import llm


# =====================================
# LOAD CHUNKED DOCUMENT
# =====================================

with open(
    "data/normalized/chunked_document.json",
    "r",
    encoding="utf-8"
) as f:
    document = json.load(f)


# =====================================
# TAKE FIRST 10 CHUNKS
# =====================================

sample_text = ""

for chunk in document["chunks"][:10]:

    sample_text += chunk["text"]
    sample_text += "\n\n"


# =====================================
# PROMPT
# =====================================

prompt = f"""
You are an expert document intelligence system.

Analyze the document and extract all important entities.

Return ONLY valid JSON.

Format:

{{
    "organizations": [],
    "people": [],
    "technologies": [],
    "locations": []
}}

Rules:
1. Do not explain anything.
2. Return JSON only.
3. Remove duplicates.
4. Extract only important entities.

DOCUMENT:

{sample_text}
"""


# =====================================
# LLM CALL
# =====================================

print("\nExtracting entities...\n")

response = llm.invoke(prompt)

raw_output = response.content.strip()

print(raw_output)


# =====================================
# PARSE JSON
# =====================================

try:

    entities = json.loads(raw_output)

except Exception as e:

    print("\nJSON Parsing Error\n")
    print(e)

    exit()


# =====================================
# CREATE OUTPUT FOLDER
# =====================================

os.makedirs(
    "data/knowledge",
    exist_ok=True
)


# =====================================
# SAVE FILE
# =====================================

with open(
    "data/knowledge/entities.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        entities,
        f,
        indent=4,
        ensure_ascii=False
    )


print("\n=====================================")
print("ENTITY EXTRACTION COMPLETE")
print("Saved:")
print("data/knowledge/entities.json")
print("=====================================\n")