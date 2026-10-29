import json
from collections import defaultdict
from pathlib import Path

source_file = Path("rag/data/legal_dataset_candidates.json")
output_file = Path("rag/data/legal_sources_review.json")

records = json.loads(source_file.read_text(encoding="utf-8"))
groups = defaultdict(list)

for record in records:
    groups[record["source_id"]].append(record)

keywords = {
    "rent_or_deposit": [
        "rent", "tenancy", "tenant", "landlord",
        "lease", "security deposit"
    ],
    "unpaid_wages": [
        "wage", "salary", "payment of wages",
        "minimum wages", "gratuity", "labour", "labor"
    ],
    "termination": [
        "termination of employment", "dismissal",
        "retrenchment", "industrial disputes",
        "standing orders", "termination of service"
    ],
    "workplace_harassment": [
        "workplace harassment", "sexual harassment",
        "posh", "internal complaints committee"
    ],
}

review = []

for source_id, chunks in sorted(groups.items()):
    first = chunks[0]
    title = first.get("title", "").lower()

    possible_categories = [
        category
        for category, terms in keywords.items()
        if any(term in title for term in terms)
    ]

    review.append({
        "source_id": source_id,
        "title": first.get("title"),
        "source_jurisdiction": first.get("source_jurisdiction"),
        "authority": first.get("authority"),
        "candidate_category": first.get("category"),
        "possible_categories_from_title": possible_categories,
        "chunk_count": len(chunks),
        "source_url": first.get("official_source_url"),
        "dataset_url": first.get("source_url"),
        "review_status": "pending_review",
        "review_note": "Title-based screening only. Verify full text, jurisdiction, current validity, and official source."
    })

output_file.write_text(
    json.dumps(review, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("Unique source groups:", len(review))
print("Saved review report:", output_file)
print("Still pending review:", sum(x["review_status"] == "pending_review" for x in review))
print("\nPotentially relevant titles:")

for item in review:
    if item["possible_categories_from_title"]:
        print(
            item["title"],
            "|", item["source_jurisdiction"],
            "|", item["possible_categories_from_title"],
            "| chunks:", item["chunk_count"]
        )
