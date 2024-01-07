"""The Yin-Yang solver."""

from typing import List

from . import utils
from .utils.claspy import require, set_max_val
from .utils.encoding import Encoding
from .utils.solutions import get_all_grid_solutions
from .utils.shading import RectangularGridShadingSolver


def encode(string: str) -> Encoding:
    return utils.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    set_max_val(2)

    s = RectangularGridShadingSolver(E.R, E.C)

    # Optimize solving by providing known roots for white and black parts
    white_root, black_root = None, None
    for r, c in E.clues:
        if E.clues[(r, c)] == "w":
            white_root = (r, c)
        else:
            black_root = (r, c)
        if white_root and black_root:
            break

    s.white_connectivity(white_root)
    s.black_connectivity(black_root)
    s.no_white_2x2()
    s.no_black_2x2()

    for r, c in E.clues:
        require(s.grid[r][c] == (E.clues[(r, c)] == "b"))

    def format_function(r, c):
        return ("black" if s.grid[r][c].value() else "white") + "_circle.png"

    return get_all_grid_solutions(s.grid, format_function=format_function)


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
