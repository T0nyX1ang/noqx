"""Manager of all the solvers as a plugin."""

import importlib
import logging
import pkgutil
import time
from types import ModuleType
from typing import Any, Dict, List

from noqx.puzzle import Puzzle
from noqx.puzzle.penpa import PenpaPuzzle
from noqx.solution import Config, instance

modules: Dict[str, ModuleType] = {}


def load_solvers(solver_dir: str):
    """Load the solvers from a valid directory."""
    puzzle_names: List[str] = []
    for module_info in pkgutil.iter_modules([solver_dir]):
        puzzle_names.append(module_info.name)

    for pt in sorted(puzzle_names):
        modules[pt] = importlib.import_module(f"{solver_dir}.{pt}")


def list_solver_metadata() -> Dict[str, Any]:
    """List all available solver metadata."""
    metadata = {}
    for puzzle_name, module in modules.items():
        if hasattr(module, "__metadata__"):
            metadata[puzzle_name] = module.__metadata__
        else:
            metadata[puzzle_name] = {
                "name": puzzle_name.capitalize().replace("_", " "),
                "category": "unk",
                "aliases": [],
                "examples": [],
            }

    return metadata


def run_solver(puzzle_name: str, puzzle_content: str, param: Dict[str, Any]) -> Dict[str, List[str]]:
    """Run the solver."""
    module = modules[puzzle_name]

    if not hasattr(module, "program"):
        raise NotImplementedError("Solver program not implemented.")

    start = time.perf_counter()
    puzzle: Puzzle = PenpaPuzzle(puzzle_name, puzzle_content, param)
    puzzle.decode()

    program: str = module.program(puzzle)
    logging.debug(f"[Solver] {str(puzzle_name).capitalize()} puzzle program generated.")

    instance.reset()
    instance.register_puzzle(puzzle)
    instance.solve(program)
    solutions: List[Puzzle] = instance.solutions

    if hasattr(module, "refine"):  # refine the solution if possible
        for solution in solutions:
            module.refine(solution)

    final: List[str] = list(map(lambda x: x.encode(), solutions))
    stop = time.perf_counter()

    if (stop - start) >= Config.time_limit:
        logging.warning(f"[Solver] {str(puzzle_name).capitalize()} puzzle timed out.")
        raise TimeoutError("Time limit exceeded.")

    logging.info(f"[Solver] {str(puzzle_name).capitalize()} puzzle solved.")
    logging.info(f"[Stats] {str(puzzle_name).capitalize()} solver took {stop - start} seconds.")

    return {"url": final}
