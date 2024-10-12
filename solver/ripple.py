"""The Ripple Effect solver."""

from typing import List

from .core.common import area, display, fill_num, grid, unique_num
from .core.helper import full_bfs
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def ripple_constraint() -> str:
    """A constraint for the 'ripples'."""
    row = ":- grid(R, C1), grid(R, C2), number(R, C1, N), number(R, C2, N), (C2 - C1) * (C2 - C1 - N - 1) < 0."
    col = ":- grid(R1, C), grid(R2, C), number(R1, C, N), number(R2, C, N), (R2 - R1) * (R2 - R1 - N - 1) < 0."
    return row + "\n" + col


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))

    flag = False
    for (r, c), num in puzzle.text.items():
        if num == "?":
            solver.add_program_line(f"black({r}, {c}).")
            flag = True
            continue

        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if flag:
            solver.add_program_line(f"{{ number(R, C, (1..{len(ar)})) }} = 1 :- area({i}, R, C), not black(R, C).")
        else:
            solver.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i))

    solver.add_program_line(unique_num(color="not black" if flag else "grid", _type="area"))
    solver.add_program_line(ripple_constraint())
    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions
