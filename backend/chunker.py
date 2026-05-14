def chunk_text(documents, chunk_size=500, overlap=50):
    if not documents:
        return []

    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    step = chunk_size - overlap

    for doc_id, doc in enumerate(documents):
        words = doc.split()

        for i in range(0, len(words), step):
            chunk = words[i:i + chunk_size]

            chunks.append({
                "text": " ".join(chunk),
                "doc_id": doc_id,
                "chunk_index": i // step
            })

    return chunks