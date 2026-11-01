<<<<<<< HEAD
"""Ingest reviewed legal chunks into HANA. Development fixtures require an explicit flag."""
import argparse, json
from pathlib import Path
from backend.db.hana import get_connection
ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "rag" / "data" / "legal_documents_approved.json"
DEV = ROOT / "rag" / "data" / "legal_documents.json"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-dev-fixtures", action="store_true", help="Include synthetic fixtures for local testing only")
    args = parser.parse_args()
    records = []
    if APPROVED.exists():
        records.extend(d for d in json.loads(APPROVED.read_text(encoding="utf-8")) if d.get("review_status") == "approved")
    if args.include_dev_fixtures:
        records.extend(json.loads(DEV.read_text(encoding="utf-8")))
    if not records:
        raise SystemExit("No approved records found. Review candidates, create legal_documents_approved.json with review_status='approved', or pass --include-dev-fixtures for development only.")
    from dl.embeddings.encoder import encode_text
    conn = get_connection()
    try:
        cur = conn.cursor()
        try:
            for d in records:
                vector = "[" + ",".join(str(float(x)) for x in encode_text(d["content"])) + "]"
                review_status = d.get("review_status", "development_fixture")
                cur.execute("UPSERT LAW_METADATA (SOURCE_ID,TITLE,AUTHORITY,JURISDICTION,CATEGORY_ID,SOURCE_URL,SOURCE_TYPE,REVIEW_STATUS) VALUES (?,?,?,?,?,?,?,?) WITH PRIMARY KEY",
                    (d["source_id"], d["title"], d.get("authority", "Not specified"), d["jurisdiction"], d["category"], d.get("official_source_url") or d.get("source_url"), d.get("source_type", "legal_document"), review_status))
                cur.execute("UPSERT LAW_CHUNKS (CHUNK_ID,SOURCE_ID,CONTENT,EMBEDDING_MODEL,EMBEDDING) VALUES (?,?,?,?,TO_REAL_VECTOR(?)) WITH PRIMARY KEY",
                    (d["chunk_id"], d["source_id"], d["content"], "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", vector))
            conn.commit()
            print(f"Ingested {len(records)} records. Verify provenance and review status in HANA.")
        finally: cur.close()
    finally: conn.close()
if __name__ == "__main__": main()
=======
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
>>>>>>> origin/main
