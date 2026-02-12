from atlassian import Jira, Confluence
from github import Github, Auth
from src.config import (
    JIRA_URL,
    JIRA_PROJECT_KEY,
    CONFLUENCE_URL,
    CONFLUENCE_SPACE_KEY,
    ATLASSIAN_USERNAME,
    ATLASSIAN_TOKEN,
    GITHUB_TOKEN,
)


class JiraService:
    def __init__(self):
        self.client = Jira(
            url=JIRA_URL,
            username=ATLASSIAN_USERNAME,
            password=ATLASSIAN_TOKEN,
            cloud=True,
        )
        self.project_key = JIRA_PROJECT_KEY

    def get_issue(self, issue_key: str):
        return self.client.issue(key=issue_key)

    def search_issues(self, jql: str, start=0, limit=50):
        return self.client.jql(jql, start=start, limit=limit)


class ConfluenceService:
    def __init__(self):
        self.client = Confluence(
            url=CONFLUENCE_URL,
            username=ATLASSIAN_USERNAME,
            password=ATLASSIAN_TOKEN,
            cloud=True,
        )
        self.space_key = CONFLUENCE_SPACE_KEY

    def search(self, query: str, limit=3):
        cql = f'type = page AND text ~ "{query}"'
        response = self.client.cql(cql, limit=limit)
        return response.get("results", [])

    def get_pages_from_space(self, start=0, limit=50):
        return self.client.get_all_pages_from_space(
            self.space_key, start=start, limit=limit, expand="body.storage"
        )


class GitHubService:
    def __init__(self):
        self.client = Github(auth=Auth.Token(GITHUB_TOKEN))

    def get_pr(self, repo_name: str, pr_number: int):
        repo = self.client.get_repo(repo_name)
        return repo.get_pull(pr_number)

    def get_all_prs(self, repo_name: str, state="all", sort="updated", direction="desc", limit=50):
        repo = self.client.get_repo(repo_name)
        return repo.get_pulls(state=state, sort=sort, direction=direction)[:limit]


# Singleton instances
jira_service = JiraService()
confluence_service = ConfluenceService()
github_service = GitHubService()
