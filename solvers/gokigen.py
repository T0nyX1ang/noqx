"""The Gokigen solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import fill_path
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, clue_encoder=lambda s: s)


def slant_conn() -> str:
    rule = ':- grid(R, C), grid_direction(R, C, "ul"), not grid_direction(R-1, C-1, "dr").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "ur"), not grid_direction(R-1, C+1, "dl").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "dl"), not grid_direction(R+1, C-1, "ur").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "dr"), not grid_direction(R+1, C+1, "ul").\n'

    rule += "grid_direc_num(R, C, D, 0) :- grid(R, C), direction(D), not grid_direction(R, C, D).\n"
    rule += "grid_direc_num(R, C, D, 1) :- grid_direction(R, C, D).\n"
    rule += 'slant_code(R, C, N0 + N1*2 + N2*4 + N3*8) :- grid_direc_num(R, C, "ul", N0), grid_direc_num(R, C, "ur", N1), grid_direc_num(R, C, "dl", N2), grid_direc_num(R, C, "dr", N3).\n'
    return rule.strip()


def slant_fill_each() -> str:
    return ':- grid(R, C), grid(R+1, C+1), { grid_direction(R, C, "dr"); grid_direction(R, C+1, "dl") } != 1.'


def no_loop() -> str:
    rule = "reachable(R, C) :- grid(R, C), not grid(R-1, C-1).\n"
    rule += "reachable(R, C) :- grid(R, C), not grid(R+1, C+1).\n"
    rule += 'reachable(R, C) :- grid(R, C), reachable(R-1, C-1), not grid_direction(R, C-1, "ur").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R-1, C+1), not grid_direction(R, C+1, "ul").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R+1, C-1), not grid_direction(R, C-1, "dr").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R+1, C+1), not grid_direction(R, C+1, "dl").\n'
    rule += ":- grid(R, C), not reachable(R, C).\n"
    return rule.strip()


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction(["ul", "ur", "dl", "dr"]))
    solver.add_program_line(fill_path(color="grid"))
    solver.add_program_line(slant_conn())
    solver.add_program_line(slant_fill_each())
    solver.add_program_line(no_loop())

    for (r, c), clue in E.clues.items():
        solver.add_program_line(f":- #count{{ D: grid_direction({r}, {c}, D) }} != {clue}.")

    solver.add_program_line(display(item="slant_code", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
