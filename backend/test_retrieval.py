from backend.app.ingestion.document_loader import load_document
from backend.app.chunking.chunker import chunk_documents
from backend.app.embeddings.embedder import generate_embeddings
from backend.app.retrieval.search import search_similar_chunks

# 1. Load PDF
documents = load_document("data/raw/attention_paper.pdf")

# 2. Create chunks
chunks = chunk_documents(
    documents,
    chunk_size=500,
    overlap=100
)

# 3. Generate document embeddings
chunk_texts = [chunk["text"] for chunk in chunks]

embeddings = generate_embeddings(chunk_texts)

# 4. Ask a question
query = "What are the advantages of self-attention over recurrent layers?"

# 5. Retrieve relevant chunks
results = search_similar_chunks(
    query=query,
    chunks=chunks,
    embeddings=embeddings,
    top_k=5
)
print("\nSEMANTIC SEARCH RESULTS")
print("=" * 60)

for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print("Chunk ID:", result["metadata"]["chunk_id"])
    print("Similarity Score:", round(result["score"], 4))
    print("Page:", result["metadata"]["page_number"])
    print("Text:")
    print(result["text"][:500])