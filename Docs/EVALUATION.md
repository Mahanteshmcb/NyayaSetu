# Evaluation Plan

## Current baseline
Run `pytest -q`. Tests cover health, request validation, four keyword-classifier paths, local retrieval and fixture-provenance disclosure.

## Metrics to add
- Classification: macro-F1, per-category precision/recall, confusion matrix, unknown/abstention rate.
- Retrieval: Recall@k, MRR, source/jurisdiction filter accuracy, no-result rate.
- Grounding: claim-to-source support reviewed by domain experts, citation completeness, unsupported-claim rate.
- Clarification: appropriate abstention rate, missed-clarification rate, unnecessary-clarification rate.
- Robustness: English, Kannada, Hindi and code-mixed scenarios; spelling variants; adversarial or underspecified inputs.
- UX: completion rate, readability and user understanding.

Keep a held-out reviewed dataset. Never report development-fixture tests as evidence of legal accuracy.
