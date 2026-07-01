def score_chunk(chunk, entities):

    score = 0

    chunk_lower = chunk.lower()

    for entity in entities:

        if entity.lower() in chunk_lower:

            score += 1

    return score


def rerank_chunks(chunks, entities):

    scored = []

    for chunk in chunks:

        score = score_chunk(
            chunk,
            entities
        )

        scored.append(
            (score, chunk)
        )

    scored.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        chunk
        for score, chunk in scored
    ]