---
name: noqx-push-meta
description: Meta workflow for preparing noqx changes for GitHub. Use when Codex is asked to push, commit and push, prepare a commit for sharing, or decide which project skills and checks apply before updating `origin`.
---

# Noqx Push Meta

## Purpose

Use this skill as the entry point before pushing changes to GitHub. It routes to the project-specific skills that contain the detailed rules and keeps the final push checklist in one place.

## Required Skill Routing

- Read `skills/noqx-git-workflow/SKILL.md` before staging, committing, writing commit messages, or pushing.
- Read `skills/noqx-solver-testing/SKILL.md` when changes touch `solver/`, solver examples, direct puzzle conversion helpers, or benchmark-related files.
- Read `skills/noqx-python-style/SKILL.md` when changes touch Python files.

## Push Checklist

1. Run `git status --short --branch` and identify all dirty files.
2. Inspect diffs for every file that might be staged.
3. Stage only files that belong to the requested change.
4. Run the checks required by the routed skills. For solver changes, this normally includes:

```powershell
uv run --with ruff ruff check solver\<solver-name>.py
python -m unittest tests.test_solver
```

5. Use a Conventional Commit message as described in `noqx-git-workflow`.
6. After committing, confirm `git status --short --branch` shows only intended state.
7. Push the current branch explicitly with `git push origin <branch>`.
8. Report the commit hash, pushed branch, checks run, and any unrelated dirty files that remain.

## Safety Rules

- Do not push unreviewed unrelated local changes.
- Do not mix local tooling or generated helper files into a solver commit unless the user explicitly asks for them.
- If hooks modify files during commit, inspect those changes before staging and committing again.
- Treat a successful push as complete only after `git status --short --branch` confirms the local branch is aligned with its upstream.
