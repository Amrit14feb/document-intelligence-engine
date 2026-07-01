from app.reasoning.llm import llm


def generate_summary(context):

    prompt = f"""
You are an expert technical analyst.

Generate a professional executive summary.

Include:

1. Main objective
2. Important technologies
3. Key organizations
4. Major contributions
5. Research significance

DOCUMENT:

{context}

SUMMARY:
"""

    response = llm.invoke(prompt)

    return response.content