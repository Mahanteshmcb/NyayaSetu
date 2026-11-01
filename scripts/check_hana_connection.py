"""Check SAP HANA Cloud connectivity and expected NyayaSetu tables.
Run from the project root after configuring .env: python scripts/check_hana_connection.py
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.db.hana import get_connection

EXPECTED = {"CASE_CATEGORIES", "LAW_METADATA", "LAW_CHUNKS"}

def main():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT CURRENT_USER, CURRENT_SCHEMA FROM DUMMY")
            user, schema = cursor.fetchone()
            print(f"Connected to HANA Cloud. User={user}; schema={schema}")
            cursor.execute("SELECT TABLE_NAME FROM SYS.TABLES WHERE SCHEMA_NAME = CURRENT_SCHEMA")
            found = {row[0].upper() for row in cursor.fetchall()}
            missing = EXPECTED - found
            if missing:
                print("Connection succeeded, but expected tables are missing:", ", ".join(sorted(missing)))
                print("Review sql/schema.sql and apply it to the intended schema after checking existing objects.")
                raise SystemExit(2)
            print("Required tables found:", ", ".join(sorted(EXPECTED)))
            cursor.execute("SELECT COUNT(*) FROM LAW_METADATA")
            print("LAW_METADATA rows:", cursor.fetchone()[0])
            cursor.execute("SELECT COUNT(*) FROM LAW_CHUNKS")
            print("LAW_CHUNKS rows:", cursor.fetchone()[0])
        finally:
            cursor.close()
    finally:
        connection.close()

if __name__ == "__main__":
    main()
