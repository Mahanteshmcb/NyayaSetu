from backend.services.classifier import classify
from backend.services.normalizer import normalize_text
from backend.services.validation import validate_description
from backend.retrieval.retriever import retrieve_sources


def analyze_case(description: str, state: str):

    description = validate_description(description)

    normalized = normalize_text(description)

    classification = classify(normalized)

    if classification.category == "unknown":
        return {
            "category": "unknown",
            "confidence": 0.0,
            "needs_clarification": True,
            "clarification_question": (
                "Can you provide more details about whether this "
                "concerns rent/deposit, unpaid wages, termination, "
                "or workplace harassment?"
            ),
            "explanation": "",
            "sources": [],
        }

    if classification.confidence < 0.6:
        return {
            "category": classification.category,
            "confidence": classification.confidence,
            "needs_clarification": True,
            "clarification_question": (
                "Can you provide more details about what happened?"
            ),
            "explanation": "",
            "sources": [],
        }

    sources = retrieve_sources(
        classification.category,
        state
    )

    if not sources:
        return {
            "category": classification.category,
            "confidence": classification.confidence,
            "needs_clarification": True,
            "clarification_question": (
                "The system does not currently have a reviewed "
                "source for this state and category."
            ),
            "explanation": "",
            "sources": [],
        }

    return {
        "category": classification.category,
        "confidence": classification.confidence,
        "needs_clarification": False,
        "clarification_question": None,
        "explanation": (
            "The dispute has been classified for further "
            "source-grounded legal information."
        ),
        "sources": sources,
    }