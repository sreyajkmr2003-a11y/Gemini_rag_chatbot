import faiss
import numpy as np

index = None
stored_chunks = []
DIMENSION = None


def initialize_index(dim):
    global index, DIMENSION
    DIMENSION = dim
    index = faiss.IndexFlatIP(dim)


def store_embeddings(chunks, embeddings):
    global index, stored_chunks, DIMENSION

    vectors = np.array(embeddings).astype("float32")

    if vectors.ndim == 1:
        vectors = vectors.reshape(1, -1)

    if index is None:
        initialize_index(vectors.shape[1])

    if vectors.shape[1] != DIMENSION:
        raise ValueError(f"Embedding dimension mismatch: expected {DIMENSION}, got {vectors.shape[1]}")

    if len(chunks) != len(vectors):
        raise ValueError("Chunks and embeddings count mismatch")

    faiss.normalize_L2(vectors)
    index.add(vectors)

    stored_chunks.extend(chunks)


def search_similar(query_embedding, top_k=3):
    global index, stored_chunks

    if index is None:
        return []

    vector = np.array(query_embedding).astype("float32").reshape(1, -1)

    faiss.normalize_L2(vector)

    distances, indices = index.search(vector, top_k)

    results = []

    for i, idx in enumerate(indices[0]):
        if 0 <= idx < len(stored_chunks):
            chunk_data = stored_chunks[idx]

            results.append({
                "text": chunk_data.get("text", ""),
                "score": float(distances[0][i]),
                "doc_id": chunk_data.get("doc_id"),
                "chunk_index": chunk_data.get("chunk_index"),
                "source": chunk_data.get("source")
            })

    return results


def reset_store():
    global index, stored_chunks, DIMENSION

    index = None
    stored_chunks = []
    DIMENSION = None