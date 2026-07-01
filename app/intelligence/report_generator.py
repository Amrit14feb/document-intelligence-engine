from app.retrieval.semantic_retriever import search_chunks
from app.reasoning.context_builder import build_context
from app.reasoning.llm import llm


def generate_technical_report():

    results = search_chunks(
        "document overview architecture technologies methodology contributions results future work",
        n_results=25
    )

    context = build_context(results)

    prompt = f"""
You are a senior technical analyst.

Generate a professional technical report.

Structure:

1. Executive Summary

2. Introduction

3. Background

4. System Architecture

5. Technologies Used

6. Methodology

7. Key Contributions

8. Results

9. Future Work

10. Conclusion

DOCUMENT:

{context}
"""

    response = llm.invoke(prompt)

    return response.content