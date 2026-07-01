import json

from app.reasoning.llm import llm


# --------------------
# LOAD CHUNKS
# --------------------

with open(
    "data/normalized/chunked_document.json",
    "r",
    encoding="utf-8"
) as f:

    document = json.load(f)


# --------------------
# TAKE FIRST FEW CHUNKS
# --------------------

sample_text = ""

for chunk in document["chunks"][:5]:

    sample_text += chunk["text"]
    sample_text += "\n\n"


# --------------------
# PROMPT
# --------------------

prompt = f"""
You are an expert document intelligence engine.

Analyze the document below.

Return ONLY valid JSON.

Format:

{{
    "domain":"",
    "subdomain":"",
    "document_type":"",
    "topics":[],
    "keywords":[]
}}

DOCUMENT:

{sample_text}
"""


# --------------------
# ASK LLM
# --------------------

response = llm.invoke(prompt)

metadata = json.loads(response.content)

with open(
    "data/normalized/document_metadata.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        metadata,
        f,
        indent=4,
        ensure_ascii=False
    )

print("DOCUMENT CLASSIFIED")