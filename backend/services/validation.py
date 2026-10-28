class InputValidationError(ValueError):
    pass

def validate_description(description: str) -> None:
    if not isinstance(description, str) or len(description.strip()) < 5:
        raise InputValidationError("Please describe the situation in at least 5 characters.")
    if len(description) > 8000:
        raise InputValidationError("Description is too long; limit it to 8000 characters.")
