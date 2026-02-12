from src.services.db import add_documents, clear_collection, inspect_collection
from src.services.clients import jira_service, confluence_service, github_service
from src.config import JIRA_PROJECT_KEY, GITHUB_REPO
import re


def sync_knowledge_base() -> str:
    """Fetches all Jira tickets and Confluence pages, storing them in the vector database."""
    print("Starting synchronization...")
    # Clear existing collection to start fresh
    clear_collection()

    total_docs = 0
    errors = []

    # --- JIRA SYNC ---
    jql = f"project = {JIRA_PROJECT_KEY} ORDER BY created DESC"
    start = 0
    max_results = 50

    while True:
        try:
            results = jira_service.search_issues(jql, start=start, limit=max_results)
        except Exception as e:
            errors.append(f"Jira sync failed: {str(e)}")
            break

        issues = results.get("issues", [])
        if not issues:
            break

        docs = []
        metadatas = []
        ids = []

        for issue in issues:
            key = issue["key"]
            summary = issue["fields"]["summary"]
            # Jira descriptions can be None
            desc = issue["fields"].get("description") or ""
            status = issue["fields"]["status"]["name"]

            # Text to embed
            content = f"Ticket: {key}\nSummary: {summary}\nStatus: {status}\nDescription: {desc}"

            docs.append(content)
            metadatas.append(
                {"source": "jira", "key": key, "status": status, "title": summary}
            )
            # Unique ID for Chroma
            ids.append(key)

        if docs:
            add_documents(docs, metadatas, ids)
            total_docs += len(docs)

        if start + max_results >= results.get("total", 0):
            break
        start += max_results

    # --- CONFLUENCE SYNC ---
    start = 0
    limit = 50

    while True:
        try:
            results = confluence_service.get_pages_from_space(start=start, limit=limit)
        except Exception as e:
            errors.append(f"Confluence sync failed: {str(e)}")
            break

        if not results:
            break

        docs = []
        metadatas = []
        ids = []

        for page in results:
            page_id = page["id"]
            title = page["title"]

            # Extract and clean body content
            body_html = page.get("body", {}).get("storage", {}).get("value", "")
            # Simple tag stripping
            body_text = re.sub(r"<[^>]+>", " ", body_html).strip()
            # Collapse multiple spaces
            body_text = re.sub(r"\s+", " ", body_text)

            content = f"Confluence Page: {title}\nID: {page_id}\nContent: {body_text}"

            docs.append(content)
            metadatas.append(
                {"source": "confluence", "title": title, "page_id": page_id}
            )
            ids.append(f"confluence-{page_id}")

        if docs:
            add_documents(docs, metadatas, ids)
            total_docs += len(docs)

        if len(results) < limit:
            break
        start += limit

    # --- GITHUB SYNC ---
    try:
        # Fetch recent PRs (open and closed)
        prs = github_service.get_all_prs(GITHUB_REPO, limit=50)

        pr_docs = []
        pr_metadatas = []
        pr_ids = []

        for pr in prs:
            pr_number = pr.number
            title = pr.title
            body = pr.body or ""
            author = pr.user.login
            state = pr.state

            # Content for embedding
            content = f"GitHub PR #{pr_number}: {title}\nAuthor: {author}\nState: {state}\nDescription: {body}"

            pr_docs.append(content)
            pr_metadatas.append(
                {
                    "source": "github",
                    "repo": GITHUB_REPO,
                    "pr_number": pr_number,
                    "title": title,
                    "state": state,
                }
            )
            pr_ids.append(f"github-pr-{GITHUB_REPO.replace('/', '-')}-{pr_number}")

        if pr_docs:
            add_documents(pr_docs, pr_metadatas, pr_ids)
            total_docs += len(pr_docs)

    except Exception as e:
        errors.append(f"GitHub sync failed: {str(e)}")

    stats = inspect_collection()
    status_msg = f"Sync complete. {total_docs} items processed. {stats}"
    if errors:
        status_msg += "\nErrors encountered:\n" + "\n".join(errors)

    print(status_msg)
    return status_msg


if __name__ == "__main__":
    import time
    import os

    # Simple loop to run ingestion periodically
    # Default to 1 hour (3600 seconds)
    interval = int(os.getenv("INGESTION_INTERVAL", "3600"))

    print(f"Starting ingestion service with interval {interval}s")

    while True:
        try:
            sync_knowledge_base()
        except Exception as e:
            print(f"Ingestion crashed: {e}")

        print(f"Sleeping for {interval}s...")
        time.sleep(interval)
