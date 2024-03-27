"""The Hotaru Beam solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import fill_path, directed_loop, connected_loop
from .utilsx.rule import adjacent
from .utilsx.solution import solver

drdc = {"l": (0, -1), "r": (0, 1), "u": (-1, 0), "d": (1, 0)}


def restrict_num_bend(r: int, c: int, num: int, color: str) -> str:
    """
    Generate a rule to restrict the number of bends in the path.

    A grid_in/grid_out rule should be defined first.
    """
    rule = "adj_loop(R, C, R1, C1) :- adj_loop(R1, C1, R, C)."  # ensure symmetry
    rule += f"reachable({r}, {c}, {r}, {c}).\n"
    rule += f"reachable({r}, {c}, R, C) :- {color}(R, C), grid(R1, C1), reachable({r}, {c}, R1, C1), adj_loop(R1, C1, R, C).\n"
    rule += f'bend(R, C) :- {color}(R, C), grid_in(R, C, "l"), not grid_out(R, C, "r").\n'
    rule += f'bend(R, C) :- {color}(R, C), grid_in(R, C, "u"), not grid_out(R, C, "d").\n'
    rule += f'bend(R, C) :- {color}(R, C), grid_in(R, C, "r"), not grid_out(R, C, "l").\n'
    rule += f'bend(R, C) :- {color}(R, C), grid_in(R, C, "d"), not grid_out(R, C, "u").\n'
    rule += f":- #count{{ R, C: grid(R, C), reachable({r}, {c}, R, C), bend(R, C) }} != {num}.\n"

    rule += "hotaru_all(R, C) :- hotaru(R, C).\n"
    rule += "hotaru_all(R, C) :- dead_end(R, C).\n"
    return rule


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ hotaru(R, C) } :- grid(R, C), not dead_end(R, C).")
    solver.add_program_line(fill_path(color="hotaru", directed=True))
    solver.add_program_line(adjacent(_type="loop_directed"))
    solver.add_program_line(directed_loop(color="hotaru"))
    solver.add_program_line(connected_loop(color="hotaru_all"))

    for (r, c), clue in E.clues.items():
        if isinstance(clue, list):
            num = int(clue[0])
            clue = clue[1]
            dr, dc = drdc[clue]
            solver.add_program_line(restrict_num_bend(r + dr, c + dc, num, color="hotaru"))
        solver.add_program_line(f"dead_end({r}, {c}).")
        solver.add_program_line(f'grid_out({r}, {c}, "{clue}").')
        solver.add_program_line(f'{{ grid_in({r}, {c}, D) }} :- direction(D), D != "{clue}".')

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
