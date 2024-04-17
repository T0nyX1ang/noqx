"""The Sudoku solver."""

from typing import Dict, List

from .utilsx.common import area, display, fill_num, grid, unique_num
from .utilsx.encoding import Encoding
from .utilsx.neighbor import adjacent
from .utilsx.solution import solver


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(9, 9))
    solver.add_program_line(adjacent(_type="x"))

    for i in range(9):
        for j in range(9):
            area_id = (i // 3) * 3 + (j // 3)
            solver.add_program_line(area(area_id, [(i, j)]))

    solver.add_program_line(fill_num(_range=range(1, 10)))
    solver.add_program_line(unique_num(_type="row", color="grid"))
    solver.add_program_line(unique_num(_type="col", color="grid"))
    solver.add_program_line(unique_num(_type="area", color="grid"))

    for (r, c), num in E.clues.items():
        solver.add_program_line(f"number({r}, {c}, {num}).")

    if E.params["Diagonal"]:  # diagonal rule
        for i in range(9):
            solver.add_program_line(f"area(10, {i}, {i}).")
            solver.add_program_line(f"area(11, {i}, {8 - i}).")

    if E.params["Untouch"]:  # untouch rule
        solver.add_program_line(":- number(R, C, N), number(R1, C1, N), adj_x(R, C, R1, C1).")

    if E.params["Nonconsecutive"]:  # untouch rule
        solver.add_program_line(":- number(R, C, N), number(R1, C1, N1), adj_x(R, C, R1, C1), |N - N1| = 1.")

    if E.params["Antiknight"]:  # antiknight rule
        solver.add_program_line("adj_knight(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| = 2, |C - C1| = 1.")
        solver.add_program_line("adj_knight(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| = 1, |C - C1| = 2.")
        solver.add_program_line(":- number(R, C, N), number(R1, C1, N), adj_knight(R, C, R1, C1).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions
