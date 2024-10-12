"""The Slitherlink solver."""

from typing import List

from .core.common import direction, display, fill_path, grid, shade_c
from .core.loop import separate_item_from_loop, single_loop
from .core.neighbor import adjacent, count_adjacent_edges
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.solution import solver


def convert_direction_to_edge() -> str:
    """Convert grid direction fact to edge fact."""
    rule = 'edge_top(R, C) :- grid_direction(R, C, "r").\n'
    rule += 'edge_left(R, C) :- grid_direction(R, C, "d").\n'
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="slither"))
    solver.add_program_line(fill_path(color="slither"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="slither", adj_type="loop"))
    solver.add_program_line(single_loop(color="slither"))
    solver.add_program_line(convert_direction_to_edge())
    solver.add_program_line(adjacent(_type="edge"))

    flag = False
    for (r, c), clue in puzzle.text.items():
        if clue == "W":
            flag = True
            solver.add_program_line(f"wolf({r}, {c}).")
        elif clue == "S":
            flag = True
            solver.add_program_line(f"sheep({r}, {c}).")
        else:
            assert isinstance(clue, int), "Clue should be an integer or wolf/sheep."
            solver.add_program_line(count_adjacent_edges(int(clue), (r, c)))

    if flag:
        solver.add_program_line(separate_item_from_loop(inside_item="sheep", outside_item="wolf"))

    solver.add_program_line(display(item="edge_top", size=2))
    solver.add_program_line(display(item="edge_left", size=2))
    solver.solve()

    return solver.solutions
