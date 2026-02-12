from typing import TypedDict, Optional


class JiraIssueContext(TypedDict):
    key: str
    summary: str
    status: str
    description: Optional[str]


class ConfluencePageContext(TypedDict):
    page_id: str
    title: str


class KnowledgeItem(TypedDict):
    source: str
    key: Optional[str]  # For Jira
    title: str
    status: Optional[str]  # For Jira
    page_id: Optional[str]  # For Confluence
    content: str
