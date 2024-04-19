"""Initialize the solver manager."""

import importlib
from types import ModuleType
from typing import Dict, List

from .core.const import PUZZLE_TYPES
from .core.encoding import Encoding, decode, encode

modules: Dict[str, ModuleType] = {}
for pt_dict in PUZZLE_TYPES:
    value: str = pt_dict["value"]  # type: ignore
    modules[value] = importlib.import_module(f"solver.{value}")  # load module


def run_solver(puzzle_type: str, puzzle_content: str) -> str:
    """Run the solver."""
    module = modules[puzzle_type]

    if not hasattr(module, "encode"):
        module.encode = encode

    if not hasattr(module, "solve"):
        raise NotImplementedError("Solver not implemented.")

    if not hasattr(module, "decode"):
        module.decode = decode

    puzzle_encoded: Encoding = module.encode(puzzle_content)
    solutions_encoded: List[Dict[str, str]] = module.solve(puzzle_encoded)
    solutions_decoded: str = module.decode(solutions_encoded)
    return solutions_decoded
