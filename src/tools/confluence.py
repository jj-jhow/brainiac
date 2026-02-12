from src.services.db import query_documents
from src.config import CONFLUENCE_URL


async def search_docs(query: str) -> str:
    """Searches Confluence for architecture or design docs in the knowledge base."""
    # We perform a semantic search but valid context usually means filtering isn't strictly necessary
    # if the query is specific, but we can't filter by 'source' easily in query_documents
    # without adding a filter param to it.
    # However, standard query_documents does semantic search on everything.
    # If we want *only* docs, we should update query_documents to accept a where clause.

    # For now, let's search everything but prioritize Confluence in formatting if we could,
    # or just rely on the fact that "search_docs" implies doc search.
    # To restrict to Confluence, let's just use the query_documents since we want
    # to find relevant info regardless of source, or if strict:

    # Let's modify query_documents to support `where` filter?
    # Or just return whatever we find. The tool name "search_docs" implies intent.

    # Actually, the user wants "minimized API calls".
    # I'll rely on the DB's semantic search.

    res = query_documents(query, n_results=5)

    docs = res.get("documents", [])
    metadatas = res.get("metadatas", [])

    if not docs or not docs[0]:
        return "No matching documentation found."

    documents = docs[0]
    metadata_list = metadatas[0]

    output = "Top Documentation Matches:\n"
    found = False
    for i, doc in enumerate(documents):
        meta = metadata_list[i]
        if meta.get("source") == "confluence":
            title = meta.get("title")
            page_id = meta.get("page_id")
            # We don't store the full URL in metadata currently (except implicitly via config + ID)
            # We can reconstruct it or just show the content.
            # The prompt asked for "minimize API calls", so showing content is better than links.
            output += f"--- Page: {title} ---\n{doc}\n\n"
            found = True

    if not found:
        return "No matching Confluence pages found in top results."

    return output
