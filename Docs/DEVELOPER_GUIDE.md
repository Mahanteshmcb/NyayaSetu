# Developer Guide

1. Create and activate a Python virtual environment.
2. Install `requirements.txt`.
3. Copy `.env.example` to `.env`; never commit `.env`.
4. Run the API: `python -m uvicorn backend.main:app --reload --port 8008`.
5. Visit `/docs`; test `/health` first, then `POST /analyze`.
6. Run `pytest -q` before changes are committed.
7. To use HANA, set `USE_HANA=true`, confirm credentials, apply the schema after checking existing tenant tables, and ensure vector dimensions match the embedding model.
8. Run frontend separately with `cd frontend; npm install; npm run dev`.

PowerShell test request:
```powershell
curl.exe -X POST "http://127.0.0.1:8008/analyze" -H "Content-Type: application/json" -d '{"description":"My landlord refuses to return my deposit.","state":"Karnataka"}'
```

If Swagger shows “Failed to fetch”, check the terminal running Uvicorn for a traceback, then test `/health` and the POST endpoint with `curl.exe`. Do not assume it is a CORS problem without checking the server log.
