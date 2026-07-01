import json
import chromadb

from sentence_transformers import SentenceTransformer

# ---------- LOAD CHUNKS ----------

with open(
    "data/normalized/chunked_document.json",
    "r",
    encoding="utf-8"
) as f:

    document=json.load(f)

# ---------- LOAD MODEL ----------

print("\nLoading embedding model...\n")

model=SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ---------- VECTOR DATABASE ----------

client=chromadb.PersistentClient(
    path="data/vectors"
)

collection=client.get_or_create_collection(
    "documents"
)

# ---------- EMBEDDING LOOP ----------

for chunk in document["chunks"]:

    embedding=model.encode(
        chunk["text"]
    ).tolist()

    collection.add(

        ids=[chunk["chunk_id"]],

        embeddings=[embedding],

        documents=[chunk["text"]],

        metadatas=[{

            "page":chunk["page_number"]
        }]
    )

print("\nEMBEDDING COMPLETE\n")

print(
    f"Stored chunks: {len(document['chunks'])}"
)