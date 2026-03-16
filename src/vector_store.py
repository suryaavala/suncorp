import os
from abc import ABC, abstractmethod
import chromadb
from google import genai

class VectorStore(ABC):
    """Abstract base class for vector storage."""
    
    @abstractmethod
    def add_texts(self, texts: list[str], ids: list[str], metadatas: list[dict]):
        pass
        
    @abstractmethod
    def query(self, query_embeddings: list[list[float]], n_results: int) -> list[str]:
        pass

class ChromaVectorStore(VectorStore):
    """Local ChromaDB implementation of the vector store."""
    def __init__(self, path: str = "data/chroma_db", collection_name: str = "policy_chunks"):
        os.makedirs(path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
    def add_texts(self, texts: list[str], ids: list[str], metadatas: list[dict], embeddings: list[list[float]]):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        
    def query(self, query_embeddings: list[list[float]], n_results: int = 2) -> list[str]:
        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []

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
    with open('data/policy.md', 'r') as f:
        content = f.read()

    chunks = chunk_text(content, chunk_size=200)
    ai_client = genai.Client()
    vector_store = ChromaVectorStore()

    for i, chunk in enumerate(chunks):
        embedding = get_gemini_embedding(ai_client, chunk)
        vector_store.add_texts(
            texts=[chunk],
            ids=[f"chunk_{i}"],
            embeddings=[[embedding]],
            metadatas=[{"source": "data/policy.md", "chunk_index": i}]
        )
    print(f"Stored {len(chunks)} chunks in Vector Store.")

if __name__ == "__main__":
    populate_vector_store()
