"""The Simple Loop solver."""

from typing import List

from .core.common import direction, display, fill_path, grid
from .core.helper import tag_encode
from .core.loop import intersect_loop
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def adjacent_loop_intersect() -> str:
    """
    Generate a constraint to check adjacent loop intersection.

    An intersect_loop rule should be defined first.
    """
    adj = 'direction_type("H"; "V").\n'
    adj += 'adj_loop_intersect(R, C, "H", R, C, "V") :- grid(R, C), not intersection(R, C).\n'
    adj += 'adj_loop_intersect(R, C, "H", R, C + 1, "H") :- grid(R, C), grid(R, C+1), grid_direction(R, C, "r").\n'
    adj += 'adj_loop_intersect(R, C, "V", R + 1, C, "V") :- grid(R, C), grid(R+1, C), grid_direction(R, C, "d").\n'
    adj += "adj_loop_intersect(R0, C0, T0, R, C, T) :- adj_loop_intersect(R, C, T, R0, C0, T0)."
    return adj


def loop_intersect_connected(color: str = "black") -> str:
    """Generate a constraint to check the reachability of {color} cells connected to loops."""
    tag = tag_encode("reachable", "grid", "adj", "loop", "intersection", color)
    rule = f'{tag}(R, C, "H") :- (R, C) = #min{{ (R1, C1): grid(R1, C1), {color}(R1, C1) }}.\n'
    rule += f"{tag}(R, C, T) :- {tag}(R1, C1, T1), grid(R, C), {color}(R, C), adj_loop_intersect(R, C, T, R1, C1, T1).\n"
    rule += f":- grid(R, C), {color}(R, C), direction_type(T), not {tag}(R, C, T).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("pipelink(R, C) :- grid(R, C).")
    solver.add_program_line(fill_path(color="pipelink"))
    solver.add_program_line(intersect_loop(color="pipelink"))
    solver.add_program_line(adjacent_loop_intersect())
    solver.add_program_line(loop_intersect_connected(color="pipelink"))

    for r, c, _ in puzzle.line:
        for d in "lurd":
            if (r, c, d) in puzzle.line:
                solver.add_program_line(f'grid_direction({r}, {c}, "{d}").')
            else:
                solver.add_program_line(f'not grid_direction({r}, {c}, "{d}").')

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions
