from backend.db.hana import get_connection


def test_hana_connection():

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT CURRENT_UTCTIMESTAMP FROM DUMMY")

        result = cursor.fetchone()

        assert result is not None

    finally:
        connection.close()