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


def generate_summary_with_evidence(context, query="executive summary objective technologies organizations contributions"):
    """Generate an executive summary and append citations + confidence.

    Additive companion to :func:`generate_summary`; the original is unchanged.
    ``query`` is used only to gather the supporting evidence appendix.
    """

    from app.intelligence.evidence import attach_evidence

    summary = generate_summary(context)
    return attach_evidence(summary, query)