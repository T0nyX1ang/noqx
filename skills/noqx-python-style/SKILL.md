---
name: noqx-python-style
description: Project-specific Python coding conventions for noqx. Use when Codex edits Python files, solver helper functions, benchmark utilities, or project guidance where local style, debuggability, cache behavior, or generated ASP code structure matters.
---

# Noqx Python Style

## Solver Helper Code

- Do not use `functools.lru_cache` in solver helper code. Prefer explicit local computation or project-visible constants so benchmark runs and solver hot edits do not depend on hidden process-local cache state.

## Formatting

- Let `ruff` and project tests be the source of truth for Python formatting and linting.
- Keep helper functions deterministic and easy to re-run in a fresh Python process during benchmark comparisons.
