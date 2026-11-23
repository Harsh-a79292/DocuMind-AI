
from pathlib import Path
from uuid import uuid4
import traceback

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

from backend.app.ingestion.document_loader import load_document
from backend.app.chunking.chunker import chunk_documents

from backend.app.embeddings.embedder import (
    generate_embeddings,
    generate_query_embedding
)

from backend.app.generation.generator import generate_answer

from backend.app.database.chroma_store import (
    store_chunks,
    search_chunks,
    delete_document
)


app = FastAPI(
    title="DocuMind AI",
    description="AI-powered Retrieval Augmented Generation application",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://frontend-vp2d.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "raw"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


# REQUEST MODELS

class QueryRequest(BaseModel):
    document_id: str
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class AskRequest(BaseModel):
    document_id: str
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


# HOME

@app.get("/")
def home():
    return {
        "message": "DocuMind AI API is running!",
        "status": "success"
    }


# HEALTH CHECK

@app.get("/health")
def health_check():
    return {"status": "healthy"}


# DOCUMENT UPLOAD

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are allowed"
        )

    document_id = uuid4().hex
    file_path = UPLOAD_DIR / f"{document_id}{extension}"

    try:
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        file_path.write_bytes(content)

        documents = load_document(str(file_path))

        chunks = chunk_documents(
            documents,
            chunk_size=500,
            overlap=100
        )

        if not chunks:
            raise ValueError("No chunks generated")

        for chunk in chunks:
            chunk["metadata"]["document_id"] = document_id

        chunk_texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = generate_embeddings(chunk_texts)

        if len(embeddings) != len(chunks):
            raise ValueError("Embedding count mismatch")

        total_stored = store_chunks(
            document_id=document_id,
            chunks=chunks,
            embeddings=embeddings
        )

        return {
            "message": "Document processed and stored successfully",
            "document_id": document_id,
            "filename": file.filename,
            "total_pages_or_sections": len(documents),
            "total_chunks": len(chunks),
            "total_embeddings": len(embeddings),
            "total_stored": total_stored,
            "embedding_dimensions": len(embeddings[0])
        }

    except HTTPException:
        file_path.unlink(missing_ok=True)
        raise

    except Exception:
        file_path.unlink(missing_ok=True)
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Document processing failed"
        )


# SEMANTIC RETRIEVAL

@app.post("/query")
def query_document(request: QueryRequest):

    try:
        query_embedding = generate_query_embedding(
            request.question
        )

        results = search_chunks(
            document_id=request.document_id,
            query_embedding=query_embedding,
            top_k=request.top_k
        )

        return {
            "question": request.question,
            "document_id": request.document_id,
            "total_results": len(results),
            "results": [
                {
                    "chunk_id": result["metadata"]["chunk_id"],
                    "page_number": result["metadata"]["page_number"],
                    "similarity_score": round(result["score"], 4),
                    "text": result["text"]
                }
                for result in results
            ]
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Document retrieval failed"
        )


# COMPLETE RAG QUESTION ANSWERING

@app.post("/ask")
def ask_document(request: AskRequest):

    try:
        query_embedding = generate_query_embedding(
            request.question
        )

        retrieved_chunks = search_chunks(
            document_id=request.document_id,
            query_embedding=query_embedding,
            top_k=request.top_k
        )

        if not retrieved_chunks:
            return {
                "question": request.question,
                "document_id": request.document_id,
                "answer": "No relevant information found in the uploaded document.",
                "total_sources": 0,
                "sources": []
            }

        answer = generate_answer(
            question=request.question,
            retrieved_chunks=retrieved_chunks
        )

        sources = [
            {
                "chunk_id": chunk["metadata"]["chunk_id"],
                "page_number": chunk["metadata"]["page_number"],
                "similarity_score": round(chunk["score"], 4),
                "source": chunk["metadata"]["source"]
            }
            for chunk in retrieved_chunks
        ]

        return {
            "question": request.question,
            "document_id": request.document_id,
            "answer": answer,
            "total_sources": len(sources),
            "sources": sources
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Answer generation failed"
        )


# DELETE DOCUMENT

@app.delete("/documents/{document_id}")
def remove_document(document_id: str):

    try:
        deleted_chunks = delete_document(document_id)

        if deleted_chunks == 0:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return {
            "message": "Document deleted successfully",
            "document_id": document_id,
            "deleted_chunks": deleted_chunks
        }

    except HTTPException:
        raise

    except Exception:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Document deletion failed"
        )

