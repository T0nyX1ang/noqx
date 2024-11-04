"""Manager of all the solvers as a plugin."""

import importlib
import pkgutil
import time
from types import ModuleType
from typing import Any, Dict, List

from .logging import logger
from .penpa import Puzzle
from .solution import Config

solver_dir = "solver"  # default solver directory

puzzle_types: List[str] = []
for module_info in pkgutil.iter_modules([solver_dir]):
    puzzle_types.append(module_info.name)

modules: Dict[str, ModuleType] = {}
for pt in sorted(puzzle_types):
    modules[pt] = importlib.import_module(f"{solver_dir}.{pt}")


def list_solver_metadata() -> Dict[str, Any]:
    """List all available solver metadata."""
    metadata = {}
    for puzzle_type, module in modules.items():
        if hasattr(module, "__metadata__"):
            metadata[puzzle_type] = module.__metadata__
        else:
            metadata[puzzle_type] = {
                "name": puzzle_type.capitalize().replace("_", " "),
                "category": "unk",
                "aliases": [],
                "examples": [],
            }

    return metadata


def run_solver(puzzle_type: str, puzzle_content: str, param: Dict[str, Any]) -> Dict[str, List[str]]:
    """Run the solver."""
    module = modules[puzzle_type]

    if not hasattr(module, "solve"):
        raise NotImplementedError("Solver not implemented.")

    start = time.time()
    puzzle: Puzzle = Puzzle(puzzle_type, puzzle_content, param)
    solutions: List[str] = list(map(str, module.solve(puzzle)))
    stop = time.time()

    if (stop - start) >= Config.time_limit:
        logger.warning(f"[Solver] {str(puzzle_type).capitalize()} puzzle timed out.")
        raise TimeoutError("Time limit exceeded.")

    logger.info(f"[Solver] {str(puzzle_type).capitalize()} puzzle solved.")
    logger.info(f"[Stats] {str(puzzle_type).capitalize()} solver took {stop - start} seconds.")

    return {"url": solutions}  # return the first solution
