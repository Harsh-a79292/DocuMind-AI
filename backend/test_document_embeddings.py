from backend.app.ingestion.document_loader import load_document
from backend.app.chunking.chunker import chunk_documents
from backend.app.embeddings.embedder import generate_embeddings

# 1. Load PDF
documents = load_document("data/raw/attention_paper.pdf")

print("Total pages:", len(documents))

# 2. Create chunks
chunks = chunk_documents(
    documents,
    chunk_size=500,
    overlap=100
)

print("Total chunks:", len(chunks))

# 3. Extract chunk texts
chunk_texts = [
    chunk["text"]
    for chunk in chunks
]

# 4. Generate embeddings
embeddings = generate_embeddings(chunk_texts)

# 5. Verify results
print("\nEmbedding generation completed!")
print("Total chunks:", len(chunks))
print("Total embeddings:", len(embeddings))

for i in range(min(3, len(chunks))):
    print("\n" + "=" * 50)
    print("Chunk:", i)
    print("Source:", chunks[i]["metadata"]["source"])
    print("Page:", chunks[i]["metadata"]["page_number"])
    print("Vector dimensions:", len(embeddings[i]))