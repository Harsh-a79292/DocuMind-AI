from backend.app.embeddings.embedder import generate_query_embedding
from backend.app.embeddings.similarity import cosine_similarity


def search_similar_chunks(
    query: str,
    chunks: list[dict],
    embeddings: list[list[float]],
    top_k: int = 3
) -> list[dict]:

    if not query.strip():
        raise ValueError("Query cannot be empty")

    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings count must match")

    if not chunks:
        return []

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    # Generate query embedding
    query_embedding = generate_query_embedding(query)

    results = []

    # Calculate similarity with every chunk
    for chunk, embedding in zip(chunks, embeddings):

        score = cosine_similarity(
            query_embedding,
            embedding
        )

        results.append({
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "score": score
        })

    # Sort by highest similarity
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]