from app.reasoning.llm import llm

from app.retrieval.semantic_retriever import search_chunks

from app.reasoning.context_builder import build_context

from app.reasoning.prompts import RAG_PROMPT

from app.retrieval.graph_retriever import get_entity_context

from app.retrieval.multi_entity_detector import detect_entities

from app.retrieval.graph_expansion import expand_entities

from app.retrieval.hybrid_ranker import rerank_chunks


# ==========================================
# QUESTION
# ==========================================

question = input(
    "Ask Question: "
)


# ==========================================
# ENTITY DETECTION
# ==========================================

entities = detect_entities(
    question
)

print("\nDETECTED ENTITIES:\n")
print(entities)


# ==========================================
# GRAPH EXPANSION
# ==========================================

expanded_entities = expand_entities(
    entities,
    hops=1
)

print("\nEXPANDED ENTITIES:\n")
print(expanded_entities)


# ==========================================
# EXPANDED QUERY
# ==========================================

expanded_query = question

if expanded_entities:

    expanded_query += " "

    expanded_query += " ".join(
        expanded_entities
    )

print("\nEXPANDED QUERY\n")
print(expanded_query)


# ==========================================
# GRAPH CONTEXT
# ==========================================

graph_context = ""

for entity in entities:

    graph_context += get_entity_context(
        entity
    )

    graph_context += "\n"


# ==========================================
# SEMANTIC RETRIEVAL
# ==========================================

results = search_chunks(
    expanded_query,
    n_results=20
)

# ==========================================
# HYBRID RERANK
# ==========================================

results = rerank_chunks(
    results,
    expanded_entities
)

# keep only best 5

results = results[:5]


# ==========================================
# DOCUMENT CONTEXT
# ==========================================

document_context = build_context(
    results
)


# ==========================================
# FINAL CONTEXT
# ==========================================

context = f"""

GRAPH KNOWLEDGE

{graph_context}

DOCUMENT KNOWLEDGE

{document_context}

"""


# ==========================================
# PROMPT
# ==========================================

prompt = RAG_PROMPT.format(
    context=context,
    question=question
)


# ==========================================
# DEBUG
# ==========================================

print("\nCONTEXT SENT TO LLM\n")

print(
    context[:5000]
)

print("\n" + "=" * 80 + "\n")


# ==========================================
# LLM
# ==========================================

response = llm.invoke(
    prompt
)


# ==========================================
# OUTPUT
# ==========================================

print("\nANSWER\n")

print(
    response.content
)

print("\nTOP RETRIEVED CHUNKS\n")

for i, chunk in enumerate(results[:5]):

    print(f"\nCHUNK {i+1}\n")

    print(chunk[:500])

    print("-" * 80)