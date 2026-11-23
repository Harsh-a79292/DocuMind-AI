from backend.app.embeddings.embedder import generate_embeddings

texts = [
    "Artificial Intelligence is transforming the world.",
    "Machine Learning is a subset of Artificial Intelligence.",
    "Deep Learning uses neural networks to learn complex patterns."
]

embeddings = generate_embeddings(texts)

print("Batch embedding generated successfully!")
print("Total input texts:", len(texts))
print("Total embeddings:", len(embeddings))

for index, embedding in enumerate(embeddings):
    print(f"\nText {index + 1}: {texts[index]}")
    print("Vector dimensions:", len(embedding))
    print("First 5 values:", embedding[:5])