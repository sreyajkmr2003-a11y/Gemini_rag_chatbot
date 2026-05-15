def chunk_text(documents, chunk_size=250, overlap=30):
    if not documents:
        return []

    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    step = chunk_size - overlap

    for doc_id, doc in enumerate(documents):
        if not doc or not doc.strip():
            continue

        words = doc.split()
        n = len(words)

        for start in range(0, n, step):
            end = start + chunk_size
            chunk_words = words[start:end]

            if not chunk_words:
                continue

            chunks.append({
                "text": " ".join(chunk_words),
                "doc_id": doc_id,
                "chunk_index": start // step,
                "word_count": len(chunk_words)
            })

    return chunks