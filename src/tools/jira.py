from src.services.db import get_document


async def get_jira_ticket(issue_key: str) -> str:
    """Fetches details for a specific Jira ticket from the knowledge base."""
    # Look for exact match on 'key' metadata from 'jira' source
    result = get_document(where={"$and": [{"source": "jira"}, {"key": issue_key}]})

    docs = result.get("documents", [])
    if not docs:
        return f"Ticket {issue_key} not found in knowledge base."

    # Return the stored content, which already includes Summary, Status, Desc
    return docs[0]
