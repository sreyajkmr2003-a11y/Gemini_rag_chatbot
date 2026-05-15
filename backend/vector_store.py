import faiss
import numpy as np
import pickle
import os

INDEX_FILE = "faiss.index"
CHUNKS_FILE = "chunks.pkl"

index = None
stored_chunks = []
DIMENSION = None


# -----------------------------
# LOAD EXISTING DATA (PERSISTENCE)
# -----------------------------
def load_store():

    global index, stored_chunks, DIMENSION

    if os.path.exists(INDEX_FILE):
        index = faiss.read_index(INDEX_FILE)

    if os.path.exists(CHUNKS_FILE):
        with open(CHUNKS_FILE, "rb") as f:
            stored_chunks = pickle.load(f)


# -----------------------------
# INITIALIZE INDEX
# -----------------------------
def initialize_index(dim):

    global index, DIMENSION

    DIMENSION = dim
    index = faiss.IndexFlatIP(dim)


# -----------------------------
# STORE EMBEDDINGS
# -----------------------------
def store_embeddings(chunks, embeddings):

    global index, stored_chunks, DIMENSION

    vectors = np.array(embeddings).astype("float32")

    if vectors.ndim == 1:
        vectors = vectors.reshape(1, -1)

    if index is None:
        initialize_index(vectors.shape[1])

    if vectors.shape[1] != DIMENSION:
        raise ValueError("Embedding dimension mismatch")

    if len(chunks) != len(vectors):
        raise ValueError("Chunks and embeddings mismatch")

    faiss.normalize_L2(vectors)

    index.add(vectors)

    stored_chunks.extend(chunks)

    # -----------------------------
    # SAVE TO DISK (IMPORTANT FIX)
    # -----------------------------
    faiss.write_index(index, INDEX_FILE)

    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(stored_chunks, f)


# -----------------------------
# SEARCH SIMILAR CHUNKS
# -----------------------------
def search_similar(query_embedding, top_k=3):

    global index, stored_chunks

    if index is None:
        load_store()

    if index is None:
        return []

    vector = np.array(query_embedding).astype("float32").reshape(1, -1)

    faiss.normalize_L2(vector)

    distances, indices = index.search(vector, top_k)

    results = []

    for i, idx in enumerate(indices[0]):

        if 0 <= idx < len(stored_chunks):

            chunk = stored_chunks[idx]

            results.append({
                "text": chunk.get("text", ""),
                "score": float(distances[0][i]),
                "doc_id": chunk.get("doc_id"),
                "chunk_index": chunk.get("chunk_index"),
                "source": chunk.get("source")
            })

    return results


# -----------------------------
# RESET STORE
# -----------------------------
def reset_store():

    global index, stored_chunks, DIMENSION

    index = None
    stored_chunks = []
    DIMENSION = None

    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)

    if os.path.exists(CHUNKS_FILE):
        os.remove(CHUNKS_FILE)