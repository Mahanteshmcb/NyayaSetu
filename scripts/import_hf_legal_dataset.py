"""Download a bounded candidate subset from KanoonGPT/indian-legal-documents.

This is an ingestion-preparation tool, not a legal validation tool. It exports
candidate chunks with review_status=pending_review. It never writes to HANA.
"""
import argparse, hashlib, json, re
from pathlib import Path

DATASET_ID = "KanoonGPT/indian-legal-documents"
DATASET_URL = "https://huggingface.co/datasets/KanoonGPT/indian-legal-documents"
ROOT = Path(__file__).resolve().parents[1]
OUT_DEFAULT = ROOT / "rag" / "data" / "legal_dataset_candidates.json"
CATEGORIES = {
    "rent_or_deposit": ["security deposit", "landlord", "tenant", "rent agreement", "rent control", "tenancy", "lease"],
    "unpaid_wages": ["unpaid wages", "wages", "minimum wages", "payment of wages", "salary", "bonus", "gratuity"],
    "termination": ["termination of employment", "dismissal", "retrenchment", "industrial disputes", "standing orders", "termination of service"],
    "workplace_harassment": ["sexual harassment", "workplace harassment", "posh", "sexual harassment of women at workplace", "internal complaints committee"],
}

def infer_category(text):
    text = text.lower()
    scores = {cat: sum(1 for term in terms if term in text) for cat, terms in CATEGORIES.items()}
    top = max(scores, key=scores.get)
    # Ambiguous or weak keyword matches are excluded instead of force-labelled.
    if scores[top] < 1 or list(scores.values()).count(scores[top]) > 1:
        return None
    return top

def chunk_text(text, size=1800, overlap=250):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    if not text:
        return []
    chunks, start = [], 0
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
    parser.add_argument("--max-documents", type=int, default=500, help="Maximum documents to inspect (default: 500)")
    parser.add_argument("--output", type=Path, default=OUT_DEFAULT)
    parser.add_argument("--include-central", action="store_true", help="Include central/national jurisdiction documents")
    args = parser.parse_args()
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise SystemExit("Install dataset tools first: pip install -r requirements.txt") from exc

    ds = load_dataset(DATASET_ID, split="train", streaming=True)
    candidates, inspected = [], 0
    for row in ds:
        inspected += 1
        if inspected > args.max_documents:
            break
        title = str(row.get("document_title") or "Untitled legal document").strip()
        jurisdiction = str(row.get("document_jurisdiction") or "Unknown").strip()
        # Keep Karnataka and (optionally) central/national records for the initial MVP.
        jlow = jurisdiction.lower()
        allowed = "karnataka" in jlow or (args.include_central and ("central" in jlow or "india" in jlow or "national" in jlow))
        if not allowed:
            continue
        content = str(row.get("text") or "").strip()
        if len(content) < 100:
            continue
        category = infer_category(title + " " + str(row.get("short_description") or "") + " " + content[:12000])
        if not category:
            continue
        doc_id = str(row.get("doc_id") or hashlib.sha256((title+content[:500]).encode()).hexdigest()[:20])
        for idx, chunk in enumerate(chunk_text(content)):
            chunk_id = f"HF-{hashlib.sha1((doc_id+str(idx)).encode()).hexdigest()[:24]}"
            candidates.append({
                "chunk_id": chunk_id, "source_id": f"HF-{doc_id}", "category": category,
                "title": title, "authority": str(row.get("issuing_authority") or "Not specified"),
                "jurisdiction": "Karnataka", "source_jurisdiction": jurisdiction, "content": chunk,
                "source_url": DATASET_URL, "source_type": str(row.get("document_type") or "legal_document"),
                "issue_date": str(row.get("issue_date") or ""),
                "dataset_id": DATASET_ID, "dataset_doc_id": doc_id,
                "provenance": "kanoongpt_indian_legal_documents_candidate",
                "review_status": "pending_review",
                "review_note": "Machine-filtered candidate. Verify the actual instrument, current validity, jurisdiction, text and official source before approval."
            })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Inspected at most {args.max_documents} dataset rows; exported {len(candidates)} candidate chunks to {args.output}")
    print("No HANA writes performed. Review candidates and confirm against official sources before use.")

if __name__ == "__main__":
    main()
