from backend.app.embeddings.embedder import generate_query_embedding

query = "What is the attention mechanism in deep learning?"

embedding = generate_query_embedding(query)

print("Query embedding generated!")
print("Vector dimensions:", len(embedding))
print("First 10 values:", embedding[:10])