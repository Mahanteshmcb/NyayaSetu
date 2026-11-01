# Evaluation Plan

<<<<<<< HEAD
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
=======
## Evidence-first rule

No metric may be invented for a report or demo. Every number must point to a versioned test-set definition, ground-truth review, code or query version, and retained result artifact. Domain reviewers should record disagreement instead of forcing a label.

## Evaluation layers

| Layer | Metric or check | Evidence |
| --- | --- | --- |
| Category classifier | Accuracy, precision, recall, F1, confusion matrix | Test-set predictions and labels |
| Indicator model | Metric appropriate to its reviewed formulation | Predictions, labels, calibration notes |
| Retrieval | Top-k relevance, source hit rate, state/category applicability | Query IDs, retrieved IDs, reviewer decisions |
| Grounding | Unsupported-claim rate, citation coverage | Output audit with claim-to-source links |
| Agent | Correct answer-versus-clarify decision, tool-call limit | Decision log and traces |
| Template | Required fields, factual consistency, editable placeholders | Domain review checklist |
| End to end | Scenario success and failure classification | Curated scenario scorecard |

## Dataset protocol

Create a small reviewed scenario set first, including positive, ambiguous, cross-state, missing-fact, code-mixed, and adversarial inputs. Split development and held-out evaluation data before tuning. Record category definitions, annotator guidance, disagreements, anonymization method, provenance, and permitted use.

## Controlled baseline comparison

Run the same predefined questions through an ungrounded LLM baseline and the HANA-grounded pipeline. Do not cherry-pick examples. Compare source support, unsupported claims, category correctness, clarification behavior, and useful output completion. Keep prompts, model versions, retrieval settings, and test-set IDs with the results.

## Acceptance gates

- A vertical slice has reviewed source coverage for its chosen state.
- The system refuses or clarifies when required evidence is absent.
- Every displayed legal claim has a visible source reference or is clearly labeled as a limitation.
- Retrieval is judged for legal relevance, not only vector similarity.
- The final report separates measured results from hypotheses and limitations.
>>>>>>> origin/main
