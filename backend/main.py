from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from crawler import crawl_website, extract_pdf_text
from chunker import chunk_text
from llm import ask_llm
from embeddings import get_embeddings, embed_query
from vector_store import store_embeddings, search_similar, reset_store

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODELS ----------------
class URLRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str


# ---------------- WEBSITE INGEST ----------------
@app.post("/ingest")
def ingest_website(data: URLRequest):

    reset_store()

    docs = crawl_website(data.url)

    if not docs:
        raise HTTPException(status_code=400, detail="No website content found")

    chunks = chunk_text(docs)

    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks created")

    texts = [c["text"] for c in chunks]
    embeddings = get_embeddings(texts)

    store_embeddings(chunks, embeddings)

    print("WEB CHUNKS:", len(chunks))

    return {"success": True, "source": "website", "chunks": len(chunks)}


# ---------------- PDF INGEST ----------------
@app.post("/ingest-pdf")
async def ingest_pdf(file: UploadFile = File(...)):

    reset_store()

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    text_list = extract_pdf_text(file.file)

    if not text_list or not text_list[0].strip():
        raise HTTPException(status_code=400, detail="Empty PDF content")

    chunks = chunk_text(text_list)

    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks created")

    texts = [c["text"] for c in chunks]
    embeddings = get_embeddings(texts)

    store_embeddings(chunks, embeddings)

    print("PDF CHUNKS:", len(chunks))

    return {"success": True, "source": "pdf", "chunks": len(chunks)}


# ---------------- CHAT ----------------
@app.post("/chat")
def chat(data: QuestionRequest):

    query_embedding = embed_query(data.question)

    results = search_similar(query_embedding, top_k=8)

    print("QUERY:", data.question)
    print("RESULTS:", results)

    if not results:
        return {
            "success": True,
            "answer": "No relevant context found."
        }

    context_chunks = [r["text"] for r in results]

    answer = ask_llm(
        question=data.question,
        context_chunks=context_chunks
    )

    return {
        "success": True,
        "answer": answer
    }


# ---------------- HEALTH ----------------
@app.get("/")
def home():
    return {"status": "RAG backend running"}