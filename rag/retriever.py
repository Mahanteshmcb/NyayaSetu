<<<<<<< HEAD
import json, math, os
from pathlib import Path
from dl.embeddings.encoder import encode_text
DATA_DIR = Path(__file__).parent / "data"
DEV_DATA_PATH = DATA_DIR / "legal_documents.json"
APPROVED_DATA_PATH = DATA_DIR / "legal_documents_approved.json"

def _load_documents():
    documents = []
    # Only records explicitly reviewed and promoted to the approved corpus are trusted as reviewed candidates.
    if APPROVED_DATA_PATH.exists():
        approved = json.loads(APPROVED_DATA_PATH.read_text(encoding="utf-8"))
        documents.extend(d for d in approved if d.get("review_status") == "approved")
    if os.getenv("USE_DEV_FIXTURES", "true").lower() in {"1", "true", "yes"}:
        documents.extend(json.loads(DEV_DATA_PATH.read_text(encoding="utf-8")))
    return documents

def _similarity(a, b):
    n = min(len(a), len(b))
    if not n: return 0.0
    dot = sum(float(a[i]) * float(b[i]) for i in range(n))
    na = math.sqrt(sum(float(x)*float(x) for x in a[:n]))
    nb = math.sqrt(sum(float(x)*float(x) for x in b[:n]))
    return dot / (na*nb) if na and nb else 0.0

def search_documents(query: str, category: str, state: str, top_k: int = 3):
    query_vec = encode_text(query)
    documents = _load_documents()
    results = []
    for doc in documents:
        doc_category = str(doc.get("category", "general")).lower()
        doc_jurisdiction = str(doc.get("jurisdiction", "")).lower()
        # General and all-India/Central materials may apply across state-level searches.
        category_aliases = {category.lower()}
        if category.lower() in {"rent_or_deposit", "rent_deposit"}:
            category_aliases.update({"rent_or_deposit", "rent_deposit"})
        category_ok = doc_category in category_aliases | {"general", "procedure", "other", "evidence"}
        jurisdiction_ok = (doc_jurisdiction == state.lower() or doc_jurisdiction in {"india", "central", "all india", "india (central)", "user evidence - not legal authority", "not specified"})
        if not category_ok or not jurisdiction_ok:
            continue
        score = _similarity(query_vec, encode_text(doc["content"] + " " + doc["title"]))
        results.append({"chunk_id": doc["chunk_id"], "source_id": doc["source_id"], "content": doc["content"],
                        "title": doc["title"], "authority": doc["authority"], "jurisdiction": doc["jurisdiction"],
                        "category": doc["category"], "score": score, "provenance": doc.get("provenance", "unknown"), "review_status": doc.get("review_status", "development_fixture"), "source_url": doc.get("official_source_url") or doc.get("source_url")})
    return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
=======
import json
import numpy as np

from dl.embeddings.encoder import encode_text


DATA_FILE = "rag/data/legal_documents.json"


def load_documents():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return float(np.dot(a, b))


def search_documents(
    query: str,
    category: str | None = None,
    state: str | None = None,
    top_k: int = 3
):
    documents = load_documents()

    query_embedding = encode_text(query)

    results = []

    for document in documents:

        if category and document["category"] != category:
            continue

        if state and document["state"] != state:
            continue

        document_embedding = encode_text(document["text"])

        score = cosine_similarity(
            query_embedding,
            document_embedding
        )

        results.append({
            "chunk_id": document["chunk_id"],
            "source_id": document["source_id"],
            "category": document["category"],
            "state": document["state"],
            "title": document["title"],
            "text": document["text"],
            "score": score
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]
>>>>>>> origin/main
