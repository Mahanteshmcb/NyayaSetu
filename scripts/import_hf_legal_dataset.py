
"""Export a bounded, unapproved candidate subset from Hugging Face.

This is a candidate preparation tool, not a legal validation tool.
It never writes to HANA. Every exported chunk remains pending_review.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

DATASET_ID = "KanoonGPT/indian-legal-documents"
DATASET_URL = (
    "https://huggingface.co/datasets/"
    "KanoonGPT/indian-legal-documents"
)

ROOT = Path(__file__).resolve().parents[1]
OUT_DEFAULT = ROOT / "rag" / "data" / "legal_dataset_candidates.json"

# Conservative title/description matching. A match is only a candidate,
# not proof that the law applies to a user's situation.
CATEGORIES = {
    "rent_or_deposit": [
    "karnataka rent act",
    "rent control act",
    "residential tenancy",
    "residential tenancy act",
    "landlord tenant dispute",
    "landlord and tenant",
    "security deposit",
    "rental security deposit",
    "tenancy agreement",
    "rent agreement",
    "residential lease",
    "refund of rental deposit",
    ],
    "unpaid_wages": [
        "payment of wages",
        "minimum wages",
        "unpaid wages",
        "wages act",
        "bonus act",
        "payment of bonus",
        "payment of gratuity",
        "gratuity act",
    ],
    "termination": [
        "termination of employment",
        "termination of service",
        "dismissal",
        "retrenchment",
        "industrial disputes",
        "industrial employment standing orders",
    ],
    "workplace_harassment": [
        "sexual harassment",
        "workplace harassment",
        "sexual harassment of women at workplace",
        "internal complaints committee",
        "prevention of sexual harassment",
        "posh act",
    ],
}


def normalize_text(value):
    """Normalize text for keyword matching."""
    value = str(value or "").lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def infer_category(title, description=""):
    """Return one unambiguous category or None."""
    searchable = normalize_text(f"{title} {description}")

    matched = []
    for category, terms in CATEGORIES.items():
        if any(normalize_text(term) in searchable for term in terms):
            matched.append(category)

    if len(matched) != 1:
        return None

    return matched[0]


def normalize_jurisdiction(raw_value, include_central):
    """
    Return the supported search scope, or None to exclude the record.

    Preserve raw_value separately. Do not infer Karnataka from a missing
    or ambiguous jurisdiction.
    """
    raw = normalize_text(raw_value)

    if not raw or raw == "unknown":
        return None

    # Explicitly reject other Indian states/territories before considering
    # broad words such as India or national.
    other_jurisdictions = [
        "uttar pradesh", "kerala", "uttarakhand", "odisha",
        "maharashtra", "tamil nadu", "andhra pradesh", "telangana",
        "goa", "gujarat", "rajasthan", "punjab", "haryana",
        "himachal pradesh", "bihar", "jharkhand", "chhattisgarh",
        "madhya pradesh", "west bengal", "assam", "sikkim",
        "arunachal pradesh", "nagaland", "manipur", "mizoram",
        "tripura", "meghalaya", "delhi", "jammu and kashmir",
        "ladakh", "chandigarh", "puducherry",
    ]

    if any(state in raw for state in other_jurisdictions):
        return None

    if "karnataka" in raw:
        return "Karnataka"

    central_labels = {
        "central",
        "central government",
        "government of india",
        "union of india",
        "national",
        "india",
        "all india",
    }

    if include_central and raw in central_labels:
        return "Central"

    return None


def chunk_text(text, size=1800, overlap=250):
    """Split document text into overlapping chunks."""
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(len(text), start + size)

        if end < len(text):
            boundary = text.rfind(". ", start + size // 2, end)
            if boundary > start:
                end = boundary + 1

        part = text[start:end].strip()
        if part:
            chunks.append(part)

        if end >= len(text):
            break

        start = max(start + 1, end - overlap)

    return chunks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-documents",
        type=int,
        default=500,
        help="Maximum dataset rows to inspect (default: 500)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUT_DEFAULT,
    )
    parser.add_argument(
        "--include-central",
        action="store_true",
        help="Include explicitly identified central/national records",
    )
    args = parser.parse_args()

    if args.max_documents < 1:
        raise SystemExit("--max-documents must be at least 1")

    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise SystemExit(
            "Install dataset tools first: pip install -r requirements.txt"
        ) from exc

    dataset = load_dataset(DATASET_ID, split="train", streaming=True)

    candidates = []
    inspected = 0
    rejected_jurisdiction = 0
    rejected_category = 0
    rejected_content = 0

    # Prevent duplicate chunks if the dataset repeats a document ID.
    seen_chunk_ids = set()

    for row in dataset:
        if inspected >= args.max_documents:
            break
        inspected += 1

        title = str(
            row.get("document_title") or "Untitled legal document"
        ).strip()

        raw_jurisdiction = str(
            row.get("document_jurisdiction") or "Unknown"
        ).strip()

        jurisdiction = normalize_jurisdiction(
            raw_jurisdiction,
            args.include_central,
        )

        if jurisdiction is None:
            rejected_jurisdiction += 1
            continue

        description = str(row.get("short_description") or "").strip()
        category = infer_category(title, description)

        if category is None:
            rejected_category += 1
            continue

        content = str(row.get("text") or "").strip()
        if len(content) < 100:
            rejected_content += 1
            continue

        doc_id = str(
            row.get("doc_id")
            or hashlib.sha256(
                (title + content[:500]).encode("utf-8")
            ).hexdigest()[:20]
        )

        source_id = f"HF-{doc_id}"

        for index, chunk in enumerate(chunk_text(content)):
            chunk_id = "HF-" + hashlib.sha1(
                (doc_id + str(index)).encode("utf-8")
            ).hexdigest()[:24]

            if chunk_id in seen_chunk_ids:
                continue
            seen_chunk_ids.add(chunk_id)

            candidates.append({
                "chunk_id": chunk_id,
                "source_id": source_id,
                "category": category,
                "title": title,
                "authority": str(
                    row.get("issuing_authority") or "Not specified"
                ),
                # Canonical scope used by the application.
                "jurisdiction": jurisdiction,
                # Preserve the original dataset value for auditing.
                "source_jurisdiction": raw_jurisdiction,
                "content": chunk,
                # This is the dataset URL, not the official law URL.
                "source_url": DATASET_URL,
                "official_source_url": "",
                "source_type": str(
                    row.get("document_type") or "legal_document"
                ),
                "issue_date": str(row.get("issue_date") or ""),
                "dataset_id": DATASET_ID,
                "dataset_doc_id": doc_id,
                "provenance": (
                    "kanoongpt_indian_legal_documents_candidate"
                ),
                "review_status": "pending_review",
                "review_note": (
                    "Machine-filtered candidate. Verify the instrument, "
                    "current validity, actual jurisdiction, category "
                    "relevance, full text, and official source before "
                    "approval."
                ),
            })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Dataset rows inspected: {inspected}")
    print(f"Candidate chunks exported: {len(candidates)}")
    print(f"Rows rejected by jurisdiction: {rejected_jurisdiction}")
    print(f"Rows rejected by category: {rejected_category}")
    print(f"Rows rejected by short/missing content: {rejected_content}")
    print(f"Output: {args.output}")
    print("All exported records remain pending_review.")
    print("No HANA writes performed.")
    print("Keyword matches are not legal validation.")


if __name__ == "__main__":
    main()
 