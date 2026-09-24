# Initial Issue Backlog

Create these as GitHub Issues, assign one owner, and link each pull request. The labels in parentheses are suggested labels.

1. **Freeze target state and source policy** (`scope`, `legal-review`): record the selected state, authoritative source classes, permitted-use rules, and decision date.
2. **Provision HANA development environment** (`infrastructure`): document connection method, schema namespace, non-secret variables, and a smoke test.
3. **Define anonymized scenario and label protocol** (`evaluation`): create 15-20 reviewed scenarios with category, state, required facts, and expected action.
4. **Create source provenance register** (`data`, `legal-review`): record exact source metadata, license, version, and review status.
5. **Design relational schema and migrations** (`data`, `infrastructure`): implement metadata tables and constraints for state, source, category, and review status.
6. **Implement normalization contract** (`feature`): preserve facts while supporting Hindi, Kannada, English, and code-mixed inputs.
7. **Build category classifier baseline** (`ml`): train/evaluate on the reviewed split and publish metrics with a confusion matrix.
8. **Define and test indicator model** (`ml`, `legal-review`): specify labels and ensure the signal is not presented as a legal conclusion.
9. **Implement legal chunking and embeddings** (`retrieval`): preserve section boundaries and record model/version metadata.
10. **Implement HANA vector retrieval** (`retrieval`, `infrastructure`): filter by state/category/date where applicable and return source metadata.
11. **Review retrieval relevance** (`evaluation`, `legal-review`): judge top-k results and retain query/result evidence.
12. **Create knowledge graph fixture** (`graph`): model category, law, authority, applicability, and remedy relationships.
13. **Implement finite agent workflow** (`agent`): enforce step/tool limits and separate user text, instructions, and evidence.
14. **Implement confidence and clarification rules** (`agent`, `evaluation`): test missing facts, low confidence, and state mismatch.
15. **Build grounded response contract** (`feature`, `legal-review`): include citations, uncertainty, disclaimer, and unsupported-claim refusal.
16. **Build editable notice templates** (`feature`, `legal-review`): validate placeholders and factual consistency.
17. **Add privacy and prompt-injection tests** (`security`): test redaction, untrusted input handling, and tool validation.
18. **Run baseline comparison** (`evaluation`): compare the same predefined cases through grounded and ungrounded pipelines.
19. **Prepare end-to-end demo and report** (`docs`): capture architecture, metrics, limitations, and contribution evidence.
20. **Rehearse viva and final checklist** (`docs`): verify every member can explain implementation choices and failures.

Start with issues 1-3 and complete issue 6-10 as a single vertical slice before parallel expansion.