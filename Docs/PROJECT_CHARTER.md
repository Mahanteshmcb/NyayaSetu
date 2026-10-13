# Project Charter

## Purpose

NyayaSetu helps a person turn an informal dispute description into cautious, source-grounded legal information and an editable document template. It targets people who may write in Hindi, Kannada, English, or a code-mixed combination and who need an understandable starting point for a small dispute.

## MVP scope

- Categories: rent or deposit, unpaid wages, termination, and workplace harassment.
- Geography: one Indian state, selected and recorded before legal ingestion.
- Inputs: a natural-language dispute description plus explicit state and relevant facts when available.
- Outputs: category, structured indicators, retrieved source material, related anonymized case summaries where permitted, uncertainty, clarifying questions, plain-language explanation, and an editable notice or letter template.
- Data platform target: SAP HANA Cloud, including relational metadata, HANA Vector Engine, and graph relationships where available in the selected environment.

## Non-goals

- Legal representation, legal advice, legal verdicts, or guaranteed outcomes.
- Automatic filing, contacting an opposing party, or taking an external legal action.
- Multi-state coverage before one-state coverage has reviewed sources and evaluation evidence.
- Claiming an ML, DL, or agent component exists merely because a library or API is imported.

## Product safety boundary

Every legal claim must be traceable to a reviewed source with jurisdiction and date metadata. The interface must state that the result is general legal information, show uncertainty, and recommend qualified legal help for urgent, high-risk, or complex matters. Personal information must be minimized, anonymized in test data, and excluded from ordinary logs.

## Decisions to freeze before implementation

| Decision | Owner | Due | Evidence |
| --- | --- | --- | --- |
| First target state | Team | Day 1 | Decision record and source inventory |
| Legal source policy and allowed licenses | Legal-content owner | Day 3 | Provenance register |
| HANA instance and access method | Platform owner | Day 3 | Setup record with secrets excluded |
| Supported languages and normalization policy | Evaluation owner | Day 5 | Reviewed test cases |
| Required facts and clarify thresholds | Full team | Day 12 | Decision table and tests |

## Definition of done

See [the evaluation plan](EVALUATION.md), [the developer guide](DEVELOPER_GUIDE.md), and [the issue backlog](ISSUE_BACKLOG.md). In short, a feature is complete only when its acceptance criteria, failure behavior, test evidence, provenance, and pull-request review are recorded.