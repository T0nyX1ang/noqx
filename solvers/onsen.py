"""The Onsen solver."""

from typing import List, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid, area
from .utilsx.loop import single_loop, fill_path
from .utilsx.rule import adjacent
from .utilsx.region import full_bfs
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def onsen(id: int, r: int, c: int, num: int) -> str:
    rule = f"onsen({id}, {r}, {c}).\n"
    rule += f"onsen({id}, R, C) :- grid(R, C), adj_loop(R, C, R1, C1), onsen({id}, R1, C1).\n"
    rule += f":- area(A, R, C), onsen({id}, R, C), #count{{ R1, C1: area(A, R1, C1), onsen({id}, R1, C1) }} != {num}."

    rule += f":- area(A, _, _), #count{{ R, C, D: grid(R, C), area_border(A, R, C, D), grid_direction(R, C, D) }} < 2.\n"
    rule += f":- area(A, _, _), onsen(ID, _, _), #count{{ R, C, D: onsen(ID, R, C), area_border(A, R, C, D), grid_direction(R, C, D) }} > 2."
    return rule.strip()


def area_border(id: int, ar: list) -> str:
    borders = []
    for r, c in ar:
        for dr, dc, direc in ((0, -1, "l"), (-1, 0, "u"), (0, 1, "r"), (1, 0, "d")):
            r1, c1 = r + dr, c + dc
            if (r1, c1) not in ar:
                borders.append(f'area_border({id}, {r}, {c}, "{direc}").')
    rule = "\n".join(borders)
    return rule


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ onsen_loop(R, C) } :- grid(R, C).")
    solver.add_program_line(fill_path(color="onsen_loop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(single_loop(color="onsen_loop", visit_all=True))

    for id, ((r, c), clue) in enumerate(E.clues.items()):
        solver.add_program_line(onsen(id, r, c, clue))
    solver.add_program_line(":- grid(R, C), onsen_loop(R, C), not onsen(_, R, C).")

    areas = full_bfs(E.R, E.C, E.edges)
    for id, ar in enumerate(areas):
        solver.add_program_line(area(_id=id, src_cells=ar))
        solver.add_program_line(area_border(id, ar))

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
