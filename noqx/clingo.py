"""Generate solutions for the given problem."""

import logging
import time
from typing import Any, Dict, List

from clingo import MessageCode
from clingo.control import Control
from clingo.solving import Model

from noqx.manager import generate_program, prepare_puzzle, store_solution


def clingo_logging_handler(code: MessageCode, message: str) -> None:  # pragma: no cover
    """Handle clingo logging."""
    if code == MessageCode.RuntimeError:
        logging.error(f"[Clingo] {code.name}: {message.strip()}")
    else:
        logging.warning(f"[Clingo] {code.name}: {message.strip()}")


class Config:
    """Configuration for the solver."""

    time_limit: int = 30
    max_solutions_to_find: int = 10
    parallel_threads: int = 1


class ClingoSolver:
    """A solver using clingo."""

    def __init__(self):
        """Initialize a solver."""
        self.clingo_instance: Control = Control(logger=clingo_logging_handler)
        self.model: List[str] = []

    def store_model(self, model: Model):  # pragma: no cover
        """Store the model on solving."""
        self.model.append(str(model))

    def solve(self, program: str):
        """Solve the problem."""
        self.clingo_instance.configuration.sat_prepro = 2
        self.clingo_instance.configuration.asp.trans_ext = "dynamic"  # type: ignore
        self.clingo_instance.configuration.asp.eq = 1  # type: ignore
        self.clingo_instance.configuration.solve.parallel_mode = Config.parallel_threads  # type: ignore
        self.clingo_instance.configuration.solve.models = Config.max_solutions_to_find  # type: ignore
        self.clingo_instance.add(program=program)
        self.clingo_instance.ground()
        with self.clingo_instance.solve(on_model=self.store_model, async_=True) as handle:  # type: ignore
            handle.wait(Config.time_limit)
            handle.cancel()

    def solution(self) -> List[str]:
        """Get the solutions."""
        return self.model


def run_solver(puzzle_name: str, puzzle_content: str, param: Dict[str, Any]) -> Dict[str, List[str]]:
    """Run the clingo solver."""
    start = time.perf_counter()  # start the counter
    puzzle = prepare_puzzle(puzzle_name, puzzle_content, param)
    program = generate_program(puzzle)

    instance = ClingoSolver()
    instance.solve(program)

    solutions: List[str] = []
    for solution in instance.solution():
        solution = store_solution(puzzle, solution)
        solutions.append(solution.encode())

    stop = time.perf_counter()  # stop the counter

    if (stop - start) >= Config.time_limit:
        logging.warning(f"[Solver] {str(puzzle_name).capitalize()} puzzle timed out.")
        raise TimeoutError("Time limit exceeded.")

    logging.info(f"[Solver] {str(puzzle_name).capitalize()} puzzle solved.")
    logging.info(f"[Stats] {str(puzzle_name).capitalize()} solver took {stop - start} seconds.")

    return {"url": solutions}
