"""The Kurotto solver."""

from typing import List

from . import utils
from .claspy import Atom, require, set_max_val, sum_bools
from .utils.encoding import Encoding
from .utils.grids import RectangularGrid
from .utils.shading import RectangularGridShadingSolver


def encode(string: str) -> Encoding:
    return utils.encode(string)


def solve(E: Encoding) -> List:
    set_max_val(E.R * E.C)

    shading_solver = RectangularGridShadingSolver(E.R, E.C)

    for r, c in E.clues:
        require(~shading_solver.grid[(r, c)])

    anchors = [coord for coord in E.clues if E.clues[coord] != "black"]
    # 'black' means an empty circle in this case; sorry, I'm being lazy with the encoding

    for anchor in anchors:
        flows = RectangularGrid(E.R, E.C, Atom)
        flows[anchor].prove_if(True)  # prove the anchor for free

        for r in range(E.R):
            for c in range(E.C):
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    r1 = r + dr
                    c1 = c + dc
                    if 0 <= r1 < E.R and 0 <= c1 < E.C:
                        if (r1, c1) == anchor:
                            flows[r][c].prove_if(shading_solver.grid[r][c])
                        else:
                            flows[r][c].prove_if(
                                shading_solver.grid[r][c] & shading_solver.grid[r1][c1] & flows[r1][c1]
                            )

        require(sum_bools(E.clues[anchor] + 1, [flows[r][c] for r in range(E.R) for c in range(E.C)]))
        # add 1 because the clue cell is proven but not black

    return shading_solver.solutions(shaded_color="black")


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
