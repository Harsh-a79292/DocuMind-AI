def precision_at_k(
    retrieved_results: list[dict],
    relevant_chunk_ids: set[int],
    k: int
) -> float:

    if k <= 0:
        raise ValueError("k must be greater than 0")

    if not retrieved_results:
        return 0.0

    top_k_results = retrieved_results[:k]

    relevant_count = sum(
        1
        for result in top_k_results
        if result["metadata"]["chunk_id"] in relevant_chunk_ids
    )

    return relevant_count / k