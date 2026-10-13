# Architecture

## System boundary

```text
User description
  -> input validation and language/code-mix normalization
  -> structured indicators and category classifier
  -> embedding generation
  -> HANA metadata filters + vector retrieval + graph lookup
  -> confidence and grounding policy
       -> clarify when required facts or evidence are missing
       -> answer with sources, uncertainty, and editable template
```

## Component responsibilities

| Component | Responsibility | Required evidence |
| --- | --- | --- |
| Input layer | Validate size, remove accidental secrets from telemetry, preserve user language | Validation tests |
| Normalizer | Produce a downstream representation without silently changing facts | Before/after reviewed examples |
| ML classifier | Predict one of the defined dispute categories | Held-out metrics and confusion matrix |
| Case-indicator model | Produce an experimental structured signal only | Label definition, calibration, limitations |
| Embedding layer | Represent input and approved chunks for semantic search | Model/version and retrieval tests |
| HANA relational layer | Store source, state, authority, date, category, and case metadata | Schema migration and fixture checks |
| Vector retrieval | Return top-k candidate chunks with metadata and scores | Query IDs, results, reviewer decisions |
| Knowledge graph | Resolve category, authority, law, remedy, and applicability relationships | Graph fixture and relationship tests |
| Agent workflow | Orchestrate a finite sequence with tool limits and clarify rules | Execution trace and answer-vs-clarify tests |
| Response layer | Present plain language, citations, uncertainty, and template placeholders | Output contract tests |

## Data contract

All source-backed records need a stable `source_id`, title, publisher or authority, URL or archive reference, jurisdiction, effective date or retrieval date, source type, license or terms, and review status. Every embedded chunk additionally needs a stable chunk ID, source ID, section boundary, content hash, embedding model version, and ingestion timestamp.

User content is untrusted input. It must remain separate from system instructions and retrieved evidence. Tool parameters are validated, retrieval is filtered by state/category/date where applicable, and the agent has a finite step and tool-call limit.

## First vertical slice

Implement one category end to end before building all four: input fixture, normalization, classifier output, one approved source set, retrieval, graph relationship, clarify path, grounded response, template, and evaluation evidence. The team should choose the slice based on source availability and reviewability, not novelty.

## Failure behavior

- Low classifier confidence: show uncertainty and ask for a category-relevant fact.
- No relevant source: do not improvise; explain that the system cannot support a reliable answer.
- State mismatch: ask for the state or report that the available source may not apply.
- Missing mandatory fact: ask one focused clarifying question.
- Retrieval disagreement: expose the conflict and route to human review.
- Prompt injection or unsafe tool input: treat it as user text, reject the instruction, and record only a redacted event.