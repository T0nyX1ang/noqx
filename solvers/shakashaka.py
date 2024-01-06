"""The Shakashaka solver."""

from typing import List

from . import utils
from .claspy import MultiVar, require, set_max_val, sum_bools, var_in
from .utils.encoding import Encoding
from .utils.grids import is_valid_coord, get_neighbors
from .utils.solutions import get_all_grid_solutions


def encode(string: str) -> Encoding:
    return utils.encode(string)


def solve(E: Encoding) -> List:
    set_max_val(4)

    tl = "top-left.png"
    tr = "top-right.png"
    bl = "bottom-left.png"
    br = "bottom-right.png"

    TRIANGLE_SYMBOLS = (tl, tr, bl, br)

    grid = [[MultiVar(*TRIANGLE_SYMBOLS, " ", "") for c in range(E.C)] for r in range(E.R)]

    # Diagonal rectangles
    for r in range(E.R):
        for c in range(E.C):
            # ---- Upper-left triangle shading ----
            if is_valid_coord(E.R, E.C, r - 1, c + 1):
                # If this cell has upper-left triangle shading,
                require(
                    (grid[r][c] != tl)
                    |
                    # The cell up and to the right of it is upper-left triangle,
                    # and the cell to the right of it is unshaded
                    ((grid[r - 1][c + 1] == tl) & (grid[r][c + 1] == " "))
                    |
                    # Or the cell immediately to the right is upper-right triangle.
                    (grid[r][c + 1] == tr)
                )
            elif is_valid_coord(E.R, E.C, r, c + 1):
                require(
                    (grid[r][c] != tl)
                    |
                    # The cell immediately to the right is upper-right triangle.
                    (grid[r][c + 1] == tr)
                )
            if is_valid_coord(E.R, E.C, r + 1, c - 1):
                require(
                    (grid[r][c] != tl)
                    |
                    # The cell down and to the left of it is upper-left triangle,
                    # and the cell below it is unshaded.
                    ((grid[r + 1][c - 1] == tl) & (grid[r + 1][c] == " "))
                    |
                    # Or the cell immediately below is lower-left triangle.
                    (grid[r + 1][c] == bl)
                )
            elif is_valid_coord(E.R, E.C, r + 1, c):
                require(
                    (grid[r][c] != tl)
                    |
                    # The cell immediately below is lower-left triangle.
                    (grid[r + 1][c] == bl)
                )
            # Cells in the bottom row and rightmost column cannot have upper-left triangle shading.
            if r == E.R - 1 or c == E.C - 1:
                require(grid[r][c] != tl)

            # ---- Upper-right triangle shading ----
            if is_valid_coord(E.R, E.C, r - 1, c - 1):
                require(
                    (grid[r][c] != tr)
                    |
                    # The cell up and to the left of it is upper-right triangle,
                    # and the cell to the left of it is unshaded
                    ((grid[r - 1][c - 1] == tr) & (grid[r][c - 1] == " "))
                    |
                    # Or the cell immediately to the left is upper-left triangle.
                    (grid[r][c - 1] == tl)
                )
            elif is_valid_coord(E.R, E.C, r, c - 1):
                require(
                    (grid[r][c] != tr)
                    |
                    # The cell immediately to the left is upper-left triangle.
                    (grid[r][c - 1] == tl)
                )
            if is_valid_coord(E.R, E.C, r + 1, c + 1):
                require((grid[r][c] != tr) | ((grid[r][c] == tr) & (grid[r + 1][c] == " ")) | (grid[r + 1][c] == br))
            elif is_valid_coord(E.R, E.C, r + 1, c):
                require((grid[r][c] != tr) | (grid[r + 1][c] == br))
            if r == E.R - 1 or c == 0:
                # Cannot be upper-right triangle.
                require(grid[r][c] != tr)

            # ---- Lower-left triangle shading ----
            if is_valid_coord(E.R, E.C, r + 1, c + 1):
                require(
                    (grid[r][c] != bl) | ((grid[r + 1][c + 1] == bl) & (grid[r][c + 1] == " ")) | (grid[r][c + 1] == br)
                )
            elif is_valid_coord(E.R, E.C, r, c + 1):
                require((grid[r][c] != bl) | (grid[r][c + 1] == br))
            if is_valid_coord(E.R, E.C, r - 1, c - 1):
                require(
                    (grid[r][c] != bl) | ((grid[r - 1][c - 1] == bl) & (grid[r - 1][c] == " ")) | (grid[r - 1][c] == tl)
                )
            elif is_valid_coord(E.R, E.C, r - 1, c):
                require((grid[r][c] != bl) | (grid[r - 1][c] == tl))
            if r == 0 or c == E.C - 1:
                require(grid[r][c] != bl)

            # ---- Lower-right triangle shading ----
            if is_valid_coord(E.R, E.C, r + 1, c - 1):
                require(
                    (grid[r][c] != br) | ((grid[r + 1][c - 1] == br) & (grid[r][c - 1] == " ")) | (grid[r][c - 1] == bl)
                )
            elif is_valid_coord(E.R, E.C, r, c - 1):
                require((grid[r][c] != br) | (grid[r][c - 1] == bl))
            if is_valid_coord(E.R, E.C, r - 1, c + 1):
                require(
                    (grid[r][c] != br) | ((grid[r - 1][c + 1] == br) & (grid[r - 1][c] == " ")) | (grid[r - 1][c] == tr)
                )
            elif is_valid_coord(E.R, E.C, r - 1, c):
                require((grid[r][c] != br) | (grid[r - 1][c] == tr))
            if r == 0 or c == 0:
                require(grid[r][c] != br)

    # Grid-aligned rectangles
    for r in range(E.R):
        for c in range(E.C):
            # If there is a cell up and to the right
            if is_valid_coord(E.R, E.C, r - 1, c + 1):
                # If this cell, the cell above, and the cell to the right are all unshaded
                # The cell up and to the right must have an unshaded lower left
                require(
                    ~((grid[r][c] == " ") & (grid[r - 1][c] == " ") & (grid[r][c + 1] == " "))
                    | (var_in(grid[r - 1][c + 1], (" ", tr)))
                )
            # If there is a cell up and to the left
            if is_valid_coord(E.R, E.C, r - 1, c - 1):
                require(
                    ~((grid[r][c] == " ") & (grid[r - 1][c] == " ") & (grid[r][c - 1] == " "))
                    | (var_in(grid[r - 1][c - 1], (" ", tl)))
                )
            # If there is a cell down and to the right
            if is_valid_coord(E.R, E.C, r + 1, c + 1):
                require(
                    ~((grid[r][c] == " ") & (grid[r + 1][c] == " ") & (grid[r][c + 1] == " "))
                    | (var_in(grid[r + 1][c + 1], (" ", br)))
                )
            # If there is a cell down and to the left
            if is_valid_coord(E.R, E.C, r + 1, c - 1):
                require(
                    ~((grid[r][c] == " ") & (grid[r + 1][c] == " ") & (grid[r][c - 1] == " "))
                    | (var_in(grid[r + 1][c - 1], (" ", bl)))
                )

    # Clues indicate the number of neighbors that have triangle shading.
    for r, c in E.clues:
        if E.clues[(r, c)] != "black":
            require(
                sum_bools(
                    E.clues[(r, c)],
                    [var_in(grid[y][x], TRIANGLE_SYMBOLS) for (y, x) in get_neighbors(E.R, E.C, r, c)],
                )
            )

    # A cell is fully shaded iff it is a clue cell.
    for r in range(E.R):
        for c in range(E.C):
            if (r, c) not in E.clues:
                require(grid[r][c] != "")
            else:
                require(grid[r][c] == "")

    return get_all_grid_solutions(grid)


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
