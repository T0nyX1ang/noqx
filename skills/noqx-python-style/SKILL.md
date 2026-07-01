---
name: noqx-python-style
description: Project-specific Python coding conventions for noqx. Use when the agent edits Python files, solver helper functions, benchmark utilities, or project guidance where local style, debuggability, cache behavior, or generated ASP code structure matters.
---

# Noqx Python Style

## Solver Helper Code

- Use `micropython` compatible syntaxes except for typing checks, some unsupported syntaxes as below:

  - `async` / `await` which needs `asyncio` support
  - `enum`, `typing.NamedTuple` and `typing.TypedDict` which needs metaclasses support
  - `dataclasses`
  - `functools.lru_cache`
  - nested `f-strings` which computes strings at runtime

## Formatting

- Let `ruff` and project tests be the source of truth for Python formatting and linting.
- Keep helper functions deterministic and easy to re-run in a fresh Python process during benchmark comparisons.
