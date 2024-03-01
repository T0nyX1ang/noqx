"""The Slitherlink solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import connected_loop, fill_path, single_loop
from .utilsx.rule import adjacent
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def slither_link() -> str:
    rule = ':- number(R, C, N), { grid_direction(R, C, "r"); grid_direction(R, C, "d"); grid_direction(R + 1, C, "r"); grid_direction(R, C + 1, "d") } != N.\n'
    rule += 'horizontal_line(R, C) :- grid_direction(R, C, "r").\n'
    rule += 'vertical_line(R, C) :- grid_direction(R, C, "d").\n'
    return rule.strip()


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R + 1, E.C + 1))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ slither_link(R, C) } :- grid(R, C).")
    solver.add_program_line(fill_path(color="slither_link"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="slither_link"))
    solver.add_program_line(single_loop(color="slither_link", visit_all=True))

    for (r, c), clue in E.clues.items():
        solver.add_program_line(f"number({r}, {c}, {clue}).")

    solver.add_program_line(slither_link())
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
