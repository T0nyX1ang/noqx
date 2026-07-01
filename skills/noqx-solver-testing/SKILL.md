---
name: noqx-solver-testing
description: Project-specific workflow for validating noqx solver changes and measuring speedups. Use when the agent writes, edits, optimizes, reviews, or prepares to commit any solver under `solver/`, especially when comparing correctness, ground/solve time, direct puzzle examples, or acceleration ratios from existing solver examples.
---

# Noqx Solver Testing

## Purpose

Use this workflow after changing a solver or trying an optimization. The goal is to prove both:

- correctness: existing examples still solve and return the expected number of solutions;
- performance: speedups are measured against a clean baseline with comparable inputs.

Do not judge an optimization from one lucky run or from a semantically weakened rule.

## Existing Test Assets

- `tests/test_solver.py` runs the normal solver test suite against examples embedded in solver metadata.
- Solver modules store collected examples in their `examples` lists. Examples may use either direct `Penpa+` data (`data`) or `puzz.link` URLs (`url`).
- `tests/puzzlink_to_direct.py` converts front-end supported `puzz.link` examples into stable `direct:` puzzle encodings.
- `noqx/puzzle/direct.py` and the direct branch in `noqx/manager.py` let local tools and benchmarks bypass the browser/front-end once a case is converted.

Use examples already collected in the solver metadata before inventing synthetic benchmark cases.

## Convert URL Examples

For `puzz.link` URL examples, convert them once into direct cases:

```powershell
uv run --with playwright python tests\puzzlink_to_direct.py --solver <solver-name> -o <cases.json>
```

Useful variants:

```powershell
uv run --with playwright python tests\puzzlink_to_direct.py --scan-examples -o all-direct-cases.json
uv run --with playwright python tests\puzzlink_to_direct.py --cases-json input-cases.json -o converted-cases.json
uv run --with playwright python tests\puzzlink_to_direct.py --puzzle-name <solver-name> --config key=value <puzz.link-url> -o case.json
```

The converter path is:

```text
`puzz.link` URL -> `Penpa+` import/export -> Python Puzzle -> direct:
```

If Playwright is missing, run with `uv run --with playwright ...`. The tool tries to use local Chrome or Edge when available.

## Correctness Workflow

1. Start from a clean baseline for the solver under test. If the worktree is dirty, identify which changes are yours and avoid mixing unrelated local files.
2. Run the target solver's collected examples first. For URL examples, prefer converted `direct:` cases so repeated benchmark runs do not depend on the browser.
3. Confirm the solver returns the expected model count. The project test convention usually expects unique examples to return exactly one solution.
4. Run formatting/linting for touched files when applicable:

```powershell
uv run --with ruff ruff check solver\<solver-name>.py
```

5. Run the full solver suite before commit or push:

```powershell
python -m unittest tests.test_solver
```

6. If a slow or edge case is added, put it in the solver metadata examples when it should become permanent coverage. Use `test: False` only for examples that should be documented but skipped by the normal suite.

## Benchmark Workflow

Measure the same direct case against baseline and candidate code.

Record at least:

```text
ground time
solve time
total time
models found
atoms
rules
program_len
```

Separate grounding from solving. Previous solver work showed that a large-looking rule change can improve solving, and a tiny-looking rule change can do nothing if the real bottleneck is elsewhere.

For noisy cases, repeat each candidate at least three times and compare ranges, not only the best run. A good result should be both semantically correct and stable enough to survive reruns.

When testing multiple ideas, change one variable at a time:

- baseline from committed `HEAD` or a known stable state;
- one candidate optimization;
- same direct input;
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
- In prior work, `noqx/manager.py`, `noqx/puzzle/direct.py`, and `tests/puzzlink_to_direct.py` were local direct-testing support files; do not mix them into an unrelated solver commit unless explicitly requested.
