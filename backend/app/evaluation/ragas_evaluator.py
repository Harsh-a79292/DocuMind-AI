import os

from dotenv import load_dotenv
from openai import OpenAI
from google import genai

from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings

from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextUtilization,
)

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")


async def evaluate_rag_response(
    question: str,
    answer: str,
    contexts: list[str],
) -> dict:

    if not question.strip():
        raise ValueError("Question cannot be empty")

    if not answer.strip():
        raise ValueError("Answer cannot be empty")

    if not contexts:
        raise ValueError("Contexts cannot be empty")

    # Gemini OpenAI-compatible client
    evaluator_client = OpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # RAGAS Instructor LLM
    evaluator_llm = llm_factory(
        "gemini-3.5-flash-lite",
        provider="openai",
        client=evaluator_client,
    )

    # Gemini embeddings
    google_client = genai.Client(api_key=API_KEY)

    evaluator_embeddings = GoogleEmbeddings(
        client=google_client,
        model="gemini-embedding-001",
    )

    # Metrics
    faithfulness = Faithfulness(llm=evaluator_llm)

    answer_relevancy = AnswerRelevancy(
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
    )

    context_utilization = ContextUtilization(
        llm=evaluator_llm,
    )

    # Evaluate
    faithfulness_result = await faithfulness.ascore(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts,
    )

    relevancy_result = await answer_relevancy.ascore(
        user_input=question,
        response=answer,
    )

    context_result = await context_utilization.ascore(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts,
    )

    return {
        "faithfulness": round(faithfulness_result.value, 4),
        "answer_relevancy": round(relevancy_result.value, 4),
        "context_utilization": round(context_result.value, 4),
    }