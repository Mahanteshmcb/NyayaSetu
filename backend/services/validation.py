<<<<<<< HEAD
class InputValidationError(ValueError):
    pass

def validate_description(description: str) -> None:
    if not isinstance(description, str) or len(description.strip()) < 5:
        raise InputValidationError("Please describe the situation in at least 5 characters.")
    if len(description) > 8000:
        raise InputValidationError("Description is too long; limit it to 8000 characters.")
=======
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
>>>>>>> origin/main
