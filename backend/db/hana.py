import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    """Create a HANA connection; credentials are read only from environment variables."""
    try:
        from hdbcli import dbapi
    except ImportError as exc:
        raise RuntimeError("hdbcli is not installed. Run pip install -r requirements.txt") from exc
    host = os.getenv("HANA_HOST", "").strip()
    user = os.getenv("HANA_USER", "").strip()
    password = os.getenv("HANA_PASSWORD", "")
    if not host or not user or not password:
        raise RuntimeError("HANA credentials are missing. Configure HANA_HOST, HANA_USER, and HANA_PASSWORD in .env")
    return dbapi.connect(address=host, port=int(os.getenv("HANA_PORT", "443")), user=user, password=password,
                         encrypt=os.getenv("HANA_ENCRYPT", "true").lower() in {"1", "true", "yes"})
