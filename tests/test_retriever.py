from app.retrieval.semantic_retriever import search_chunks

results = search_chunks(
    "What is TTC?"
)

for i, chunk in enumerate(results):

    print(f"\nRESULT {i+1}\n")

    print(chunk[:500])