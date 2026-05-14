from chunker import chunk_text
from embeddings import get_embeddings, embed_query
from vector_store import store_embeddings, search_similar


def process_documents(documents):
    """
    FULL PIPELINE:
    documents → chunks → embeddings → store
    """
    chunks = documents

    if isinstance(documents, list) and documents and isinstance(documents[0], str):
        chunks = chunk_text(documents)

    if not chunks:
        raise ValueError("No chunks found")

    texts = [
        c["text"] if isinstance(c, dict) and "text" in c else str(c)
        for c in chunks
    ]

    texts = [t.strip() for t in texts if t and t.strip()]

    if not texts:
        raise ValueError("Empty text after cleaning")

    embeddings = get_embeddings(texts)

    store_embeddings(texts, embeddings)


def retrieve_context(question):
    """
    Retrieve top-k similar chunks
    """

    query_embedding = embed_query(question)

    results = search_similar(query_embedding, top_k=3)

    if not results:
        return ""

    return "\n\n".join([r if isinstance(r, str) else r.get("text", "") for r in results])