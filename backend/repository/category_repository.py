from backend.db.hana import get_connection


def get_categories():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                CATEGORY_ID,
                CATEGORY_NAME,
                DESCRIPTION
            FROM CASE_CATEGORIES
            ORDER BY CATEGORY_ID
        """)

        rows = cursor.fetchall()

        return [
            {
                "category_id": row[0],
                "category_name": row[1],
                "description": row[2],
            }
            for row in rows
        ]

    finally:
        conn.close()