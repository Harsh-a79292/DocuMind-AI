from copy import deepcopy


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 500,
    overlap: int = 100
) -> list[dict]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size"
        )

    chunked_documents = []

    for document in documents:

        text = document["text"].strip()
        metadata = document["metadata"]

        if not text:
            continue

        words = text.split()

        start = 0
        chunk_index = 0

        while start < len(words):

            end = min(start + chunk_size, len(words))

            chunk_text = " ".join(words[start:end])

            chunked_documents.append({
                "text": chunk_text,
                "metadata": {
                    **deepcopy(metadata),
                    "chunk_id": len(chunked_documents),
                    "chunk_index": chunk_index,
                    "word_start": start,
                    "word_end": end,
                    "word_count": end - start
                }
            })
            chunk_index += 1

            if end == len(words):
                break

            start = end - overlap

    return chunked_documents