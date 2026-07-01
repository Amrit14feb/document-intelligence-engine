from app.reasoning.llm import llm

from app.retrieval.semantic_retriever import search_chunks_with_scores

from app.reasoning.context_builder import build_context

from app.reasoning.prompts import RAG_PROMPT

from app.retrieval.graph_retriever import get_entity_context

from app.retrieval.multi_entity_detector import detect_entities

from app.retrieval.graph_traversal import (
    build_adjacency,
    rank_expanded_entities,
    load_relationships,
)

from app.knowledge_extraction.entity_resolver import (
    build_canonical_index,
    resolve_all,
    load_entities,
    load_aliases,
)

from app.retrieval.hybrid_scorer import hybrid_rank

from app.intelligence.citation_generator import (
    generate_citations,
    format_sources,
    load_chunk_records,
)

from app.intelligence.confidence_scorer import (
    confidence_from_scored_chunks,
    format_confidence,
)


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
# ENTITY RESOLUTION (priority #3)
# ==========================================
#
# Canonicalize detected mentions so aliases/variants collapse to one node
# before we traverse the graph.

canonical_index = build_canonical_index(load_entities())
aliases = load_aliases()

entities = resolve_all(entities, canonical_index, aliases)

print("\nRESOLVED ENTITIES:\n")
print(entities)


# ==========================================
# GRAPH EXPANSION via traversal (priority #4)
# ==========================================
#
# Distance-weighted BFS keeps the closest neighbours instead of the legacy
# length-based cap.

adjacency = build_adjacency(load_relationships())

expanded_entities = rank_expanded_entities(
    entities,
    adjacency,
    max_hops=2,
    top_k=15,
    include_seeds=True,
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

# Count graph relationships that fed the context (used for confidence scoring).
num_graph_relationships = len(
    [line for line in graph_context.splitlines() if line.strip()]
)


# ==========================================
# SEMANTIC RETRIEVAL (with scores)
# ==========================================

candidates = search_chunks_with_scores(
    expanded_query,
    n_results=20
)

# ==========================================
# HYBRID FUSION
# ==========================================
#
# Fuse the vector store's semantic similarity with entity coverage and query
# keyword overlap. Keyword overlap uses the *original* question (not the
# entity-expanded query) so expansion terms do not drown out the user's intent.

ranked = hybrid_rank(
    candidates,
    entities=expanded_entities,
    query=question,
    top_k=5,
)

results = [scored.text for scored in ranked]


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


# ==========================================
# CITATIONS (priority #5)
# ==========================================

chunk_records = load_chunk_records()

citations = generate_citations(
    results,
    chunk_records,
)

print("\n" + format_sources(citations) + "\n")


# ==========================================
# CONFIDENCE (priority #6)
# ==========================================

confidence = confidence_from_scored_chunks(
    ranked,
    num_graph_relationships=num_graph_relationships,
)

print(format_confidence(confidence) + "\n")