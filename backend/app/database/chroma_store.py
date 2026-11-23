from pathlib import Path

import chromadb


BASE_DIR = Path(__file__).resolve().parents[3]
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# Persistent ChromaDB client
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

# Collection for document chunks
collection = client.get_or_create_collection(
    name="documind_documents",
    metadata={"hnsw:space": "cosine"}
)


def store_chunks(
    document_id: str,
    chunks: list[dict],
    embeddings: list[list[float]]
) -> int:

    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings count must match")

    if not chunks:
        raise ValueError("No chunks provided")

    ids = []
    documents = []
    metadatas = []
    vectors = []

    for chunk, embedding in zip(chunks, embeddings):

        metadata = chunk["metadata"]

        chunk_id = (
            f"{document_id}_{metadata['chunk_id']}"
        )

        ids.append(chunk_id)
        documents.append(chunk["text"])
        vectors.append(embedding)

        metadatas.append({
            "document_id": document_id,
            "source": str(metadata.get("source", "")),
            "file_type": str(metadata.get("file_type", "")),
            "page_number": (
                metadata.get("page_number")
                if metadata.get("page_number") is not None
                else -1
            ),
            "chunk_id": int(metadata["chunk_id"]),
            "chunk_index": int(metadata["chunk_index"])
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=vectors,
        metadatas=metadatas
    )

    return len(ids)


def search_chunks(
    document_id: str,
    query_embedding: list[float],
    top_k: int = 3
) -> list[dict]:

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"document_id": document_id},
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved = []

    if not results["ids"] or not results["ids"][0]:
        return retrieved

    for index in range(len(results["ids"][0])):

        metadata = results["metadatas"][0][index]
        distance = results["distances"][0][index]

        retrieved.append({
            "text": results["documents"][0][index],
            "metadata": {
                "document_id": metadata["document_id"],
                "source": metadata["source"],
                "file_type": metadata["file_type"],
                "page_number": (
                    None
                    if metadata["page_number"] == -1
                    else metadata["page_number"]
                ),
                "chunk_id": metadata["chunk_id"],
                "chunk_index": metadata["chunk_index"]
            },
            "score": 1.0 - distance
        })

    return retrieved


def delete_document(document_id: str) -> int:

    existing = collection.get(
        where={"document_id": document_id},
        include=[]
    )

    ids = existing["ids"]

    if ids:
        collection.delete(ids=ids)

    return len(ids)