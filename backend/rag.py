from chunker import chunk_text
from embeddings import get_embeddings, embed_query
from vector_store import store_embeddings, search_similar


# -----------------------------
# MAIN INGESTION PIPELINE
# -----------------------------
def process_documents(documents, source_type="unknown"):

    if not documents:
        raise ValueError("No documents provided")

    # -----------------------------
    # STEP 1: Ensure chunking happens ONCE
    # -----------------------------
    if isinstance(documents[0], str):
        chunks = chunk_text(documents)
    else:
        chunks = documents

    if not chunks:
        raise ValueError("No chunks created")

    # -----------------------------
    # STEP 2: Clean chunks
    # -----------------------------
    processed_chunks = []

    for c in chunks:

        if not isinstance(c, dict):
            continue

        text = c.get("text", "").strip()

        if not text:
            continue

        processed_chunks.append({
            "text": text,
            "doc_id": c.get("doc_id", 0),
            "chunk_index": c.get("chunk_index", 0),
            "source": source_type
        })

    if not processed_chunks:
        raise ValueError("Empty chunks after cleaning")

    # -----------------------------
    # STEP 3: Embeddings
    # -----------------------------
    texts = [c["text"] for c in processed_chunks]
    embeddings = get_embeddings(texts)

    # -----------------------------
    # STEP 4: Store in vector DB
    # -----------------------------
    store_embeddings(processed_chunks, embeddings)

    return processed_chunks


# -----------------------------
# RETRIEVAL PIPELINE
# -----------------------------
def retrieve_context(question, top_k=3):

    if not question:
        return []

    query_embedding = embed_query(question)

    results = search_similar(
        query_embedding,
        top_k=top_k
    )

    return results if results else []