---
name: noqx-git-workflow
description: Project-specific git workflow for the noqx repository. Use when Codex stages files, writes commit messages, creates commits, runs pre-commit hooks, pushes to GitHub, or explains commit/push rules for noqx.
---

# Noqx Git Workflow

## Project Rules

- The repository uses pre-commit hooks from `.pre-commit-config.yaml`.
- Install hooks with:

```powershell
uv pre-commit install
```

- Pre-commit runs `ruff`, `ruff-format`, and `prettier`.
- Commit message validation runs `conventional-pre-commit` as a `commit-msg` hook.
- Current normal development branch observed in this workspace is `dev`; confirm the current branch before pushing.
- Remote `origin` points to GitHub. Confirm with `git remote -v` if the push target matters.

## Before Staging

- Run `git status --short` before staging.
- Inspect `git diff` for tracked changes and identify unrelated user work.
- Stage only files that belong to the requested change.
- Do not accidentally stage local benchmark helpers, generated caches, or unrelated direct-testing files.
- If unrelated dirty files exist, leave them alone and mention them in the final status.

## Commit Message Format

Write commit messages in Conventional Commits style:

```text
type(scope): short imperative summary
type: short imperative summary
```

The scope is optional. Use lowercase types. For solver-only changes, a puzzle scope is usually helpful.

Good examples:

```text
perf(nikoji): optimize small shape matching
fix(statuepark): preserve white connectivity
test(nikoji): add direct benchmark case
docs: document solver benchmark workflow
chore: update pre-commit hooks
```

Common types for this repository:

- `perf`: solver speedups or performance-oriented rewrites.
- `fix`: correctness fixes or bug fixes.
- `test`: tests, benchmark cases, or coverage-only changes.
- `docs`: documentation, comments, or project guidance.
- `refactor`: behavior-preserving code restructuring.
- `chore`: maintenance that is not solver behavior.

Avoid bare summaries such as:

```text
optimize nikoji shape matching
```

The `conventional-pre-commit` hook rejects that because it lacks a Conventional Commit type.

## Commit And Push

Use non-interactive commands.

Recommended sequence:

```powershell
git status --short
git diff -- <intended-files>
git add -- <intended-files>
git diff --cached --stat
git diff --cached
git commit -m "type(scope): short imperative summary"
git status --short
git push origin <branch>
```

If hooks modify files during commit, inspect the changes, rerun relevant tests if needed, stage the hook edits, and commit again.

## Reporting

After a successful commit, report:

- commit hash;
- commit message;
- pushed branch and remote when pushed;
- tests or checks that passed;
- any unrelated dirty files still present.

