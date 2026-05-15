from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from crawler import crawl_website, extract_pdf_text
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

@app.post("/ingest")
def ingest_website(data: URLRequest):

    docs = crawl_website(data.url)

    if not docs:
        raise HTTPException(status_code=400, detail="No content found from URL")

    chunks = chunk_text(docs)

    process_documents(chunks, source_type="website")

    return {
        "success": True,
        "chunks": len(chunks)
    }

@app.post("/ingest-pdf")
async def ingest_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_bytes = await file.read()

    text = extract_pdf_text(file_bytes)

    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    chunks = chunk_text([text])

    process_documents(chunks, source_type="pdf")

    return {
        "success": True,
        "chunks": len(chunks)
    }

@app.post("/chat")
def chat(data: QuestionRequest):

    query_embedding = embed_query(data.question)

    results = search_similar(query_embedding, top_k=5)

    if not results:
        return {
            "success": True,
            "answer": "No relevant context found in knowledge base."
        }

    context = [r.get("text", "") for r in results if r.get("text")]

    if not context:
        return {
            "success": True,
            "answer": "No valid context retrieved."
        }

    answer = ask_llm(data.question, context)

    return {
        "success": True,
        "answer": answer
    }
    
@app.get("/")
def home():
    return {"status": "RAG backend running successfully"}