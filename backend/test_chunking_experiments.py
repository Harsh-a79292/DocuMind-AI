from backend.app.ingestion.document_loader import load_document
from backend.app.chunking.chunker import chunk_documents


documents = load_document("data/raw/attention_paper.pdf")

experiments = [
    {"name": "Small", "size": 200, "overlap": 40},
    {"name": "Medium", "size": 500, "overlap": 100},
    {"name": "Large", "size": 800, "overlap": 150},
]

print("\nCHUNKING EXPERIMENT RESULTS")
print("=" * 75)

for experiment in experiments:

    chunks = chunk_documents(
        documents,
        chunk_size=experiment["size"],
        overlap=experiment["overlap"]
    )

    sizes = [
        chunk["metadata"]["word_count"]
        for chunk in chunks
    ]

    average_size = sum(sizes) / len(sizes)

    print(f"\nExperiment: {experiment['name']}")
    print(f"Chunk size: {experiment['size']}")
    print(f"Overlap: {experiment['overlap']}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Average chunk size: {average_size:.2f}")
    print(f"Minimum chunk size: {min(sizes)}")
    print(f"Maximum chunk size: {max(sizes)}")