from typing import List, Dict, Any
import os
import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB
# If CHROMA_HOST is set (e.g., in Docker), use HttpClient.
# Otherwise, fall back to a local PersistentClient (e.g., for local testing without Docker compose).
_chroma_host = os.getenv("CHROMA_HOST")
_chroma_port = os.getenv("CHROMA_PORT", "8000")

if _chroma_host:  # E.g. "chromadb" or "localhost"
    _client = chromadb.HttpClient(host=_chroma_host, port=int(_chroma_port))
else:
    # Use local persistence directory if no host provided
    _client = chromadb.PersistentClient(path="./brainiac_db")

_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def get_collection():
    """Get the Chroma collection, creating it if necessary."""
    return _client.get_or_create_collection(
        name="brainiac_knowledge",
        embedding_function=_embedding_function,
        metadata={"hnsw:space": "cosine"},
    )


def add_documents(
    documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]
):
    """Add documents to the collection."""
    if not documents:
        return
    collection = get_collection()
    collection.add(documents=documents, metadatas=metadatas, ids=ids)


def query_documents(query_text: str, n_results: int = 5) -> Dict[str, Any]:
    """Query the collection for relevant documents."""
    collection = get_collection()
    return collection.query(query_texts=[query_text], n_results=n_results)


def get_document(where: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve documents matching specific metadata criteria."""
    collection = get_collection()
    return collection.get(where=where)


def inspect_collection():
    """Return stats about the collection."""
    collection = get_collection()
    count = collection.count()
    return f"Collection contains {count} documents."


def clear_collection():
    """Clear all documents from the collection."""
    # Chroma doesn't have a direct 'clear', so we delete and recreate
    try:
        _client.delete_collection("brainiac_knowledge")
    except ValueError:
        pass  # Collection might not exist
    # Re-create is handled by next usage or explicit call
    get_collection()
