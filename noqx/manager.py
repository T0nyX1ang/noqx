"""Manager of all the solvers as a plugin."""

import importlib
import logging
import pkgutil
import time
from types import ModuleType
from typing import Any, Dict, List

from noqx.clingo import ClingoSolver, Config
from noqx.puzzle import Puzzle
from noqx.puzzle.penpa import PenpaPuzzle
from noqx.solution import store_solutions

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


def prepare_puzzle(puzzle_name: str, puzzle_content: str, param: Dict[str, Any]) -> Puzzle:
    """Prepare the puzzle."""
    puzzle = PenpaPuzzle(puzzle_name, puzzle_content, param)
    puzzle.decode()

    return puzzle


def generate_program(puzzle: Puzzle) -> str:
    """Generate the solver program."""
    module = modules[puzzle.puzzle_name]
    if not hasattr(module, "program"):
        raise NotImplementedError("Solver program not implemented.")

    logging.debug(f"[Solver] {str(puzzle.puzzle_name).capitalize()} puzzle program generated.")
    return module.program(puzzle)


def refine_solution(puzzle: Puzzle, raw_solutions: List[str]) -> List[str]:
    """Refine every solution."""
    module = modules[puzzle.puzzle_name]

    solutions: List[str] = []
    for model_str in raw_solutions:
        solution = store_solutions(puzzle, model_str)
        if hasattr(module, "refine"):  # refine the solution if possible
            module.refine(solution)

        solutions.append(solution.encode())

    return solutions


def run_solver(puzzle_name: str, puzzle_content: str, param: Dict[str, Any]) -> Dict[str, List[str]]:
    """Run the solver."""
    start = time.perf_counter()  # start the counter
    puzzle = prepare_puzzle(puzzle_name, puzzle_content, param)
    program = generate_program(puzzle)

    instance = ClingoSolver()
    instance.solve(program)
    raw_solutions: List[str] = instance.solution()

    solutions = refine_solution(puzzle, raw_solutions)
    stop = time.perf_counter()  # stop the counter

    if (stop - start) >= Config.time_limit:
        logging.warning(f"[Solver] {str(puzzle_name).capitalize()} puzzle timed out.")
        raise TimeoutError("Time limit exceeded.")

    logging.info(f"[Solver] {str(puzzle_name).capitalize()} puzzle solved.")
    logging.info(f"[Stats] {str(puzzle_name).capitalize()} solver took {stop - start} seconds.")

    return {"url": solutions}
