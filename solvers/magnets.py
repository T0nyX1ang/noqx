"""The Magnets solver."""

from typing import List

from . import utilsx
from .utilsx.common import area, count, display, grid, shade_cc
from .utilsx.encoding import Encoding
from .utilsx.helper import full_bfs
from .utilsx.rule import adjacent
from .utilsx.solution import solver


def magnet_constraint() -> str:
    """Generate the magnet constraint."""
    constraint = ":- red(R, C), red(R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- blue(R, C), blue(R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- red(R, C), area(A, R, C), not blue(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- blue(R, C), area(A, R, C), not red(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- gray(R, C), area(A, R, C), not gray(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    return constraint.strip()


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(shade_cc(["red", "blue", "gray"]))
    solver.add_program_line(adjacent(4))

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        assert len(ar) == 2, "All regions must be of size 2."
        solver.add_program_line(area(_id=i, src_cells=ar))

    for c, num in E.top.items():
        solver.add_program_line(count(int(num), color="red", _type="col", _id=c))

    for r, num in E.left.items():
        solver.add_program_line(count(int(num), color="red", _type="row", _id=r))

    for c, num in E.bottom.items():
        solver.add_program_line(count(int(num), color="blue", _type="col", _id=c))

    for r, num in E.right.items():
        solver.add_program_line(count(int(num), color="blue", _type="row", _id=r))

    for (r, c), clue in E.clues.items():
        if clue in ["red", "blue", "gray"]:
            solver.add_program_line(f"{clue}({r}, {c}).")

    solver.add_program_line(magnet_constraint())
    solver.add_program_line(display(item="red"))
    solver.add_program_line(display(item="blue"))
    solver.solve()
    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
