"""Generate solutions for the given problem."""

import logging
from typing import List

from clingo import MessageCode
from clingo.control import Control
from clingo.solving import Model


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
