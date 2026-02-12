import os
import sys
from dotenv import load_dotenv

load_dotenv()

REQUIRED_ENV_VARS = [
    "JIRA_URL",
    "JIRA_PROJECT_KEY",
    "CONFLUENCE_URL",
    "CONFLUENCE_SPACE_KEY",
    "ATLASSIAN_USERNAME",
    "ATLASSIAN_TOKEN",
    "GITHUB_TOKEN",
    "GITHUB_REPO",
]


def validate_env() -> dict[str, str]:
    """Validate that all required environment variables are set and non-empty."""
    missing: list[str] = []
    empty: list[str] = []
    values: dict[str, str] = {}

    for var in REQUIRED_ENV_VARS:
        value = os.getenv(var)
        if value is None:
            missing.append(var)
        elif not value.strip():
            empty.append(var)
        else:
            values[var] = value.strip()

    errors: list[str] = []
    if missing:
        errors.append(f"  Missing: {', '.join(missing)}")
    if empty:
        errors.append(f"  Empty:   {', '.join(empty)}")

    if errors:
        print(
            "ERROR: Required environment variables are not configured correctly.\n"
            + "\n".join(errors)
            + "\n\nPlease check your .env file. See .env.example for reference.",
            file=sys.stderr,
        )
        sys.exit(1)

    return values


_env = validate_env()

JIRA_URL: str = _env["JIRA_URL"]
JIRA_PROJECT_KEY: str = _env["JIRA_PROJECT_KEY"]
CONFLUENCE_URL: str = _env["CONFLUENCE_URL"]
CONFLUENCE_SPACE_KEY: str = _env["CONFLUENCE_SPACE_KEY"]
ATLASSIAN_USERNAME: str = _env["ATLASSIAN_USERNAME"]
ATLASSIAN_TOKEN: str = _env["ATLASSIAN_TOKEN"]
GITHUB_TOKEN: str = _env["GITHUB_TOKEN"]
GITHUB_REPO: str = _env["GITHUB_REPO"]
