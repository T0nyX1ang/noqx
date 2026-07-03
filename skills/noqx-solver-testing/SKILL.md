---
name: noqx-solver-testing
description: Project-specific workflow for validating noqx solver changes and measuring speedups. Use when the agent writes, edits, optimizes, reviews, or prepares to commit any solver under `solver/`, especially when comparing correctness, ground/solve time, puzzle examples, or acceleration ratios from existing solver examples.
---

# Noqx Solver Testing

## Purpose

Use this workflow after changing a solver or trying an optimization. The goal is to prove both:

- correctness: existing examples still solve and return the expected number of solutions;
- performance: speedups are measured against a clean baseline with comparable inputs.

Do not judge an optimization from one lucky run or from a semantically weakened rule.

## Existing Test Assets

- `tests/test_solver.py` runs the normal solver test suite against examples embedded in solver metadata.
- Solver modules store collected examples in their `examples` lists. Examples may use either `Penpa+` data (`data`) or `puzz.link` URLs (`url`).
- `run_single.py` loads one solver example or explicit `puzz.link` URL through Playwright and exports the `Penpa+` payload used by `prepare_puzzle`.

Use examples already collected in the solver metadata before inventing synthetic benchmark cases.

## Convert URL Examples

For a single `puzz.link` URL example, use `run_single.py` to load it through the front-end and capture the exported payload:

```powershell
uv run --with playwright run_single.py -n <puzzle-name> -e <example-number>
```

Please note that the count of the examples in the solver metadata is zero-based, so the first example is `-e 0`, the second is `-e 1`, and so on.

Useful variants:

```powershell
uv run --with playwright run_single.py -n <puzzle-name> -e <example-number> --browser-path <browser.exe>
uv run --with playwright run_single.py -n <puzzle-name> -l <puzz.link-url>
uv run --with playwright run_single.py -n <puzzle-name> -l <puzz.link-url> -p '{"key": true}'
```

The single-case import path is:

```text
`puzz.link` URL -> Playwright -> `imp(...)` in `penpa-edit/js/app.js` -> `exp()` -> `prepare_puzzle(...)`
```

If Playwright is missing, run with `uv run --with playwright ...`. The tool tries to use local Chrome or Edge when available, or accepts `--browser-path` when you need a specific executable.

## Correctness Workflow

1. Start from a clean baseline for the solver under test. If the worktree is dirty, identify which changes are yours and avoid mixing unrelated local files.
2. Run the target solver's collected examples first. For URL examples, use `run_single.py` to verify the Playwright import/export path and capture the exact payload passed to `prepare_puzzle`.
3. Confirm the solver returns the expected model count. The project test convention usually expects unique examples to return exactly one solution.
4. Run formatting/linting for touched files when applicable:

```powershell
uv run --with ruff ruff check solver\<puzzle-name>.py
```

5. Run the full solver suite before commit or push:

```powershell
python -m unittest tests.test_solver
```

6. If a slow or edge case is added, put it in the solver metadata examples when it should become permanent coverage. Use `test: False` only for examples that should be documented but skipped by the normal suite.

## Benchmark Workflow

Measure the same case against baseline and candidate code.

Grab the statistics file from logging. Record at least:

```text
ground time
solve time
total time
models found
atoms
rules
```

Separate grounding from solving. Previous solver work showed that a large-looking rule change can improve solving, and a tiny-looking rule change can do nothing if the real bottleneck is elsewhere.

The ground time can be evalulated between the following example log lines:

```text
2026-07-03 17:14:50.384 | DEBUG | [Solver] Parameter: PARALLEL_THREADS -> 1.
2026-07-03 17:14:50.461 | DEBUG | [Solver] ASP Program grounded.
2026-07-03 17:14:50.467 | DEBUG | [Solver] Battleship puzzle solved.
```

For noisy cases, repeat each candidate at least three times and compare ranges, not only the best run. A good result should be both semantically correct and stable enough to survive reruns.

When testing multiple ideas, change one variable at a time:

- baseline from committed `HEAD` or a known stable state;
- one candidate optimization;
- same link input;
- same solver config;
- same clingo settings such as timeout, model count, and threads.

## Interpreting Speedups

- Prefer wall-clock total time for user-facing claims, but keep ground and solve split in the notes.
- Be suspicious of speedups that come from weaker constraints. Fast but invalid models are unacceptable.
- If an optimization only improves program size or atom/rule counts but not solve time, describe it as a possible cleanup, not as the main performance fix.
- If program text grows substantially, check that the solve-time increase is large and repeatable enough to justify the grounding/text cost.
- A safe optimization can still be rejected if it is not a stable win on the collected examples.

## Handoff To Git Workflow

- Summarize benchmark data before commit or push, including baseline and candidate timings.
- Use `skills/noqx-git-workflow/SKILL.md` for staging, commit message, commit, and push rules.
- In prior work, `noqx/manager.py` and `run_single.py` were local support files; do not mix them into an unrelated solver commit unless explicitly requested.
