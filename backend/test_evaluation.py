from backend.app.evaluation.metrics import precision_at_k

retrieved_results = [
    {"metadata": {"chunk_id": 5}},
    {"metadata": {"chunk_id": 8}},
    {"metadata": {"chunk_id": 2}},
    {"metadata": {"chunk_id": 9}},
    {"metadata": {"chunk_id": 4}}
]

relevant_chunk_ids = {5, 8, 9, 12}

score = precision_at_k(
    retrieved_results,
    relevant_chunk_ids,
    k=5
)

print("Precision@5:", score)