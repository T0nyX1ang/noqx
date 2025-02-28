"""Entry point for the noqx-pyscript connector."""

from typing import Any, Dict

from pyscript import window  # pylint: disable=import-error  # type: ignore  # noqa: I001

from noqx.manager import generate_program, load_solvers, prepare_puzzle, store_solution

load_solvers("solver")


def _prepare_puzzle(puzzle_name: str, puzzle_content: str, param: Dict[str, Any]):
    return prepare_puzzle(puzzle_name, puzzle_content, param.to_py())


window.prepare_puzzle = _prepare_puzzle
window.generate_program = generate_program
window.store_solution = store_solution
