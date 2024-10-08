"""Initialize the solver manager."""

import importlib
import time
from types import ModuleType
from typing import Any, Dict, List

from .core.const import PUZZLE_TYPES, logger
from .core.penpa import Puzzle
from .core.solution import Config

modules: Dict[str, ModuleType] = {}
for pt in PUZZLE_TYPES:
    modules[pt] = importlib.import_module(f"solver.{pt.replace('-', '_')}")  # load module


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
    logger.info(f"[Stats] {str(puzzle_type).capitalize()} solver took {stop - start} seconds")

    return {"url": solutions}  # return the first solution
