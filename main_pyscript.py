"""Entry point for the noqx-pyscript connector."""

from pyscript import window  # pylint: disable=import-error  # type: ignore  # noqa: I001

from noqx.manager import prepare_puzzle, generate_program, store_solution, load_solvers

load_solvers("solver")

window.prepare_puzzle = prepare_puzzle
window.generate_program = generate_program
window.store_solution = store_solution
