from src.services.db import get_document
from src.config import GITHUB_REPO


async def get_pr_context(repo_name: str, pr_number: int) -> str:
    """Retrieves PR discussion and diff summary from the knowledge base."""
    # Note: repo_name might differ if the user queries a different repo than configured,
    # but we only ingest GITHUB_REPO.

    # We ignore repo_name if it doesn't match config, or we just trust the query matches ingestion.

    result = get_document(
        where={
            "$and": [
                {"source": "github"},
                {"pr_number": int(pr_number)},
                {"repo": repo_name},
            ]
        }
    )

    docs = result.get("documents", [])
    if not docs:
        return f"PR #{pr_number} in {repo_name} not found in knowledge base."

    return docs[0]
