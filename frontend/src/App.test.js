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

# -----------------------------
# CORS (MOBILE + FRONTEND SAFE)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# MODELS
# -----------------------------
class URLRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str


# -----------------------------
# INGEST WEBSITE
# -----------------------------
@app.post("/ingest")
def ingest_website(data: URLRequest):

    docs = crawl_website(data.url)

    if not docs or not docs[0].strip():
        raise HTTPException(status_code=400, detail="No content found")

    chunks = chunk_text(docs)

    process_documents(chunks, source_type="website")

    return {
        "success": True,
        "chunks_created": len(chunks)
    }


# -----------------------------
# INGEST PDF
# -----------------------------
@app.post("/ingest-pdf")
async def ingest_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    text_list = extract_pdf_text(file.file)

    if not text_list or not text_list[0].strip():
        raise HTTPException(status_code=400, detail="PDF extraction failed")

    chunks = chunk_text(text_list)

    process_documents(chunks, source_type="pdf")

    return {
        "success": True,
        "chunks_created": len(chunks)
    }


# -----------------------------
# CHAT API
# -----------------------------
@app.post("/chat")
def chat(data: QuestionRequest):

    query_embedding = embed_query(data.question)

    results = search_similar(query_embedding, top_k=5)

    if not results:
        return {
            "success": True,
            "answer": "No relevant context found."
        }

    context = [r["text"] for r in results if r.get("text")]

    answer = ask_llm(data.question, context)

    return {
        "success": True,
        "answer": answer
    }


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def home():
    return {"status": "RAG backend running"}