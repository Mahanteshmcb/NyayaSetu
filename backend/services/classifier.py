from dataclasses import dataclass


@dataclass
class ClassificationResult:
    category: str
    confidence: float


CATEGORY_KEYWORDS = {
    "rent_or_deposit": [
        "rent",
        "deposit",
        "landlord",
        "tenant",
        "house",
        "rental",
    ],
    "unpaid_wages": [
        "salary",
        "wage",
        "wages",
        "payment",
        "employer",
        "pay",
        "paid",
    ],
    "termination": [
        "fired",
        "termination",
        "terminated",
        "dismissed",
        "job",
        "employment",
    ],
    "workplace_harassment": [
        "harassment",
        "abuse",
        "threat",
        "workplace",
        "manager",
        "colleague",
    ],
}


def classify(text: str) -> ClassificationResult:
    text = text.lower()

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(
            1 for keyword in keywords
            if keyword in text
        )
        scores[category] = score

    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]

    if best_score == 0:
        return ClassificationResult(
            category="unknown",
            confidence=0.0
        )

    confidence = min(0.95, 0.5 + (best_score * 0.1))

    return ClassificationResult(
        category=best_category,
        confidence=confidence
    )