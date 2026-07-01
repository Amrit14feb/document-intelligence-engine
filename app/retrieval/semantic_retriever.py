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


# -------------------------
# RETRIEVAL WITH SCORES
# -------------------------

def search_chunks_with_scores(query, n_results=5):
    """Retrieve chunks together with a semantic similarity score.

    This is an additive companion to :func:`search_chunks`. The plain
    ``search_chunks`` throws away ChromaDB's distances, which makes real hybrid
    ranking impossible. Here we expose each chunk alongside a similarity score
    in roughly [0, 1] (higher == more similar) so the hybrid scorer can fuse
    semantic relevance with entity/keyword signals.

    Returns:
        A list of dicts: ``{"text": <chunk>, "semantic_score": <float>}``,
        ordered as returned by the vector store (best first).
    """

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    documents = results["documents"][0]

    # ChromaDB returns distances (smaller == closer). Convert to a bounded
    # similarity so callers get a "higher is better" signal regardless of the
    # underlying metric. 1 / (1 + distance) is metric-agnostic and monotonic.
    distances = results.get("distances")
    if distances and distances[0] is not None:
        distances = distances[0]
    else:
        distances = [0.0] * len(documents)

    scored = []
    for doc, distance in zip(documents, distances):
        similarity = 1.0 / (1.0 + float(distance))
        scored.append({"text": doc, "semantic_score": similarity})

    return scored