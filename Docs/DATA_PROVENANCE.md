<<<<<<< HEAD
# Data Provenance and Safety

The five records under `rag/data/legal_documents.json` are synthetic development fixtures identified by `DEV-*`. They are useful only to exercise API, filtering and retrieval code. They are not official laws, judgments, legal opinions, or validated case summaries. Do not cite them to end users as authorities.

Before adding real material, record source URL, source type, jurisdiction, publication/update date, licence/terms, retrieval date, reviewer, review status and the exact text range. Have a domain reviewer validate legal meaning. Keep a clear distinction between official primary sources, secondary commentary and anonymized case summaries. Never upload confidential or identifying user information into test fixtures.
=======
# Data Provenance Register

Every legal source, case summary, label set, and model input used in development must have a record. Complete this table before ingestion; do not replace unknown values with guesses.

| Field | Required value |
| --- | --- |
| `source_id` | Stable internal identifier |
| Source title and type | Act, rule, judgment, government page, reviewed summary, or other |
| Publisher or authority | Named issuing body |
| URL or archive reference | Reproducible location |
| Jurisdiction | State, national, or other applicability |
| Publication/effective/retrieval dates | Use the dates that are actually known |
| License or terms | Permission and restrictions |
| Content hash/version | Identify the exact captured material |
| Review status | Unreviewed, reviewed, rejected, or superseded |
| Reviewer and review date | Accountable human review |
| Allowed use | Training, retrieval, evaluation, or citation only |
| Notes | Conflicts, amendments, exclusions, or limitations |

## Collection rules

Prefer authoritative and legally permitted sources. Preserve section boundaries and amendments. Do not scrape or redistribute content when terms do not permit it. Case material must be anonymized, lawfully obtained, and labeled as a summary rather than an authority unless the original authority is available and approved.

## Review checklist

- Is the source authentic and attributable?
- Does it apply to the selected state and relevant date?
- Are the terms compatible with the intended use?
- Are citations and section boundaries preserved?
- Has a reviewer checked that the plain-language interpretation does not overstate the source?
- Can the team reproduce which exact source version produced an output?
>>>>>>> origin/main
