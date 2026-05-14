from chunker import chunk_text
from embeddings import get_embeddings, embed_query
from vector_store import store_embeddings, search_similar


def process_documents(documents, source_type="unknown"):
    """
    FULL RAG PIPELINE

    documents
        ↓
    chunks
        ↓
    embeddings
        ↓
    vector storage
    """
    chunks = documents

    if (
        isinstance(documents, list)
        and documents
        and isinstance(documents[0], str)
    ):
        chunks = chunk_text(documents)

    if not chunks:
        raise ValueError("No chunks found")

    processed_chunks = []

    for c in chunks:

        if isinstance(c, dict) and "text" in c:

            text = c["text"].strip()

            if text:

                processed_chunks.append({
                    "text": text,
                    "doc_id": c.get("doc_id", 0),
                    "chunk_index": c.get("chunk_index", 0),
                    "source": source_type
                })

    if not processed_chunks:
        raise ValueError("Empty text after cleaning")

    texts = [c["text"] for c in processed_chunks]

    embeddings = get_embeddings(texts)

    store_embeddings(processed_chunks, embeddings)

    return processed_chunks


def retrieve_context(question, top_k=3):
    """
    Retrieve most relevant chunks
    """

    query_embedding = embed_query(question)

    results = search_similar(
        query_embedding,
        top_k=top_k
    )

    if not results:
        return []

    return results