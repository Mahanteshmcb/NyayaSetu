# SAP HANA Cloud setup for NyayaSetu

## Is HANA required?

No, not to run the local prototype. Keep `USE_HANA=false` to use the local development retriever. HANA becomes useful when you need persistent, centralized storage of reviewed legal sources and embeddings, vector similarity search, and a demonstrable SAP database integration. For the current issue backlog, prioritize #7 (schema/migrations), #8 (ingestion/embeddings), and #10 (vector search). Implement #11 (knowledge graph) and #9 (PAL classifier) only after core retrieval is tested and there is a real need/data for them.

## 1. Create a HANA Cloud instance

1. Open SAP BTP Cockpit and select the subaccount and space for your project.
2. Open SAP HANA Cloud Central and create/start a SAP HANA Cloud database instance if your account/region offers it.
3. Create or identify a database user with permissions to create and read the project tables. Use least privilege for any deployed application.
4. In the instance's connection settings, confirm the SQL endpoint/host and port. HANA Cloud commonly uses port `443`; use the exact endpoint shown by your instance.
5. Ensure your IP/network is permitted by the instance's allowed connections. Never expose the database publicly without network controls.

Availability, free-tier eligibility, UI labels and setup details vary by SAP BTP account and region; follow the current SAP Help documentation and the details displayed for your instance.

## 2. Configure the project

From the project root, create `.env` from `.env.example` if you have not already done so. Fill in only the server-side HANA credentials:

```dotenv
USE_HANA=true
USE_DEV_FIXTURES=false
HANA_HOST=your-instance-host.hanacloud.ondemand.com
HANA_PORT=443
HANA_USER=your_database_user
HANA_PASSWORD=your_database_password
HANA_ENCRYPT=true
HANA_VALIDATE_CERTIFICATE=true
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Do not commit `.env`, put HANA credentials in Vite variables, or expose credentials in the browser. `.env` is read by FastAPI. Restart FastAPI after changing it.

Install dependencies inside the project's activated virtual environment:

```powershell
python -m pip install -r requirements.txt
```

## 3. Apply the schema carefully

Open `sql/schema.sql` in SAP HANA Database Explorer or your approved SQL client. Review it against the target schema before running it. It creates `CASE_CATEGORIES`, `LAW_METADATA`, and `LAW_CHUNKS`; do not rerun blindly if tables already exist. Back up or migrate existing data before changing table definitions. The `LAW_CHUNKS.EMBEDDING` column is `REAL_VECTOR(384)`, so the configured embedding model must produce 384 dimensions. Changing models requires a planned re-embedding and schema/data migration.

## 4. Verify connectivity and tables

From the project root, with the venv active and `.env` configured:

```powershell
python scripts/check_hana_connection.py
```

This checks connectivity, current user/schema, and the presence of expected tables. It does not prove vector search works end-to-end.

## 5. Ingest reviewed legal documents

The ingestion script only accepts approved records from `rag/data/legal_documents_approved.json` by default. Review official provenance, current validity, jurisdiction, category, and text before placing records there. Then run:

```powershell
python scripts/ingest_legal_data.py
```

For local pipeline testing only, synthetic development fixtures can be loaded explicitly:

```powershell
python scripts/ingest_legal_data.py --include-dev-fixtures
```

Keep `USE_DEV_FIXTURES=false` for legal answers based on approved sources only. Synthetic fixtures are not law and must never be presented as legal authority.

## 6. Turn on HANA retrieval

Set `USE_HANA=true` in the root `.env`, restart FastAPI, and run the API test suite. The HANA retriever filters by the predicted category, includes the selected state and national-level sources, and excludes development fixtures unless explicitly enabled. Test all four current categories and confirm the returned source title, URL, jurisdiction, review status, and text.

## Scope and non-goals

- **Now:** secure connection, reviewed source metadata, chunk storage, vector retrieval, ingestion, health diagnostics and tests.
- **Later:** SAP HANA PAL classifier (#9), knowledge graph queries (#11), evaluation dashboard (#18). These are not prerequisites for a functioning RAG pipeline.
- **Not HANA responsibilities:** Google sign-in, browser chat history, Google Maps lawyer discovery, and frontend session state. Keep those as separate services/components.

## Troubleshooting

- Connection refused/timeout: verify instance is running, host/port, network allowlist and VPN/firewall.
- Authentication failed: verify user/password and database user permissions.
- Missing tables: apply reviewed `sql/schema.sql` to the correct schema.
- Vector dimension error: check `EMBEDDING_MODEL` and ensure vectors have 384 dimensions; re-embed existing records after a model change.
- No sources returned: check `USE_HANA=true`, `CATEGORY_ID`, jurisdiction values, `REVIEW_STATUS='approved'`, and whether ingestion populated rows. Do not lower relevance thresholds to hide an empty or poor corpus.
- Incorrect retrieval: test representative questions, inspect chunk boundaries, improve official-source coverage, and measure retrieval precision before changing the model.
