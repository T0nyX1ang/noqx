"""The N Cells solver."""

from typing import List

from . import utils
from .claspy import set_max_val
from .utils.borders import RectangularGridBorderSolver
from .utils.encoding import Encoding
from .utils.regions import RectangularGridRegionSolver


def encode(string: str) -> Encoding:
    return utils.encode(string, has_params=True)


def solve(E: Encoding) -> List:
    region_size = int(E.params["region_size"])

    assert (E.R * E.C) % region_size == 0, "It's impossible to divide grid into regions of this size!"

    # set the maximum IntVar value to the number of cells
    set_max_val(E.R * E.C)

    region_solver = RectangularGridRegionSolver(E.R, E.C, max_num_regions=E.R * E.C)
    border_solver = RectangularGridBorderSolver(E.R, E.C, region_solver)

    region_solver.set_region_size(region_size, [], min_region_size=region_size)
    region_solver.region_roots({})

    for r, c in E.clues:
        region_solver.set_num_neighbors_in_different_region(r, c, E.clues[(r, c)])

    return border_solver.solutions()


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
