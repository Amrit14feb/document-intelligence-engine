from app.retrieval.semantic_retriever import search_chunks
from app.reasoning.context_builder import build_context
from app.reasoning.llm import llm

import json


STRUCTURED_REPORT_QUERY = (
    "document overview architecture technologies methodology contributions"
)


def generate_structured_report():

    results = search_chunks(
        STRUCTURED_REPORT_QUERY,
        n_results=20
    )

    context = build_context(results)

    prompt = f"""
You are an expert technical report writer.

Your task is to generate a COMPLETE professional technical report from the provided document.

Return ONLY valid JSON.

The JSON format MUST be:

{{
    "title":"",
    "sections":[
        {{
            "heading":"",
            "content":""
        }}
    ]
}}

Rules:

1. Generate a professional report title.

2. Generate between 10 and 15 sections.

3. The report should follow a logical technical flow.

Possible sections include:

- Executive Summary
- Introduction
- Background
- Project Objectives
- System Overview
- System Architecture
- Hardware Components
- Software Components
- Technologies Used
- Research Methodology
- Design Process
- Validation and Testing
- Research Contributions
- Challenges
- Future Work
- Conclusion

Use only the sections that are relevant to the document.

For EACH section:

- Write detailed content.
- Minimum 300 words.
- Maximum 700 words.
- Use multiple paragraphs.
- Explain concepts instead of only listing facts.
- Connect ideas naturally.
- Mention important technologies.
- Mention important organizations.
- Mention important people.
- Mention important hardware/software whenever available.
- Do NOT repeat identical information across sections.
- Use ONLY information available in the document.
- Never invent facts.

DOCUMENT:

{context}
"""

    response = llm.invoke(prompt)

    return json.loads(
        response.content
    )


def generate_structured_report_with_evidence():
    """Generate the structured report and add a grounding section.

    Additive companion to :func:`generate_structured_report`. Appends a
    "Sources & Confidence" section (citations + confidence) so the JSON report
    stays traceable to the document, without changing the base schema.
    """

    from app.intelligence.evidence import gather_evidence

    report = generate_structured_report()
    evidence = gather_evidence(STRUCTURED_REPORT_QUERY)

    report.setdefault("sections", []).append(
        {
            "heading": "Sources & Confidence",
            "content": evidence.appendix(),
        }
    )
    return report