# Dataset and provenance notes

- `legal_documents.json`: synthetic development fixtures from the original archive; not legal authorities.
- `legal_dataset_candidates.json`: generated locally by `scripts/import_hf_legal_dataset.py`; candidate-only, keyword-filtered records from the KanoonGPT dataset. It is not created until the importer is run.
- `../../ml/data/scenarios_seed.json`: synthetic labeled examples for testing workflows only; not a representative or reviewed legal dataset.

External source: https://huggingface.co/datasets/KanoonGPT/indian-legal-documents
Dataset card states Apache-2.0 and describes fields such as document title, type, jurisdiction, issuing authority, issue date, description and text. Dataset rows may lack official source URLs; this importer records the dataset URL as provenance, not as the official instrument URL.

Before production use, verify each candidate against the official Gazette, India Code, Karnataka government source or court source as appropriate. Record source URL, effective date, amendment status, jurisdiction, reviewer and review date. Never use keyword-derived category labels as ground truth for model training without human review.
