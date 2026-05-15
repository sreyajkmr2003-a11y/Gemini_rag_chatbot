from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once (important for deployment performance)
model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# DOCUMENT EMBEDDINGS
# -----------------------------
def get_embeddings(texts):

    if not texts:
        return np.array([], dtype="float32")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return np.asarray(embeddings, dtype="float32")


# -----------------------------
# QUERY EMBEDDING
# -----------------------------
def embed_query(text):

    if not text or not text.strip():
        return np.array([], dtype="float32")

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return np.asarray(embedding, dtype="float32")