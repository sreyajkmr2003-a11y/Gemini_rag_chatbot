def chunk_text(documents, chunk_size=250, overlap=30):
    """
    Splits documents into overlapping chunks.

    Args:
        documents (list): List of text documents
        chunk_size (int): Maximum words per chunk
        overlap (int): Overlapping words between chunks

    Returns:
        list: List of chunk dictionaries
    """

    if not documents:
        return []

    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    step = chunk_size - overlap

    for doc_id, doc in enumerate(documents):

        if not doc.strip():
            continue

        words = doc.split()

        for i in range(0, len(words), step):

            chunk_words = words[i:i + chunk_size]

            if not chunk_words:
                continue

            chunks.append({
                "text": " ".join(chunk_words),
                "doc_id": doc_id,
                "chunk_index": i // step,
                "word_count": len(chunk_words)
            })

    return chunks