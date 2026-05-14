from fastapi import FastAPI, HTTPException, UploadFile, File
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

    try:

        documents = crawl_website(data.url)

        if not documents:
            raise HTTPException(
                status_code=400,
                detail="Crawler returned empty content"
            )

        chunks = chunk_text(documents)

        process_documents(
            chunks,
            source_type="website"
        )

        return {
            "success": True,
            "message": "Website ingestion successful",
            "chunks_created": len(chunks)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/ingest-pdf")
async def ingest_pdf(file: UploadFile = File(...)):

    try:

        if not file.filename.endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        documents = extract_pdf_text(file.file)

        if not documents:
            raise HTTPException(
                status_code=400,
                detail="PDF extraction failed"
            )

        chunks = chunk_text(documents)

        process_documents(
            chunks,
            source_type="pdf"
        )

        return {
            "success": True,
            "message": "PDF ingestion successful",
            "chunks_created": len(chunks)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/chat")
def chat(data: QuestionRequest):

    try:

        query_embedding = embed_query(data.question)

        results = search_similar(
            query_embedding,
            top_k=3
        )

        if not results:
            return {
                "success": False,
                "answer": "No relevant context found."
            }

        context_chunks = []

        for r in results:

            context_chunks.append(
                f"""
SOURCE: {r.get('source', 'unknown')}

{r.get('text', '')}
"""
            )

        answer = ask_llm(
            question=data.question,
            context_chunks=context_chunks
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )