import os
import chromadb
from google import genai

def chunk_text(text: str, chunk_size: int = 200) -> list[str]:
    """Splits text into chunks of roughly `chunk_size` words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def get_gemini_embedding(client: genai.Client, text: str) -> list[float]:
    """Gets text embedding from Google GenAI."""
    response = client.models.embed_content(
        model='gemini-embedding-001',
        contents=text,
    )
    return response.embeddings[0].values

def populate_vector_store():
    """Reads policy, chunks it, embeds it, and stores it in Chroma."""
    # 1. Read Policy
    with open('data/policy.md', 'r') as f:
        content = f.read()

    # 2. Chunk text
    chunks = chunk_text(content, chunk_size=200)

    # 3. Setup GenAI client
    # The client automatically picks up GEMINI_API_KEY from environment
    ai_client = genai.Client()

    # 4. Setup ChromaDB
    os.makedirs('data/chroma_db', exist_ok=True)
    chroma_client = chromadb.PersistentClient(path="data/chroma_db")
    collection = chroma_client.get_or_create_collection(name="policy_chunks")

    # 5. Embed and Store
    for i, chunk in enumerate(chunks):
        embedding = get_gemini_embedding(ai_client, chunk)
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": "data/policy.md", "chunk_index": i}]
        )
    print(f"Stored {len(chunks)} chunks in ChromaDB.")

if __name__ == "__main__":
    populate_vector_store()
