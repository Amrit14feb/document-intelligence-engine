from app.retrieval.semantic_retriever import search_chunks
from app.reasoning.context_builder import build_context
from app.reasoning.llm import llm


REPORT_QUERY = (
    "document overview architecture technologies methodology "
    "contributions results future work"
)


def generate_technical_report():

    results = search_chunks(
        REPORT_QUERY,
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


def generate_technical_report_with_evidence():
    """Generate the technical report and append citations + confidence.

    Additive companion to :func:`generate_technical_report`; reuses the same
    retrieval query so the evidence reflects the report's own context.
    """

    from app.intelligence.evidence import attach_evidence

    report = generate_technical_report()
    return attach_evidence(report, REPORT_QUERY)