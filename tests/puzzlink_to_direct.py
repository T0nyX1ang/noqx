"""Convert front-end supported puzz.link examples into noqx direct encodings.

This tool intentionally reuses the browser-side import path:

    puzz.link URL -> penpa-edit import_url/imp -> Penpa payload -> Python Puzzle -> direct:

Run it with Playwright available, for example:

    uv run --with playwright python tests/puzzlink_to_direct.py --solver battleship -o cases.json
"""

import argparse
import json
import pkgutil
import sys
from contextlib import suppress
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from noqx.manager import list_solver_metadata, load_solver, prepare_puzzle  # noqa: E402
from noqx.puzzle.direct import from_puzzle  # noqa: E402


def parse_config(raw: str) -> Dict[str, Any]:
    """Parse JSON or simple key=value CLI config syntax."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        config = {}
        for item in raw.split(","):
            if not item:
                continue
            key, sep, value = item.partition("=")
            if not sep:
                raise
            try:
                config[key] = json.loads(value)
            except json.JSONDecodeError:
                config[key] = value
        return config


def load_solvers() -> None:
    """Load all solver modules once for metadata and direct conversion."""
    for module_info in pkgutil.iter_modules([str(ROOT_DIR / "solver")]):
        with suppress(ValueError):
            load_solver("solver", module_info.name)


def scan_example_urls(solvers: Optional[List[str]] = None):
    """Yield URL examples from solver metadata."""
    requested = set(solvers or [])
    for solver_name, metadata in sorted(list_solver_metadata().items()):
        if requested and solver_name not in requested:
            continue
        for index, example in enumerate(metadata.get("examples", [])):
            if "url" in example:
                yield {
                    "solver": solver_name,
                    "index": index,
                    "url": example["url"],
                    "config": example.get("config", {}),
                }


def load_cases_json(path: str) -> List[Dict[str, Any]]:
    """Read cases from a local JSON cache or previous converter output."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("converted", data.get("cases", []))

    cases = []
    for index, item in enumerate(data):
        solver = item.get("solver", item.get("name"))
        if not solver:
            raise ValueError(f"Missing solver/name in case {index}.")
        cases.append(
            {
                "solver": solver,
                "index": item.get("index", index),
                "label": item.get("label"),
                "url": item["url"],
                "config": item.get("config", {}),
            }
        )
    return cases


def find_browser_executable(explicit_path: Optional[str]) -> Optional[str]:
    """Find a locally installed Chromium-family browser."""
    candidates = []
    if explicit_path:
        candidates.append(Path(explicit_path))
    candidates.extend(
        [
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
            Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        ]
    )

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return None


def playwright_module():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "Playwright is required for front-end URL conversion. "
            "Run with: uv run --with playwright python tests/puzzlink_to_direct.py ..."
        ) from exc
    return sync_playwright


def frontend_case_to_penpa(page, case: Dict[str, Any]) -> Dict[str, Any]:
    """Use the loaded front-end to import one URL and export a Penpa payload."""
    return page.evaluate(
        """
({ url, solver, config }) => {
  imp(url, true);

  const typeSelect = document.getElementById("type");
  if (solver && typeof solver_metadata !== "undefined" && solver_metadata[solver] && typeSelect.value !== solver) {
    typeSelect.value = solver;
    typeSelect.dispatchEvent(new Event("change"));
  }

  const puzzleType = typeSelect.value;
  if (!puzzleType) {
    throw new Error("Front-end did not determine a puzzle type.");
  }

  const setParam = (key, value) => {
    const input = document.getElementById(`param_${key}`);
    if (!input) return;

    if (key === "shapeset") {
      if (Array.isArray(value)) input.value = value;
      else if (typeof presetData !== "undefined" && presetData[value]) input.value = presetData[value].config;
      else if (value === "" || value === undefined || value === null) input.value = [];
      else input.value = value;
    } else if (input.type === "checkbox") {
      input.checked = Boolean(value);
    } else {
      input.value = value;
    }
  };

  for (const [key, value] of Object.entries(config || {})) {
    setParam(key, value);
  }

  const params = {};
  const metadata = solver_metadata[puzzleType] || {};
  for (const key of Object.keys(metadata.parameters || {})) {
    const input = document.getElementById(`param_${key}`);
    if (!input) continue;
    params[key] = input.type === "checkbox" ? input.checked : input.value;
  }

  return {
    solver: puzzleType,
    data: exp(true),
    config: Object.keys(config || {}).length ? config : params,
    frontend_config: params,
  };
}
""",
        {"url": case["url"], "solver": case.get("solver"), "config": case.get("config", {})},
    )


def convert_case_with_frontend(page, case: Dict[str, Any]) -> Dict[str, Any]:
    frontend = frontend_case_to_penpa(page, case)
    solver = frontend["solver"]
    config = frontend["config"]
    penpa_payload = frontend["data"]

    puzzle = prepare_puzzle(solver, penpa_payload, config)
    direct = from_puzzle(puzzle)
    return {
        "solver": solver,
        "index": case.get("index"),
        "label": case.get("label"),
        "url": case["url"],
        "config": config,
        "direct": direct.content,
        "rows": puzzle.row,
        "cols": puzzle.col,
        "counts": {
            "surface": len(puzzle.surface),
            "text": len(puzzle.text),
            "symbol": len(puzzle.symbol),
            "edge": len(puzzle.edge),
            "line": len(puzzle.line),
        },
    }


def convert_cases(cases: List[Dict[str, Any]], frontend_path: str, browser_executable: Optional[str], headless: bool):
    sync_playwright = playwright_module()
    frontend_uri = Path(frontend_path).resolve().as_uri()
    converted = []
    unsupported = []

    with sync_playwright() as playwright:
        launch_kwargs = {"headless": headless}
        if browser_executable:
            launch_kwargs["executable_path"] = browser_executable

        browser = playwright.chromium.launch(**launch_kwargs)
        page = browser.new_page()
        page.goto(frontend_uri, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_function(
            "typeof imp === 'function' && typeof exp === 'function' && typeof import_url === 'function' && typeof solver_metadata !== 'undefined'",
            timeout=60000,
        )

        for case in cases:
            try:
                converted.append(convert_case_with_frontend(page, case))
            except Exception as exc:
                unsupported.append({**case, "error": str(exc)})
                try:
                    page.reload(wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_function(
                        "typeof imp === 'function' && typeof exp === 'function' && typeof import_url === 'function' && typeof solver_metadata !== 'undefined'",
                        timeout=60000,
                    )
                except Exception:
                    pass

        browser.close()

    return converted, unsupported


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="*", help="puzz.link URLs to convert. Defaults to --scan-examples when omitted.")
    parser.add_argument("--puzzle-name", help="Puzzle name for positional URLs. Usually inferred by the front-end.")
    parser.add_argument("--config", default="{}", help="JSON config or key=value pairs for positional URLs.")
    parser.add_argument("--cases-json", help="Read cases from a JSON file with solver/name, url, and optional config.")
    parser.add_argument("--scan-examples", action="store_true", help="Scan solver metadata for examples with URL fields.")
    parser.add_argument("--solver", action="append", help="Limit --scan-examples to this solver. Can be repeated.")
    parser.add_argument("--frontend", default=str(ROOT_DIR / "penpa-edit" / "index.html"), help="Path to penpa-edit/index.html.")
    parser.add_argument("--browser-executable", help="Path to Chrome/Edge. Defaults to a local system browser when found.")
    parser.add_argument("--headed", action="store_true", help="Show the browser while converting.")
    parser.add_argument("--output", "-o", help="Output JSON path. Defaults to stdout.")
    args = parser.parse_args(argv)

    load_solvers()

    if args.cases_json:
        cases = load_cases_json(args.cases_json)
    elif args.urls:
        config = parse_config(args.config)
        cases = [{"solver": args.puzzle_name, "index": None, "url": url, "config": config} for url in args.urls]
    else:
        args.scan_examples = True
        cases = list(scan_example_urls(args.solver))

    browser_executable = find_browser_executable(args.browser_executable)
    converted, unsupported = convert_cases(cases, args.frontend, browser_executable, not args.headed)

    output = {
        "format": "noqx-direct-url-examples",
        "version": 1,
        "converted": converted,
        "unsupported": unsupported,
    }
    text = json.dumps(output, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

    print(f"converted={len(converted)} unsupported={len(unsupported)}", file=sys.stderr)
    return 0 if converted else 1


if __name__ == "__main__":
    raise SystemExit(main())
