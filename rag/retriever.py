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