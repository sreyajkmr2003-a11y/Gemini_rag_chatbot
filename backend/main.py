import os
import asyncio
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from crawler import crawl_website
from pdf_utils import extract_pdf_text
from chunker import chunk_text
from rag import process_documents
from llm import ask_llm
from embeddings import embed_query
from vector_store import search_similar

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/ingest")
async def ingest_website(data: URLRequest):
    try:
        documents = await asyncio.to_thread(crawl_website, data.url)

        if not documents:
            raise HTTPException(status_code=400, detail="No content extracted from URL")

        chunks = chunk_text(documents)

        await asyncio.to_thread(process_documents, chunks, "website")

        return {
            "success": True,
            "message": "Website ingestion successful",
            "chunks_created": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest-pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF allowed")

        file_bytes = await file.read()

        documents = await asyncio.to_thread(extract_pdf_text, file_bytes)

        print("🔵 PDF EXTRACTION OUTPUT START")
        print("LENGTH:", len(documents) if documents else 0)
        print("SAMPLE TEXT:", documents[:300] if documents else "EMPTY")
        print("🔵 PDF EXTRACTION OUTPUT END")

        if not documents or len(documents.strip()) == 0:
            raise HTTPException(status_code=400, detail="PDF extraction failed")

        chunks = chunk_text([documents])

        print("🟢 CHUNKS CREATED:", len(chunks))

        await asyncio.to_thread(process_documents, chunks, "pdf")

        print("📦 PDF INGESTION COMPLETE")

        return {
            "success": True,
            "message": "PDF ingestion successful",
            "chunks_created": len(chunks)
        }

    except Exception as e:
        print("❌ INGEST ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat(data: QuestionRequest):
    try:
        query_embedding = embed_query(data.question)

        results = search_similar(query_embedding, top_k=3)

        if not results:
            return {
                "success": False,
                "answer": "No relevant context found."
            }

        context_chunks = []

        for r in results:
            context_chunks.append(f"SOURCE: {r.get('source', 'unknown')}\n\n{r.get('text', '')}")

        answer = ask_llm(
            question=data.question,
            context_chunks=context_chunks
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
