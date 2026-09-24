# Team Workflow and GitHub Management

This document explains how people join the project, how work is assigned, and how code reaches `main`. The repository owner must configure the GitHub settings described in the final section.

## 1. People and permissions

The repository owner should invite contributors from **Settings -> Collaborators -> Add people**. Give the least permission that allows the person's work:

| Role | GitHub permission | Project responsibility |
| --- | --- | --- |
| Maintainer / project owner | Maintain or Admin | Scope, access, branch rules, final merge, release decisions |
| Platform and ML contributor | Write | HANA schema, ingestion, classifier, embeddings, tests |
| Legal-content and evaluation contributor | Write | Source review, provenance, scenarios, retrieval and grounding review |
| Application and integration contributor | Write | API/UI, agent workflow, templates, end-to-end integration |
| Reviewer | Write or Triage | Reviews assigned issues and pull requests; does not merge without approval |

For a four-person team, one person may hold two responsibility areas, but every issue still has exactly one accountable owner and one reviewer. Do not share GitHub accounts or tokens.

## 2. How work is created and assigned

1. The project owner creates a GitHub Project with these columns or statuses: `Backlog`, `Todo`, `In Progress`, `Review`, `Testing`, `Done`.
2. The team discusses the backlog and moves only ready tasks into `Todo`.
3. A contributor takes one task, or the maintainer assigns it using the issue's **Assignees** control.
4. The assignee adds the issue number to the branch name and pull request.
5. The assignee moves the Project item to `In Progress` when coding starts.
6. The assignee moves it to `Review` when a pull request is open.
7. After review approval, CI success, and manual testing, the maintainer moves it to `Done` after merge.

An issue is ready only when it has an objective, inputs, outputs, acceptance criteria, failure behavior, owner, reviewer, and evidence to retain. Use the feature or bug issue forms instead of vague tasks such as "build AI".

## 3. Ownership model

The assignee is responsible for progress and communication, not for working alone. The reviewer checks correctness and evidence. The maintainer protects scope and decides when work is ready to merge.

Recommended initial ownership:

| Area | Primary owner | Backup reviewer |
| --- | --- | --- |
| HANA schema and data ingestion | Platform/ML | Application/integration |
| Legal sources and provenance | Legal/evaluation | Project owner |
| Classifier and evaluation | Platform/ML | Legal/evaluation |
| Agent and API/UI integration | Application/integration | Platform/ML |

Avoid having two people edit the same schema, central route, orchestration file, or evaluation dataset at the same time. Coordinate before taking a high-conflict issue.

## 4. Branch rules

Use temporary branches based on the latest `main`:

```powershell
git switch main
git pull --ff-only origin main
git switch -c feature/12-wage-classifier
```

Recommended names:

- `feature/12-wage-classifier`
- `fix/18-state-filter`
- `docs/3-source-policy`
- `test/11-retrieval-evaluation`

One branch should represent one meaningful issue. Do not create a branch for every tiny edit, and do not reuse a completed branch for a new task.

## 5. Pull request lifecycle

The contributor runs focused tests and checks the diff before pushing:

```powershell
git status
git diff
git add <specific-files>
git diff --staged
git commit -m "feat: add wage category classifier"
git push -u origin feature/12-wage-classifier
```

The pull request must:

- reference the issue, for example `Closes #12`;
- explain the implementation and any changed assumptions;
- list commands and test results;
- include metrics, scenario IDs, source review, or traces when relevant;
- identify privacy, legal-grounding, and failure-path considerations;
- name a reviewer who did not author the change.

Reviewers should ask:

1. Does the change meet the acceptance criteria?
2. Does it test failure behavior as well as the normal path?
3. Are legal claims sourced and state-applicable?
4. Could it expose personal data, secrets, or unsafe tool behavior?
5. Can the author explain the important design choices and limitations?

The author resolves comments and reruns checks. The maintainer merges only after required approval, passing Actions checks, and a successful manual test where applicable. Prefer **Squash and merge** for a small feature so `main` retains a readable history. Delete the remote feature branch after merging.

## 6. Updating a branch safely

Before opening or updating a pull request:

```powershell
git fetch origin
git switch main
git pull --ff-only origin main
git switch feature/12-wage-classifier
git merge main
# resolve conflicts deliberately if Git reports any
# run tests again
git push
```

Do not use `git reset --hard`, `git checkout --`, or a blind "ours/theirs" conflict choice to discard work. Read both versions, resolve the intent, test, and commit the resolution.

## 7. When an issue is complete

The owner may request review only when:

- the acceptance criteria are checked;
- normal and failure cases were tested;
- relevant evidence is attached or linked;
- source provenance is complete;
- documentation is updated;
- the working tree and pull request contain only intended files.

The maintainer closes the issue after merge. If the work is incomplete, keep the issue open or create a follow-up issue; do not mark it Done because the code merely exists.

## 8. Configure GitHub protection once

The repository owner should open **Settings -> Branches -> Add branch protection rule** for `main` and enable:

- Require a pull request before merging.
- Require at least one approval.
- Dismiss stale approvals when new commits are pushed, if practical.
- Require status checks to pass before merging, selecting the documentation workflow and later test/lint workflows.
- Require branches to be up to date before merging, if the team can keep branches current.
- Block force pushes and branch deletion.
- Do not allow bypassing these rules for ordinary contributors.

Also check **Settings -> Actions -> General** and allow the repository's required workflows. Review **Settings -> Collaborators** quarterly and remove people who no longer contribute.

GitHub settings are permission-controlled and cannot be safely reproduced by a normal repository file. Record the chosen settings in the project owner's private notes after configuring them.

## 9. Weekly team meeting

Keep it short. Each person answers:

```text
Completed issue and evidence:
Current issue and next deliverable:
Blocker or decision needed:
Files or ownership that may conflict:
```

The maintainer updates the Project board and records scope decisions. If a task is blocked for more than one working session, split it, reassign it, or reduce scope rather than hiding the blocker.
