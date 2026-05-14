import faiss
import numpy as np

index = None
stored_texts = []
DIMENSION = None


def initialize_index(dim):
    global index, DIMENSION
    DIMENSION = dim
    index = faiss.IndexFlatIP(dim)  # cosine similarity after normalization


def store_embeddings(texts, embeddings):
    global index, stored_texts, DIMENSION

    vectors = np.array(embeddings).astype("float32")

    if vectors.ndim == 1:
        vectors = vectors.reshape(1, -1)

    if index is None:
        initialize_index(vectors.shape[1])

    if vectors.shape[1] != DIMENSION:
        raise ValueError(
            f"Embedding dimension mismatch: expected {DIMENSION}, got {vectors.shape[1]}"
        )

    if len(texts) != len(vectors):
        raise ValueError("Texts and embeddings count mismatch")

    faiss.normalize_L2(vectors)

    index.add(vectors)

    stored_texts.extend(texts)


def search_similar(query_embedding, top_k=3):
    vector = np.array(query_embedding).astype("float32").reshape(1, -1)

    faiss.normalize_L2(vector)

    distances, indices = index.search(vector, top_k)

    results = []

    print("\n🔥 FAISS DEBUG")
    print("Distances:", distances)
    print("Indices:", indices)

    for i, idx in enumerate(indices[0]):
        if 0 <= idx < len(stored_texts):
            results.append({
                "text": stored_texts[idx],
                "score": float(distances[0][i])
            })

    return results


def reset_store():
    global index, stored_texts, DIMENSION
    index = None
    stored_texts = []
    DIMENSION = None