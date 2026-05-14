from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from crawler import crawl_website
from chunker import chunk_text
from rag import process_documents, retrieve_context
from llm import ask_gemini
from embeddings import get_embeddings, embed_query
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

@app.post("/ingest")
def ingest_website(data: URLRequest):
    try:
        print("\n🔥 INGEST START")

        documents = crawl_website(data.url)

        if not documents:
            raise HTTPException(status_code=400, detail="Crawler returned empty content")

        print("DOC SAMPLE:", str(documents[0])[:200])

        chunks = chunk_text(documents)

        if not chunks:
            raise HTTPException(status_code=400, detail="Chunking failed")

        print(f"CHUNKS CREATED: {len(chunks)}")

        process_documents(chunks)

        return {
            "success": True,
            "message": "Ingestion successful",
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

        good_chunks = [r["text"] for r in results]

        answer = ask_gemini(
            question=data.question,
            context_chunks=good_chunks
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
