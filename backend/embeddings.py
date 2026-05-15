from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


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


def embed_query(text):
    if not text:
        return np.array([], dtype="float32")

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return np.asarray(embedding, dtype="float32")