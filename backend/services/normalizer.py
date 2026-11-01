import re

<<<<<<< HEAD
def normalize_text(text: str) -> str:
    """Normalize whitespace and case without removing user-provided facts."""
    return re.sub(r"\s+", " ", text).strip().lower()
=======

def normalize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    return text
>>>>>>> origin/main
