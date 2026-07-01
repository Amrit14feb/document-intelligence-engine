import json

# ---------- LOAD NORMALIZED ----------

with open(
    "data/normalized/normalized_document.json",
    "r",
    encoding="utf-8"
) as f:

    document=json.load(f)

# ---------- CHUNK SETTINGS ----------

CHUNK_SIZE=1200

OVERLAP=200

# ---------- CHUNK FUNCTION ----------

import re

def create_chunks(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    chunks = []

    current_chunk = ""

    for sentence in sentences:

        if len(current_chunk) + len(sentence) < 1200:

            current_chunk += " " + sentence

        else:

            chunks.append(
                current_chunk.strip()
            )

            current_chunk = sentence

    if current_chunk:

        chunks.append(
            current_chunk.strip()
        )

    return chunks
# ---------- BUILD CHUNKS ----------

all_chunks=[]

chunk_id=1

for page in document["pages"]:

    text=page["clean_text"]

    page_chunks=create_chunks(text)

    for chunk in page_chunks:

        all_chunks.append({

            "chunk_id":f"CHUNK_{chunk_id}",

            "page_number":page["page_number"],

            "text":chunk,

            "char_count":len(chunk)
        })

        chunk_id+=1

# ---------- SAVE ----------

output={

    "doc_id":document["doc_id"],

    "title":document["title"],

    "chunks":all_chunks
}

with open(
    "data/normalized/chunked_document.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        output,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nCHUNKING COMPLETE\n")

print(f"Chunks created: {len(all_chunks)}")