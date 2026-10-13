from backend.db.hana import get_connection


def insert_source(
    source_id,
    title,
    authority,
    source_type,
    jurisdiction,
    review_status,
    license_terms=None
):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO LAW_METADATA (
            SOURCE_ID,
            TITLE,
            AUTHORITY,
            JURISDICTION,
            RETRIEVAL_DATE,
            SOURCE_TYPE,
            LICENSE_TERMS,
            REVIEW_STATUS
        )
        VALUES (
            ?, ?, ?, ?, CURRENT_DATE, ?, ?, ?
        )
    """

    cursor.execute(
        sql,
        (
            source_id,
            title,
            authority,
            jurisdiction,
            source_type,
            license_terms,
            review_status
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


def insert_chunk(
    chunk_id,
    source_id,
    content,
    section_boundary,
    content_hash,
    embedding_model,
    embedding
):
    connection = get_connection()
    cursor = connection.cursor()

    vector_string = "[" + ",".join(
        str(float(value))
        for value in embedding
    ) + "]"

    sql = """
        INSERT INTO LAW_CHUNKS (
            CHUNK_ID,
            SOURCE_ID,
            SECTION_BOUNDARY,
            CONTENT,
            CONTENT_HASH,
            EMBEDDING_MODEL,
            INGESTION_TIMESTAMP,
            EMBEDDING
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, TO_REAL_VECTOR(?)
        )
    """

    cursor.execute(
        sql,
        (
            chunk_id,
            source_id,
            section_boundary,
            content,
            content_hash,
            embedding_model,
            vector_string
        )
    )

    connection.commit()

    cursor.close()
    connection.close()