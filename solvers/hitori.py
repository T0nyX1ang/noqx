"""The Hitori solver."""

from typing import List

from . import utils
from .claspy import require, set_max_val
from .utils.encoding import Encoding
from .utils.shading import RectangularGridShadingSolver


def encode(string: str) -> Encoding:
    return utils.encode(string)


def solve(E: Encoding) -> List:
    set_max_val(max(E.R, E.C))
    s = RectangularGridShadingSolver(E.R, E.C)

    K = list(E.clues.keys())
    for i, (r, c) in enumerate(K):
        for r1, c1 in K[i + 1 :]:
            if E.clues[(r, c)] == E.clues[(r1, c1)] and (r == r1 or c == c1):
                require(s.grid[r][c] | s.grid[r1][c1])
    s.no_adjacent()
    s.white_connectivity()

    return s.solutions()


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
