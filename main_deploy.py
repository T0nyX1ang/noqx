"""Entry point for the deployment."""

from typing import Any, Dict

from pyscript import window  # pylint: disable=import-error  # type: ignore  # noqa: I001

from noqx.manager import Solver, generate_program, modules, prepare_puzzle, store_solution
from noqx.puzzle import Puzzle


def js_load_solvers(solver_dir: str):
    """Load the solvers from a valid directory."""
    solver_metadata = window.solver_metadata.to_py()
    for pt in sorted(solver_metadata.keys()):
        __import__(f"{solver_dir}.{pt}")

    for solver_cls in Solver.__subclasses__():
        puzzle_type = solver_cls.__module__.lower().replace(solver_dir, "").replace(".", "")
        if puzzle_type in modules:  # pragma: no cover
            raise ValueError(f"Solver for {puzzle_type} already exists.")

        modules[puzzle_type] = solver_cls()


def _prepare_puzzle(puzzle_name: str, puzzle_content: str, param: Dict[str, Any]):
    try:
        return prepare_puzzle(puzzle_name, puzzle_content, param.to_py())
    except Exception as e:
        raise RuntimeWarning(str(e)) from e


def _generate_program(puzzle: Puzzle):
    try:
        return generate_program(puzzle)
    except Exception as e:
        raise RuntimeWarning(str(e)) from e


js_load_solvers("solver")
window.prepare_puzzle = _prepare_puzzle
window.generate_program = _generate_program
window.store_solution = store_solution
