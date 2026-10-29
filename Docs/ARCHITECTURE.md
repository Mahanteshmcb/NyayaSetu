# Architecture

Request flow: user description → input validation → whitespace/case normalization → baseline dispute classifier → confidence gate → HANA vector retrieval (when `USE_HANA=true`) or synthetic local fixtures → retrieval threshold → explanation with provenance or clarification question.

## Modules
- `backend/main.py`: FastAPI app, CORS, route registration.
- `backend/api/routes.py`: health and analysis endpoints.
- `backend/services/agent.py`: orchestration and safe clarification path.
- `ml/classifier.py`: transparent keyword baseline; not the planned HANA PAL model.
- `dl/embeddings/encoder.py`: sentence-transformers adapter and offline deterministic fallback.
- `rag/retriever.py`: local development-fixture retrieval.
- `rag/hana_retriever.py`: HANA `REAL_VECTOR` cosine-similarity retrieval with national-law inclusion and reviewed-source filtering.
- `scripts/check_hana_connection.py`: connection/schema diagnostic for HANA Cloud.
- `Docs/HANA_CLOUD_SETUP.md`: setup, ingestion, security and troubleshooting guide.
- `frontend/`: React/Vite interface.

The knowledge graph, HANA PAL classifier, streaming integration, notice PDF generator and evaluation dashboard remain future work, matching the open issue backlog.
