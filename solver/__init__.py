"""Initialize the solver manager."""

import importlib
import time
from types import ModuleType
from typing import Dict, List

from .core.const import PUZZLE_TYPES
from .core.penpa import Puzzle

modules: Dict[str, ModuleType] = {}
for pt in PUZZLE_TYPES:
    modules[pt] = importlib.import_module(f"solver.{pt}")  # load module


def run_solver(puzzle_type: str, puzzle_content: str) -> Dict[str, List[str]]:
    """Run the solver."""
    module = modules[puzzle_type]

    if not hasattr(module, "solve"):
        raise NotImplementedError("Solver not implemented.")

    start = time.time()
    puzzle: Puzzle = Puzzle(puzzle_content)
    solutions: List[str] = module.solve(puzzle)
    stop = time.time()
    print(f"[Stats] {str(puzzle_type)} solver took {stop - start} seconds")
    return {"url": solutions}  # return the first solution
