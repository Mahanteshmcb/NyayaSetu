# Developer Guide

## Prerequisites

Install Git and the runtime chosen in the first implementation issue. Obtain HANA access through the team-approved account. Never put credentials in the repository, issue text, notebooks, logs, or screenshots. Record setup assumptions in a local ignored environment file and provide only variable names in `.env.example`.

## First checkout

```powershell
git clone https://github.com/Mahanteshmcb/NyayaSetu.git
cd NyayaSetu
git switch main
git pull --ff-only origin main
```

Read the charter and architecture before implementing a component. Confirm the target state and source policy in the issue you are taking.

## Branch and pull-request workflow

```powershell
git switch main
git pull --ff-only origin main
git switch -c feature/<meaningful-task>
# implement one coherent task
git status
git diff
# run the relevant tests
git add <specific-files>
git diff --staged
git commit -m "feat: describe the completed task"
git push -u origin feature/<meaningful-task>
```

Open a pull request with the acceptance criteria and test evidence. A teammate reviews the code and evidence before merge. Update `main` and start a fresh temporary branch for the next task. Never directly push to `main`.

## Engineering loop

1. Start from an issue with objective, owner, inputs, outputs, acceptance criteria, and failure behavior.
2. Make the smallest testable change.
3. Read the relevant files and dependency behavior; do not accept generated code blindly.
4. Run a focused test first, then the wider suite when it exists.
5. Inspect `git diff` and `git diff --staged` before committing.
6. Retain evidence: metrics, retrieved IDs, source review, traces, or scenario results as appropriate.
7. Update documentation when setup, data behavior, or public contracts change.

## AI-assisted development rule

AI tools may help explain an unfamiliar API, suggest boilerplate, find bugs, or propose tests. They must not replace design decisions, source review, legal review, or test execution. The author must be able to explain every important changed line, rejected alternative, dependency, limitation, and evidence during the viva. Do not generate the full application in one prompt.

## Testing expectations

Test both successful and failure paths. Include Hindi, Kannada, English, and code-mixed fixtures where supported. Use anonymized or synthetic test cases; do not paste real personal disputes into tracked files. A model metric without a held-out dataset and provenance is not evidence.

## Commit hygiene

Use focused messages such as `feat: add wage category fixture`, `test: measure retrieval hit rate`, or `docs: record source policy`. Do not commit `.env`, tokens, raw legal data, local databases, generated model weights, or unreviewed copied material.