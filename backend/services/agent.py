from backend.services.validation import validate_description
from backend.services.normalizer import normalize_text
from backend.services.ml_classifier import predict_category
from rag.retriever import search_documents


CONFIDENCE_THRESHOLD = 0.40
RETRIEVAL_THRESHOLD = 0.35


def analyze_case(description: str, state: str):

    # 1. Validate input
    validate_description(description)

    # 2. Normalize input
    normalized = normalize_text(description)

    # 3. Classify dispute
    classification = predict_category(normalized)

    category = classification["category"]
    confidence = classification["confidence"]

    # 4. Handle unknown / low-confidence classification
    if category == "unknown" or confidence < CONFIDENCE_THRESHOLD:
        return {
            "category": category,
            "confidence": confidence,
            "needs_clarification": True,
            "clarification_question": (
                "Can you provide more details about what happened?"
            ),
            "explanation": "",
            "sources": []
        }

    # 5. Semantic retrieval
    results = search_documents(
        query=normalized,
        category=category,
        state=state,
        top_k=3
    )

    # 6. Remove weak retrieval results
    results = [
        result
        for result in results
        if result["score"] >= RETRIEVAL_THRESHOLD
    ]

    # 7. No evidence → clarify instead of inventing
    if not results:
        return {
            "category": category,
            "confidence": confidence,
            "needs_clarification": True,
            "clarification_question": (
                "I could not find sufficiently relevant information "
                "for this case. Can you provide more details?"
            ),
            "explanation": "",
            "sources": []
        }

    # 8. Build explanation from retrieved evidence
    best_result = results[0]

    explanation = (
        f"Your issue appears to relate to "
        f"{category.replace('_', ' ')}. "
        f"Relevant information was found regarding "
        f"{best_result['title']}."
    )

    # 9. Convert retrieval results to API sources
    sources = [
        {
            "source_id": result["source_id"],
            "title": result["title"],
            "authority": "Development Fixture",
            "jurisdiction": result["state"]
        }
        for result in results
    ]

    return {
        "category": category,
        "confidence": confidence,
        "needs_clarification": False,
        "clarification_question": None,
        "explanation": explanation,
        "sources": sources
    }