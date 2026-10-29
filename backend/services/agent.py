import os
from backend.services.validation import validate_description
from backend.services.normalizer import normalize_text
from backend.services.ml_classifier import predict_category
from rag.retriever import search_documents

CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.40"))
RETRIEVAL_THRESHOLD = float(os.getenv("RETRIEVAL_THRESHOLD", "0.35"))


def _retrieve(query: str, category: str, state: str):
    if os.getenv("USE_HANA", "false").lower() in {"1", "true", "yes"}:
        from rag.hana_retriever import search_hana
        return search_hana(query=query, category=category, state=state, top_k=3)
    return search_documents(query=query, category=category, state=state, top_k=3)


def analyze_case(description: str, state: str, language: str = "auto"):
    validate_description(description)
    normalized = normalize_text(description)
    classification = predict_category(normalized)
    category = classification["category"]
    confidence = float(classification["confidence"])

    if category == "unknown" or confidence < CONFIDENCE_THRESHOLD:
        return {"category": category, "confidence": confidence, "needs_clarification": True,
                "clarification_question": "Can you share a little more detail, such as what happened, when it happened, and what outcome you are seeking?",
                "explanation": "", "sources": []}

    results = _retrieve(normalized, category, state)
    results = [r for r in results if float(r.get("score", 0)) >= RETRIEVAL_THRESHOLD]
    if not results:
        return {"category": category, "confidence": confidence, "needs_clarification": True,
                "clarification_question": "I could not find sufficiently relevant information for this situation. Can you add more details?",
                "explanation": "", "sources": []}

    # Dev fixtures are not legal authorities. Explicitly disclose that provenance in the response.
    sources = [{"source_id": r["source_id"], "title": r["title"], "authority": r.get("authority", "Not specified"),
                "jurisdiction": r.get("jurisdiction", state), "score": round(float(r.get("score", 0)), 4),
                "provenance": r.get("provenance", "development_fixture"), "review_status": r.get("review_status", "development_fixture"), "source_url": r.get("source_url")} for r in results]
    best = results[0]
    if best.get("review_status") == "approved":
        explanation = (f"Your description appears related to {category.replace('_', ' ')}. "
                       f"The retrieved reviewed source, '{best['title']}', may provide relevant legal context. "
                       "Check the source and its current applicability to your facts; this is general legal information, not a determination of your rights or case outcome.")
    else:
        explanation = (f"Your description appears related to {category.replace('_', ' ')}. "
                       f"The retrieved item '{best['title']}' is available as development context. "
                       "The included development records are synthetic and do not establish your legal rights. "
                       "Please verify applicable law and facts with a qualified legal professional.")
    return {"category": category, "confidence": confidence, "needs_clarification": False,
            "clarification_question": None, "explanation": explanation, "sources": sources}
