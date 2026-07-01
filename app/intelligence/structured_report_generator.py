from app.retrieval.semantic_retriever import search_chunks
from app.reasoning.context_builder import build_context
from app.reasoning.llm import llm

import json


def generate_structured_report():

    results = search_chunks(
        "document overview architecture technologies methodology contributions",
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