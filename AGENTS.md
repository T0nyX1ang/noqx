# AGENTS.md

## Project Notes

- The default project guidance file is `AGENTS.md` at the repository root.
- For solver changes, read `./agents/skills/noqx-solver-testing/SKILL.md` before editing, optimizing, benchmarking, committing, or pushing files under `solver/`.
- The solver testing skill records the project-specific workflow for using existing examples, converting `puzz.link` URLs to `Penpa+` data, checking correctness, and reporting speed-ups.
- For Python code style and solver helper conventions, read `./agents/skills/noqx-python-style/SKILL.md` before editing Python files.
- Before committing or pushing to GitHub, read `./agents/skills/noqx-push-meta/SKILL.md` as the top-level checklist.
- For staging, committing, commit messages, and pushing to GitHub, read `./agents/skills/noqx-git-workflow/SKILL.md`.

## Project Structure

- `noqx/` contains the core Python package.
  - `noqx/clingo.py` provides the `Clingo` execution wrapper, solver configuration, statistics handling, and runtime solve entry point.
  - `noqx/manager.py` loads solver modules, exposes solver metadata, prepares puzzles, and stores solutions back into `Penpa+`-compatible structures.
  - `noqx/puzzle/` contains the puzzle model layer.
    - `noqx/puzzle/__init__.py` defines the shared puzzle types, directions, points, colors, and base puzzle abstractions.
    - `noqx/puzzle/penpa.py` handles `Penpa+` decoding and encoding for puzzle import/export.
  - `noqx/rule/` contains reusable rule helpers used by solver implementations.
    - `noqx/rule/common.py` contains common number, shading and counting rules.
    - `noqx/rule/neighbor.py` contains adjacency and neighborhood helpers.
    - `noqx/rule/reachable.py` contains reachability helpers.
    - `noqx/rule/route.py` contains loop and path-related helpers.
    - `noqx/rule/shape.py` contains rectangles, polyominoes, and geometry utilities.
    - `noqx/rule/variety.py` contains helpers which are not categorized currently.
    - `noqx/rule/helper.py` contains shared validation helpers and error-handling utilities.
- `solver/` contains the individual puzzle solver implementations.
- `tests/` contains test entry points and helper scripts, including the single-case runner used for Playwright-backed URL checks.
- `penpa-edit/` contains the bundled front-end assets used to import and export puzzle data.
- `docs/` contains the documentation source, while `site/`, `htmlcov/`, and `dist/` are generated outputs which are not required to scan/format.
- `build/` contains bundled third-party assets used by the app and front-end integration.
- `main.py` is the primary application entry point for the backend server.
- `main_deploy.py` is the primary application entry point for integrating the `Pyscript` feature.
- `run_single.py` at the repository root is the `Playwright`-backed single-case CLI runner.
