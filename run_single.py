"""
Test a single case within a certain solver in Noqx.

Useful for debugging a specific solver with performance improvements.
"""

import argparse
import json
import logging
import os
import pkgutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from noqx.clingo import ClingoSolver, Config
from noqx.manager import generate_program, list_solver_metadata, load_solver, prepare_puzzle, store_solution

parser = argparse.ArgumentParser(description="Simple case test in Noqx.")
parser.add_argument("-n", "--puzzle-name", required=True, type=str, help="The puzzle name.")
parser.add_argument("-e", "--example-number", default=0, type=int, help="Number of the example, starting from 0.")
parser.add_argument("-l", "--link", default="", type=str, help="The puzzle link.")
parser.add_argument("-p", "--parameter", default="{}", type=str, help="The parameters to pass to the solver in JSON format.")
parser.add_argument("-tl", "--time-limit", default=Config.time_limit, type=int, help="time limit in seconds.")
parser.add_argument("-pt", "--parallel-threads", default=Config.parallel_threads, type=int, help="parallel threads.")
parser.add_argument("-bp", "--browser-path", default=None, type=str, help="The path to the browser executable for Playwright.")
args = parser.parse_args()
Config.time_limit = args.time_limit
Config.parallel_threads = args.parallel_threads

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG
)


def playwright_module():
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        logging.error("Playwright is required for front-end URL conversion.")
        logging.error("Please run with: uv run --with playwright python tests/puzzlink_to_direct.py ...")
        sys.exit(1)
    return sync_playwright


def find_browser_executable(explicit_path: Optional[str] = None) -> Optional[str]:
    """Find a locally installed Chromium-family browser."""
    candidates = []
    if explicit_path:
        candidates.append(Path(explicit_path))
    candidates.extend(
        [
            Path("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"),
            Path("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"),
            Path("C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"),
            Path("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"),
        ]
    )

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return None


def load_puzzlink_content(link: str) -> str:
    """Convert a puzz.link URL into the Penpa+ payload."""
    sync_playwright = playwright_module()
    frontend_path = os.path.join(".", "penpa-edit", "index.html")
    frontend_uri = "file:///" + os.path.abspath(frontend_path).replace("\\", "/")
    browser_executable = find_browser_executable(args.browser_path)

    with sync_playwright() as playwright:
        launch_kwargs: Dict[str, Any] = {"headless": True}
        if browser_executable:
            launch_kwargs["executable_path"] = browser_executable

        # warning: only Chromium-family browsers are supported in this script
        browser = playwright.chromium.launch(**launch_kwargs)
        page = browser.new_page()
        page.goto(frontend_uri, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_function(
            "typeof imp === 'function' && typeof exp === 'function' && typeof solver_metadata !== 'undefined'",
            timeout=60000,
        )

        selected = page.evaluate(f'$("#type").val("{puzzle_name}").trigger("change");')
        if not selected:
            logging.error(f"Failed to select puzzle type: {puzzle_name}. Please ensure the puzzle is supported in Penpa+.")
            sys.exit(1)

        imported = page.evaluate("(url) => imp(url, true)", link)
        if not imported:
            logging.error("Failed to import URL. Please ensure the link is valid and the puzzle is supported in Penpa+.")
            sys.exit(1)

        result = page.evaluate("exp();")
        browser.close()
        return result


for module_info in pkgutil.iter_modules(["solver"]):
    load_solver("solver", module_info.name)

metadata = list_solver_metadata()

if not args.puzzle_name or args.puzzle_name not in metadata:
    logging.error(f"Invalid puzzle name: {args.puzzle_name}.")
    sys.exit(1)

puzzle_name = args.puzzle_name
link = args.link
puzzle_content = ""

if args.example_number < 0:
    logging.error("Invalid example number. It must be a non-negative integer.")
    sys.exit(1)

params = metadata[puzzle_name]["examples"][args.example_number].get("config", {})

if not link:
    candidate = metadata[puzzle_name]["examples"][args.example_number]
    if "url" in candidate:
        link = candidate["url"]
        puzzle_content = load_puzzlink_content(link)

    if "data" in candidate:
        link = candidate["data"]
        puzzle_content = link

    if not link:
        logging.error("Unable to extract a link from parameters.")
        sys.exit(1)

else:
    puzzle_content = load_puzzlink_content(link)

if not params:
    try:
        params = json.loads(args.parameter)
    except json.JSONDecodeError:
        logging.error("Invalid parameter format.")
        sys.exit(1)

puzzle = prepare_puzzle(puzzle_name, puzzle_content, params)
program = generate_program(puzzle)

instance = ClingoSolver()
instance.solve(program)
total_time = instance.statistics["summary"]["times"]["total"]

logging.debug(f"[Solver] {str(puzzle_name).capitalize()} puzzle solved.")

solutions: List[str] = []
URL_PREFIX = "https://swaroopg92.github.io/penpa-edit/#"
for i, solution in enumerate(instance.solution()):
    solution = store_solution(puzzle, solution)
    logging.debug(f"[Solver] Solution {i + 1} URL -> {URL_PREFIX}{solution.encode()}")

if total_time >= Config.time_limit and len(solutions) == 0:
    logging.warning(f"[Solver] {str(puzzle_name).capitalize()} puzzle timed out.")
    raise TimeoutError("Time limit exceeded.")

logging.debug(f"[Solver] {str(puzzle_name).capitalize()} puzzle statistics: {instance.statistics}.")
