import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-embedding-001"


def generate_embedding(text: str) -> list[float]:

    if not text.strip():
        raise ValueError("Input text cannot be empty")

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT"
        )
    )

    return response.embeddings[0].values


def generate_embeddings(texts: list[str]) -> list[list[float]]:

    if not texts:
        raise ValueError("Input texts cannot be empty")

    if any(not text.strip() for text in texts):
        raise ValueError("All input texts must be non-empty")

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT"
        )
    )

    return [
        embedding.values
        for embedding in response.embeddings
    ]
def generate_query_embedding(query: str) -> list[float]:

    if not query.strip():
        raise ValueError("Query cannot be empty")

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY"
        )
    )

    return response.embeddings[0].values