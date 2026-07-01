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

- When you add a feature in a solver helper function, consider whether it should be added to the `noqx` module for reuse by other solvers. Some laws are listed to help you decide:

  - If the feature is a general-purpose utility which can be used across different parts of solver, it should be in `noqx`.
  - If the feature is only in a solver-specific helper, it should be in the solver module.
  - If you cannot decide whether it is general-purpose or solver-specific, put it in the solver module first, and move it to `noqx` later if it is reused by other solvers.

## Formatting

- Let `ruff` and project tests be the source of truth for Python formatting and linting.
- Keep helper functions deterministic and easy to re-run in a fresh Python process during benchmark comparisons.
- Match the repo's existing style: short module docstrings, class docstrings, and method docstrings are common in `noqx` modules.
- Prefer explicit imports grouped by standard library, third-party, and local modules, and keep the order stable.
- Use type annotations on public functions and solver helpers when they improve readability or clarify the expected `Puzzle` data.
- Keep solver logic easy to follow with straightforward loops and branches rather than clever one-liners or deeply nested expressions.
- When building ASP output, prefer incremental `self.add_program_line(...)` calls so each generated rule stays readable and testable.
- Write code so the same helper can be executed repeatedly in a clean process without depending on hidden global state or cached results.
