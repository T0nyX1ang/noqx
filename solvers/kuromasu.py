"""The Kuromasu solver."""

from typing import List

from . import utils
from .claspy import BoolVar, IntVar, require, set_max_val
from .utils.encoding import Encoding
from .utils.shading import RectangularGridShadingSolver


def encode(string: str) -> Encoding:
    return utils.encode(string)


def solve(E: Encoding) -> List:
    set_max_val(E.R * E.C)

    s = RectangularGridShadingSolver(E.R, E.C)
    arbitrary_white_clue = None  # Use this later

    # Steal code from Cave
    for (r, c), value in E.clues.items():
        arbitrary_white_clue = (r, c)
        if value == "?":
            continue
        dirs = {}
        for u, v in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ray = []
            n = 1
            while 0 <= r + u * n < E.R and 0 <= c + v * n < E.C:  # add all ray cells
                ray.append((r + u * n, c + v * n))
                n += 1
            num_seen_cells = IntVar(0, len(ray))
            for n in range(len(ray) + 1):
                cond_n = BoolVar(True)
                for d in range(n):
                    cond_n &= ~s.grid[ray[d]]
                if n < len(ray):
                    cond_n &= s.grid[ray[n]]
                require((num_seen_cells == n) == cond_n)
            dirs[(u, v)] = num_seen_cells
        require(dirs[(1, 0)] + dirs[(-1, 0)] + dirs[(0, 1)] + dirs[(0, -1)] == E.clues[(r, c)] - 1)

    # Simple rules
    s.white_connectivity(arbitrary_white_clue)
    s.no_adjacent()
    s.white_clues(E.clues)

    return s.solutions()


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
