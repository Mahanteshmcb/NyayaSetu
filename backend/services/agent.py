from backend.services.validation import validate_description
from backend.services.normalizer import normalize_text
from backend.services.ml_classifier import predict_category
from backend.services.explainer import build_explanation
from rag.hana_retriever import search_hana


CONFIDENCE_THRESHOLD = 0.40
RETRIEVAL_THRESHOLD = 0.35

LEGAL_DISCLAIMER = (
    "This is general legal information, not legal advice. "
    "Applicable law and the facts of your situation must be verified."
)


def clarification_response(
    category: str,
    confidence: float,
    question: str,
    uncertainty: str,
) -> dict:
    """Return a safe response when more information is needed."""

    return {
        "category": category,
        "confidence": confidence,
        "needs_clarification": True,
        "clarification_question": question,
        "explanation": "",
        "uncertainty": uncertainty,
        "disclaimer": LEGAL_DISCLAIMER,
        "sources": [],
    }
from types import SimpleNamespace


def classify(description: str):
    """
    Classify a dispute and return an object with attributes
    expected by the existing classifier tests.
    """
    validate_description(description)
    normalized = normalize_text(description)
    result = predict_category(normalized)

    return SimpleNamespace(
        category=result["category"],
        confidence=result["confidence"],
    )

def analyze_case(description: str, state: str) -> dict:
    """
    Analyze a dispute using:
    1. Input validation
    2. Text normalization
    3. ML classification
    4. Jurisdiction/category-filtered HANA retrieval
    5. Grounded explanation and uncertainty reporting
    """

    # Step 1: Validate the user's description.
    validate_description(description)

    # Step 2: Normalize the text before classification and retrieval.
    normalized = normalize_text(description)

    # Step 3: Predict the dispute category.
    classification = predict_category(normalized)

    category = classification["category"]
    confidence = float(classification["confidence"])

    # Step 4: Ask for clarification when classification is uncertain.
    if (
        category == "unknown"
        or confidence < CONFIDENCE_THRESHOLD
    ):
        return clarification_response(
            category=category,
            confidence=confidence,
            question=(
                "Can you explain what happened, who is involved, "
                "and what outcome you are seeking?"
            ),
            uncertainty=(
                "The system could not classify the dispute "
                "with sufficient confidence."
            ),
        )

    # Step 5: Retrieve material matching the predicted category
    # and the user's jurisdiction.
    results = search_hana(
        query=normalized,
        category=category,
        state=state,
        top_k=3,
    )

    # Step 6: Keep results that meet the retrieval threshold.
    results = [
        result
        for result in results
        if float(result.get("score", 0.0)) >= RETRIEVAL_THRESHOLD
    ]

    # Step 7: Fail safely when no relevant source is found.
    if not results:
        return clarification_response(
            category=category,
            confidence=confidence,
            question=(
                "I could not find sufficiently relevant material "
                "for your jurisdiction and dispute category. "
                "Can you provide more details about the situation?"
            ),
            uncertainty=(
                "No retrieved source met the relevance threshold. "
                "The system cannot provide a grounded explanation "
                "for this request."
            ),
        )

    # Step 8: Generate an explanation using retrieved material.
    explanation_data = build_explanation(
        category=category,
        results=results,
    )

    # Step 9: Return source provenance with the explanation.
    sources = [
        {
            "source_id": result["source_id"],
            "title": result["title"],
            "authority": result.get("authority"),
            "jurisdiction": result.get("jurisdiction"),
        }
        for result in results
    ]

    return {
        "category": category,
        "confidence": confidence,
        "needs_clarification": False,
        "clarification_question": None,
        "explanation": explanation_data["explanation"],
        "uncertainty": explanation_data["uncertainty"],
        "disclaimer": LEGAL_DISCLAIMER,
        "sources": sources,
    }