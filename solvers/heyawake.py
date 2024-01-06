"""The Heyawake solver."""

from typing import List

from . import utils
from .claspy import BoolVar, require
from .utils.borders import Direction
from .utils.encoding import Encoding
from .utils.regions import RectangularGridRegionSolver, full_bfs
from .utils.shading import RectangularGridShadingSolver


def encode(string: str) -> Encoding:
    return utils.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    rooms = full_bfs(E.R, E.C, E.edges, E.clues)

    shading_solver = RectangularGridShadingSolver(E.R, E.C)
    shading_solver.no_adjacent()
    shading_solver.white_connectivity()
    region_solver = RectangularGridRegionSolver(E.R, E.C, shading_solver.grid, given_regions=rooms)
    region_solver.set_shaded_cells_in_region(E.clues, [True])

    for r in range(E.R):
        borders_in_row = [c for c in range(1, E.C) if (r, c, Direction.LEFT) in E.edges]
        # for each pair of consecutive borders, we get a constraint:
        # at least one cell in this span has to be shaded
        for i in range(len(borders_in_row) - 1):
            b1, b2 = borders_in_row[i], borders_in_row[i + 1]
            x = BoolVar(False)
            for c in range(b1 - 1, b2 + 1):
                x |= shading_solver.grid[r][c]
            require(x)

    for c in range(E.C):
        borders_in_col = [r for r in range(1, E.R) if (r, c, Direction.TOP) in E.edges]
        for i in range(len(borders_in_col) - 1):
            b1, b2 = borders_in_col[i], borders_in_col[i + 1]
            x = BoolVar(False)
            for r in range(b1 - 1, b2 + 1):
                x |= shading_solver.grid[r][c]
            require(x)

    return shading_solver.solutions(shaded_color="darkgray")


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
