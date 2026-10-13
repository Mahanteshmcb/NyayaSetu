from backend.db.hana import get_connection
from dl.embeddings.encoder import encode_text


def search_hana(
    query: str,
    category: str,
    state: str,
    top_k: int = 3
):
    query_embedding = encode_text(query)

    vector_string = "[" + ",".join(
        str(float(value))
        for value in query_embedding
    ) + "]"

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        SELECT
            c.CHUNK_ID,
            c.SOURCE_ID,
            c.CONTENT,
            m.TITLE,
            m.AUTHORITY,
            m.JURISDICTION,
            m.CATEGORY_ID,
            COSINE_SIMILARITY(
                c.EMBEDDING,
                TO_REAL_VECTOR(?)
            ) AS SCORE
        FROM LAW_CHUNKS c
        JOIN LAW_METADATA m
            ON c.SOURCE_ID = m.SOURCE_ID
        WHERE m.CATEGORY_ID = ?
          AND m.JURISDICTION = ?
        ORDER BY SCORE DESC
        LIMIT ?
    """

    cursor.execute(
        sql,
        (
            vector_string,
            category,
            state,
            top_k
        )
    )

    rows = cursor.fetchall()

    results = []

    for row in rows:
        results.append({
            "chunk_id": row[0],
            "source_id": row[1],
            "content": row[2],
            "title": row[3],
            "authority": row[4],
            "jurisdiction": row[5],
            "category": row[6],
            "score": float(row[7])
        })

    cursor.close()
    connection.close()

    return results