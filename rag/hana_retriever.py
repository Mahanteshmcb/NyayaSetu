import os
from backend.db.hana import get_connection
from dl.embeddings.encoder import encode_text

def search_hana(query: str, category: str, state: str, top_k: int = 3):
    embedding = encode_text(query)
    vector_string = "[" + ",".join(str(float(v)) for v in embedding) + "]"
    connection = get_connection()
    try:
        cursor = connection.cursor()
        try:
            sql = """SELECT c.CHUNK_ID, c.SOURCE_ID, c.CONTENT, m.TITLE, m.AUTHORITY,
                     m.JURISDICTION, m.CATEGORY_ID, m.SOURCE_URL, m.REVIEW_STATUS,
                     COSINE_SIMILARITY(c.EMBEDDING, TO_REAL_VECTOR(?)) AS SCORE
                     FROM LAW_CHUNKS c JOIN LAW_METADATA m ON c.SOURCE_ID=m.SOURCE_ID
                     WHERE m.CATEGORY_ID=? AND m.JURISDICTION=?
                       AND (m.REVIEW_STATUS='approved' OR (? = 1 AND m.REVIEW_STATUS='development_fixture'))
                     ORDER BY SCORE DESC LIMIT ?"""
            include_dev = 1 if os.getenv("USE_DEV_FIXTURES", "true").lower() in {"1", "true", "yes"} else 0
            cursor.execute(sql, (vector_string, category, state, include_dev, int(top_k)))
            rows = cursor.fetchall()
            return [{"chunk_id":r[0], "source_id":r[1], "content":r[2], "title":r[3], "authority":r[4],
                     "jurisdiction":r[5], "category":r[6], "source_url":r[7], "review_status":r[8],
                     "score":float(r[9]), "provenance":"hana_database_record"} for r in rows]
        finally:
            cursor.close()
    finally:
        connection.close()
