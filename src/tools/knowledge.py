from src.services.db import query_documents

# Helper to normalize text
def clean_doc_text(text: str) -> str:
    if not text:
        return ""
    return text.replace("\n", " ").strip()

async def search_knowledge_base(query: str) -> str:
    """Semantic search across Jira and Confluence knowledge base."""
    # The default query_documents returns a dict with 'documents', 'metadatas' keys
    # containing lists of lists.
    res = query_documents(query)

    docs = res.get("documents", [])
    # Check if we got any results (docs is [[...]] or None)
    if not docs or not docs[0]:
        return "No matching records found."

    documents_list = docs[0]
    # metadatas might be None if none provided, but we inserted them
    metadatas_list = res.get("metadatas", [[]])[0]

    output = "Found relevant items:\n"
    for i, doc in enumerate(documents_list):
        meta = metadatas_list[i] if metadatas_list and i < len(metadatas_list) else {}
        source = meta.get("source", "unknown")
        # Jira key or page title
        ref = meta.get("key") or meta.get("title")

        # Simple cleanup
        clean_doc = clean_doc_text(doc)[:200]
        output += f"- [{source.upper()}] {ref}: {clean_doc}...\n"

    return output
