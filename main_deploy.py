"""Entry point for the deployment."""

from typing import Any, Dict

from pyscript import window  # pylint: disable=import-error  # type: ignore  # noqa: I001

from noqx.manager import generate_program, load_solvers, prepare_puzzle, store_solution
from noqx.puzzle import Puzzle


def _prepare_puzzle(puzzle_name: str, puzzle_content: str, param: Dict[str, Any]):
    try:
        return {
            "success": True,
            "result": prepare_puzzle(puzzle_name, puzzle_content, param.to_py()),
        }
    except Exception as e:  # pylint: disable=broad-except
        return {
            "success": False,
            "result": str(e),
        }


def _generate_program(puzzle: Puzzle):
    try:
        return {
            "success": True,
            "result": generate_program(puzzle),
        }
    except Exception as e:  # pylint: disable=broad-except
        return {
            "success": False,
            "result": str(e),
        }


def _store_solution(puzzle: Puzzle, model_str: str):
    try:
        return {
            "success": True,
            "result": store_solution(puzzle, model_str).encode(),
        }
    except Exception as e:  # pylint: disable=broad-except
        return {
            "success": False,
            "result": str(e),
        }


load_solvers("solver")
window.prepare_puzzle = _prepare_puzzle
window.generate_program = _generate_program
window.store_solution = _store_solution
