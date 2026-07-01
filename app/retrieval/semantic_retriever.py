import chromadb
from sentence_transformers import SentenceTransformer

# -------------------------
# LOAD MODEL ONCE
# -------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -------------------------
# LOAD VECTOR DB ONCE
# -------------------------

client = chromadb.PersistentClient(
    path="data/vectors"
)

collection = client.get_collection(
    "documents"
)

# -------------------------
# RETRIEVAL FUNCTION
# -------------------------

def search_chunks(query, n_results=5):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    print("\nTOP RETRIEVED CHUNKS\n")

    for i, doc in enumerate(results["documents"][0]):

        print("\n")
        print(f"CHUNK {i+1}\n")
        print(doc[:700])
        print("-" * 80)

    return results["documents"][0]