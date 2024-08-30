"""The Magnets solver."""

from typing import List

from .core.common import area, count, display, grid, shade_cc
from .core.penpa import Puzzle, Solution
from .core.helper import full_bfs
from .core.neighbor import adjacent
from .core.solution import solver


def magnet_constraint() -> str:
    """Generate the magnet constraint."""
    constraint = ":- math_G__2__0(R, C), math_G__2__0(R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__3__0(R, C), math_G__3__0(R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__2__0(R, C), area(A, R, C), not math_G__3__0(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__3__0(R, C), area(A, R, C), not math_G__2__0(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- gray(R, C), area(A, R, C), not gray(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    return constraint.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_cc(["math_G__2__0", "math_G__3__0", "gray"]))
    solver.add_program_line(adjacent())

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        assert len(ar) == 2, "All regions must be of size 2."
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__2__0", _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "BOTTOM clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__2__0", _type="row", _id=r))

    for (r, c), num in filter(lambda x: x[0][0] == puzzle.row and x[0][1] >= 0, puzzle.text.items()):  # filter bottom number
        assert isinstance(num, int), "LEFT clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__3__0", _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == puzzle.col and x[0][0] >= 0, puzzle.text.items()):  # filter right number
        assert isinstance(num, int), "RIGHT clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__3__0", _type="row", _id=r))

    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name in ("math_G__2__0", "math_G__3__0"):
            solver.add_program_line(f"{symbol_name}({r}, {c}).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")

    solver.add_program_line(magnet_constraint())
    solver.add_program_line(display(item="math_G__2__0"))
    solver.add_program_line(display(item="math_G__3__0"))
    solver.add_program_line(display(item="gray"))
    solver.solve()
    return solver.solutions
