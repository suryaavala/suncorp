from sentence_transformers import CrossEncoder

reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_chunks(query: str, chunks: list[str], top_k: int = 2) -> list[str]:
    """Re-ranks a list of text chunks based on their relevance to the query.

    Args:
        query (str): The user's claim description.
        chunks (list[str]): A list of policy chunks retrieved from the vector store.
        top_k (int, optional): The number of top chunks to return. Defaults to 2.

    Returns:
        list[str]: A list of the `top_k` most relevant chunks.
    """
    if not chunks:
        return []

    pairs = [(query, chunk) for chunk in chunks]
    scores = reranker_model.predict(pairs)
    scored_chunks = list(zip(chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    top_chunks = [chunk for chunk, score in scored_chunks[:top_k]]

    return top_chunks
