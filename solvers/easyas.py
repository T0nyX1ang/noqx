"""The Easy As solver."""

from typing import List

from .utils.claspy import MultiVar, BoolVar, require, sum_bools
from . import utils
from .utils.encoding import Encoding
from .utils.solutions import get_all_grid_solutions


def encode(string: str) -> Encoding:
    return utils.encode(string, has_params=True, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    letters = list(E.params["letters"])
    grid = [[MultiVar(*letters, "") for c in range(E.C)] for r in range(E.R)]

    # ENFORCE CLUED CELLS, IF ANY
    for r, c in E.clues:
        require(grid[r][c] == E.clues[(r, c)])

    # ENFORCE LATIN SQUARE CONSTRAINTS
    for i in range(E.R):
        for lt in letters:
            require(sum_bools(1, [grid[i][j] == lt for j in range(E.C)]))
            require(sum_bools(1, [grid[j][i] == lt for j in range(E.R)]))

    # ENFORCE FIRST-SEEN CONSTRAINTS IN EACH DIRECTION
    for side, clues in ("U", E.top), ("R", E.right), ("B", E.bottom), ("L", E.left):
        for i, lt in clues.items():
            view = BoolVar(False)
            for j in range(E.C) if side in "UL" else range(E.C - 1, -1, -1):  # iteration direction
                i1, i2 = (i, j) if side in "LR" else (j, i)  # row/col indices in some order

                # False = seen no letters yet, True = seen l first;
                # and implicitly require that no other possibilities exist
                new_view = BoolVar()
                require(~new_view == (~view & (grid[i1][i2] == "")))
                require(new_view == ((~view & (grid[i1][i2] == lt)) | view))
                view = new_view

    return get_all_grid_solutions(grid)


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
