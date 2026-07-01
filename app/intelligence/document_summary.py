from app.retrieval.semantic_retriever import search_chunks
from app.reasoning.context_builder import build_context
from app.reasoning.llm import llm


def summarize_document():

    results = search_chunks(
        "document overview research objective technology architecture contributions",
        n_results=20
    )

    context = build_context(results)

    prompt = f"""
Create an executive summary.

Include:

1. Objective
2. Technologies
3. Organizations
4. Contributions
5. Future Work

DOCUMENT:

{context}
"""

    response = llm.invoke(prompt)

    return response.content