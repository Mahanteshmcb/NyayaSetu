# Known Limitations in This Archive

This ZIP was reconstructed from the implementation details shared in ChatGPT history; it is not a byte-for-byte export of the user's local folder or GitHub repository. The user's live HANA tenant, credentials, exact schema, and any local unshared edits are not bundled.

- Keyword classifier is a baseline; not SAP HANA PAL.
- HANA schema/SQL types must be verified against the actual tenant.
- HANA vector dimensions must match the configured embedding model. The schema's 384 dimensions match the default MiniLM model but not the 384-dimensional offline fallback only by intent, not semantic quality.
- Offline fallback vectors are feature hashes and are not production embeddings.
- Included content is synthetic and not legal advice.
- Full knowledge graph, evaluation dashboard, SSE, and PDF template generation are not implemented.
