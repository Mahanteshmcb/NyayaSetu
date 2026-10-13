import json
import hashlib

from dl.embeddings.encoder import encode_text
from backend.db.law_repository import (
    insert_source,
    insert_chunk
)


DATA_FILE = "rag/data/legal_documents.json"

EMBEDDING_MODEL = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


def content_hash(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def main():

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)

    print(f"Found {len(documents)} documents")

    for document in documents:

        source_id = document["source_id"]
        chunk_id = document["chunk_id"]
        text = document["text"]
        category = document["category"]
        state = document["state"]

        print(f"\nProcessing {chunk_id}...")

        # Generate embedding
        embedding = encode_text(text)

        print(
            f"Embedding generated: "
            f"{len(embedding)} dimensions"
        )

        # Insert source metadata
        try:
            insert_source(
                source_id=source_id,
                title=document["title"],
                authority="Development Fixture",
                source_type="development_fixture",
                jurisdiction=state,
                review_status="PENDING_REVIEW",
                license_terms=(
                    "Development-only fixture; "
                    "not an approved legal source."
                )
            )

            print(f"Inserted source: {source_id}")

        except Exception as error:
            print(
                f"Source insertion failed: {error}"
            )
            continue

        # Insert chunk and vector
        try:
            insert_chunk(
                chunk_id=chunk_id,
                source_id=source_id,
                content=text,
                section_boundary="Development fixture",
                content_hash=content_hash(text),
                embedding_model=EMBEDDING_MODEL,
                embedding=embedding
            )

            print(f"Inserted chunk: {chunk_id}")

        except Exception as error:
            print(
                f"Chunk insertion failed: {error}"
            )

    print("\nHANA ingestion completed.")


if __name__ == "__main__":
    main()