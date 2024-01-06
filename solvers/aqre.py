"""The Aqre solver."""

from typing import List

from . import utils
from .claspy import require, set_max_val, sum_bools
from .utils.encoding import Encoding
from .utils.regions import full_bfs
from .utils.shading import RectangularGridShadingSolver


def encode(string: str) -> Encoding:
    return utils.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    set_max_val(E.R * E.C)

    shading_solver = RectangularGridShadingSolver(E.R, E.C)
    shading_solver.black_connectivity()
    grid = shading_solver.grid

    # GIVEN NUMBERS ARE SATISFIED
    if E.clues:
        for coord in (clue_regions := full_bfs(E.R, E.C, E.edge_ids, clues=E.clues)):
            require(sum_bools(E.clues[coord], [grid[other] for other in clue_regions[coord]]))

    # NO FOUR IN A ROW
    for i in range(E.R):
        for j in range(E.C):
            if i < E.R - 3:
                require(grid[(i, j)] | grid[(i + 1, j)] | grid[(i + 2, j)] | grid[(i + 3, j)])
                require((~grid[(i, j)]) | (~grid[(i + 1, j)]) | (~grid[(i + 2, j)]) | (~grid[(i + 3, j)]))
            if j < E.C - 3:
                require(grid[(i, j)] | grid[(i, j + 1)] | grid[(i, j + 2)] | grid[(i, j + 3)])
                require((~grid[(i, j)]) | (~grid[(i, j + 1)]) | (~grid[(i, j + 2)]) | (~grid[(i, j + 3)]))

    return shading_solver.solutions(shaded_color="darkgray")


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
