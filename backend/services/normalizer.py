import re

def normalize_text(text: str) -> str:
    """Normalize whitespace and case without removing user-provided facts."""
    return re.sub(r"\s+", " ", text).strip().lower()
