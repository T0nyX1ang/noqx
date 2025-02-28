"""Entry point for the noqx-pyscript connector."""

from typing import Any, Dict

from pyscript import window  # pylint: disable=import-error  # type: ignore  # noqa: I001

from noqx.manager import generate_program, load_solvers, prepare_puzzle, store_solution
from noqx.puzzle import Puzzle

load_solvers("solver")


def _prepare_puzzle(puzzle_name: str, puzzle_content: str, param: Dict[str, Any]):
    return prepare_puzzle(puzzle_name, puzzle_content, param.to_py())


def _generate_program(puzzle: Puzzle):
    try:
        return generate_program(puzzle)
    except Exception as e:
        raise RuntimeWarning(str(e)) from e


window.prepare_puzzle = _prepare_puzzle
window.generate_program = _generate_program
window.store_solution = store_solution
