<<<<<<< HEAD
# 20-Day Plan (working baseline)

1. Confirm scope, categories and safety disclaimer.
2. Define API schema and health endpoint.
3. Implement validation and normalization.
4. Establish baseline classifier.
5. Create reviewed scenario format.
6. Configure HANA Cloud and credentials.
7. Define relational schema and migrations.
8. Prepare source provenance metadata.
9. Build embedding pipeline.
10. Ingest reviewed documents.
11. Implement HANA vector retrieval.
12. Add metadata and jurisdiction filters.
13. Implement clarification thresholds.
14. Ground explanation and source display.
15. Add editable notice templates.
16. Build frontend interaction.
17. Connect frontend and backend.
18. Create multilingual scenario dataset.
19. Run evaluation and document failure modes.
20. Demo, review and prioritize next issues.

Progress should be marked only after the corresponding code, tests, and evidence are checked.
=======
# 20-Day Execution Plan

The team may extend this to 24 days only by adding review or validation time, not by silently expanding scope. Use the owner placeholders until the team agrees on names.

| Days | Deliverable | Owner |
| --- | --- | --- |
| 1-3 | Select one state; provision HANA/AI access; agree schema, source policy, and 15-20 reviewed scenarios | Platform / Legal / Evaluation |
| 4-7 | Load approved metadata; create the first category fixture; implement and measure the classifier baseline | Platform / ML |
| 8-12 | Select embedding model; implement chunking and vector retrieval; review top-k results | Platform / Legal |
| 13-16 | Add graph relationships, finite agent workflow, confidence rules, clarification path, and letter template | Platform / Evaluation |
| 17-19 | Build ungrounded baseline; run controlled side-by-side evaluation; classify failures | All |
| 20 | Freeze report, limitations, demo script, contribution record, and viva rehearsal | All |

## Daily operating rhythm

Each day ends with a short update: completed issue, evidence produced, blocker, next issue, and any changed assumption. Do not count an imported library as an implemented AI component; show its inputs, outputs, and measured behavior.

## Scope guardrails

If source review, state applicability, or evaluation falls behind, reduce categories or interface breadth. Do not add states, agents, or model complexity to compensate. One complete defensible vertical slice is the milestone that unlocks expansion.
>>>>>>> origin/main
