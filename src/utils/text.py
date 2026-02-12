def clean_text(text: str) -> str:
    """Removes newlines and truncates text."""
    if not text:
        return ""
    return text.replace("\n", " ")[:200]
