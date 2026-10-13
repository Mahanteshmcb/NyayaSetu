MAX_DESCRIPTION_LENGTH = 5000


def validate_description(description: str) -> str:
    if not isinstance(description, str):
        raise TypeError("Description must be a string.")

    description = description.strip()

    if not description:
        raise ValueError("Description cannot be empty.")

    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise ValueError(
            f"Description cannot exceed {MAX_DESCRIPTION_LENGTH} characters."
        )

    return description