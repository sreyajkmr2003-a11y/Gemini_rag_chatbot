from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embeddings(texts):
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embeddings.astype("float32")


def embed_query(text):
    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embedding.astype("float32")