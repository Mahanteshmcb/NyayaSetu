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