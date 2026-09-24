# NyayaSetu

NyayaSetu is a source-grounded legal-information explainer for common disputes. A user can describe a rent/deposit, wage, termination, or workplace-harassment situation in Hindi, Kannada, English, or a code-mixed form. The planned system classifies the situation, retrieves reviewed legal sources and related anonymized case summaries, explains the result in plain language, and drafts an editable template notice.

This is a capstone prototype for legal information and decision support. It is not a lawyer, a legal opinion, a guarantee of an outcome, or a substitute for professional advice. The product must show sources, uncertainty, state applicability, and missing facts.

## Project status

The repository is in the foundation phase. The team should freeze one Indian state before ingesting legal material and complete one defensible vertical slice before expanding coverage. The target execution window is 20 days, with a fourth contributor welcome if ownership remains explicit.

## Start here

- [Project charter](Docs/PROJECT_CHARTER.md): scope, non-goals, assumptions, and decision log.
- [Architecture](Docs/ARCHITECTURE.md): the ML, embedding, retrieval, graph, and agent boundaries.
- [Developer guide](Docs/DEVELOPER_GUIDE.md): environment setup, branch workflow, testing, and AI-assisted development rules.
- [Evaluation plan](Docs/EVALUATION.md): datasets, metrics, evidence, and the grounded-versus-ungrounded comparison.
- [Data provenance register](Docs/DATA_PROVENANCE.md): required evidence for every legal or case source.
- [20-day plan](Docs/20_DAY_PLAN.md): daily milestones and ownership placeholders.
- [Issue backlog](Docs/ISSUE_BACKLOG.md): the first implementation-sized work items.
- [Original project specification](Docs/Explainer_Project_Documentation_v1.docx): supplied working blueprint.

## Team rules

1. `main` is stable; do not push directly to it.
2. One meaningful task uses one temporary feature branch and one pull request.
3. Every issue has an owner, acceptance criteria, and evidence to retain.
4. AI assistance is allowed for explanation, boilerplate, debugging, and test ideas. Every generated change must be read, reviewed, tested, and explainable by its author.
5. Never fabricate legal sources, cases, datasets, metrics, or citations.
6. Do not log raw personal dispute descriptions or commit credentials, local databases, model weights, or environment files.

## Local setup

This foundation commit contains documentation and repository governance only; application dependencies will be added with the first implementation issue. To work with the repository:

```powershell
git clone https://github.com/Mahanteshmcb/NyayaSetu.git
cd NyayaSetu
git switch main
```

Before coding, read the developer guide and create a feature branch from an updated `main`.

## License

See [LICENSE](LICENSE). Legal content brought into the project must also be tracked with its source, version/date, jurisdiction, license or terms, and permitted use.
