"""Transparent keyword baseline. Replace with a trained and evaluated model for production."""
RULES = {
 "rent_or_deposit": ["landlord", "tenant", "rent", "deposit", "security deposit", "rental", "lease", "house owner"],
 "unpaid_wages": ["salary", "wage", "unpaid", "payroll", "overtime", "not paid", "payment due"],
 "termination": ["fired", "terminated", "termination", "dismissed", "job loss", "employment ended", "notice period"],
 "workplace_harassment": ["harassment", "sexual harassment", "workplace bullying", "hostile workplace", "inappropriate touching", "threatened at work"]
}

def predict_category(text: str) -> dict:
    text = text.lower()
    scores = {category: sum(1 for term in terms if term in text) for category, terms in RULES.items()}
    best = max(scores, key=scores.get)
    hits = scores[best]
    if hits == 0:
        return {"category": "unknown", "confidence": 0.0, "scores": scores}
    # Conservative, heuristic confidence; not a calibrated probability.
    confidence = min(0.95, 0.35 + 0.18 * hits)
    return {"category": best, "confidence": round(confidence, 4), "scores": scores}
