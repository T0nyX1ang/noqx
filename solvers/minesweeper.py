"""The Minesweeper solver."""

from typing import List

from . import utils
from .utils.claspy import require, set_max_val, sum_bools
from .utils.encoding import Encoding
from .utils.shading import RectangularGridShadingSolver


def encode(string: str) -> Encoding:
    return utils.encode(string)


def solve(E: Encoding) -> List:
    set_max_val(8)
    shading_solver = RectangularGridShadingSolver(E.R, E.C)

    # Enforce that clue cells can't be shaded, and that their numbers are correct
    shading_solver.white_clues(E.clues)

    for cell, num in E.clues.items():
        if num != "?":
            require(sum_bools(num, [shading_solver.grid[surr] for surr in shading_solver.grid.get_surroundings(*cell)]))

    return shading_solver.solutions()


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
