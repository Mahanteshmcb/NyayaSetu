"""SAP HANA Cloud connection helper. Credentials must come from environment variables."""
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    try:
        from hdbcli import dbapi
    except ImportError as exc:
        raise RuntimeError("hdbcli is not installed. Run: python -m pip install -r requirements.txt") from exc
    host = os.getenv("HANA_HOST", "").strip()
    user = os.getenv("HANA_USER", "").strip()
    password = os.getenv("HANA_PASSWORD", "")
    if not host or not user or not password:
        raise RuntimeError("HANA credentials are missing. Configure HANA_HOST, HANA_USER, and HANA_PASSWORD in the project-root .env file.")
    try:
        port = int(os.getenv("HANA_PORT", "443"))
    except ValueError as exc:
        raise RuntimeError("HANA_PORT must be an integer, normally 443 for SAP HANA Cloud.") from exc
    encrypt = os.getenv("HANA_ENCRYPT", "true").lower() in {"1", "true", "yes"}
    # HANA Cloud connections should use TLS. Avoid disabling certificate validation in production.
    kwargs = {"address": host, "port": port, "user": user, "password": password, "encrypt": encrypt}
    validate = os.getenv("HANA_VALIDATE_CERTIFICATE", "true").lower() in {"1", "true", "yes"}
    if encrypt:
        kwargs["sslValidateCertificate"] = validate
    return dbapi.connect(**kwargs)
