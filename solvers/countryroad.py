"""The Country Road solver."""

from typing import List

from . import utils
from .claspy import require, reset, set_max_val, sum_bools, var_in
from .utils.encoding import Encoding
from .utils.loops import ISOLATED, RectangularGridLoopSolver
from .utils.regions import full_bfs, RectangularGridRegionSolver


def encode(string: str) -> Encoding:
    return utils.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    rooms = full_bfs(E.R, E.C, E.edges)

    # get the size of the largest room
    max_room_size = max(len(room) for room in rooms)

    # reset clasp, and set the maximum IntVar value to the max room size
    reset()
    set_max_val(max_room_size)

    loop_solver = RectangularGridLoopSolver(E.R, E.C)
    loop_solver.loop(E.clues, includes_clues=True)
    loop_solver.no_reentrance(rooms)
    loop_solver.hit_every_region(rooms)

    region_solver = RectangularGridRegionSolver(E.R, E.C, loop_solver.grid, given_regions=rooms)

    for r, c in E.clues:
        for room in rooms:
            if (r, c) in room:
                clued_room = room
        require(sum_bools(E.clues[(r, c)], [~var_in(loop_solver.grid[y][x], ISOLATED) for (y, x) in clued_room]))

    for r in range(E.R):
        for c in range(E.C):
            for y, x in region_solver.get_neighbors_in_other_regions(r, c):
                require(~(var_in(loop_solver.grid[r][c], ISOLATED) & var_in(loop_solver.grid[y][x], ISOLATED)))

    return loop_solver.solutions()


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
