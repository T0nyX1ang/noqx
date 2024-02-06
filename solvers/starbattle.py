"""The Star Battle solver."""

from typing import List

from . import utils
from .utils.claspy import require, set_max_val, sum_bools
from .utils.encoding import Encoding
from .utils.regions import full_bfs
from .utils.shading import RectangularGridShadingSolver


def encode(string: str) -> Encoding:
    return utils.encode(string, has_params=True, has_borders=True)


def solve(E: Encoding) -> List:
    num_stars = int(E.params["stars"])
    set_max_val(num_stars)

    rooms = full_bfs(E.R, E.C, E.edges)

    shading_solver = RectangularGridShadingSolver(E.R, E.C)
    shading_solver.no_surrounding()

    for room in rooms:
        require(sum_bools(num_stars, [shading_solver.grid[r][c] for (r, c) in room]))

    for r in range(E.R):
        require(sum_bools(num_stars, [shading_solver.grid[r][c] for c in range(E.C)]))

    for c in range(E.C):
        require(sum_bools(num_stars, [shading_solver.grid[r][c] for r in range(E.R)]))

    return shading_solver.solutions(shaded_color="gray")


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
