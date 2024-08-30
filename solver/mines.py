"""The sun_moon__4__0sweeper solver."""

from typing import List

from .core.common import count, display, grid, shade_c
from .core.penpa import Puzzle, Solution
from .core.neighbor import adjacent, count_adjacent
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    mine_count = puzzle.param["mine_count"]

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="sun_moon__4__0"))
    solver.add_program_line(adjacent(_type=8))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"sun_moon__4__0({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not sun_moon__4__0({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(f"not sun_moon__4__0({r}, {c}).")
        solver.add_program_line(count_adjacent(num, (r, c), color="sun_moon__4__0", adj_type=8))

    if mine_count:
        assert isinstance(mine_count, str) and mine_count.isdigit(), "Please provide a valid mine count."
        solver.add_program_line(count(int(mine_count), color="sun_moon__4__0", _type="grid"))

    solver.add_program_line(display(item="sun_moon__4__0"))
    solver.solve()

    return solver.solutions
