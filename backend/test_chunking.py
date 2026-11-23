from backend.app.ingestion.document_loader import load_document
from backend.app.chunking.chunker import chunk_documents


# Step 1: Load PDF
documents = load_document("data/raw/attention_paper.pdf")

# Step 2: Generate chunks
chunks = chunk_documents(
    documents,
    chunk_size=500,
    overlap=100
)

# Step 3: Display results
print("Total pages:", len(documents))
print("Total chunks:", len(chunks))

for chunk in chunks[:5]:
    print("\n" + "=" * 60)
    print("METADATA:", chunk["metadata"])
    print("TEXT:")
    print(chunk["text"][:300])