"""The Moon-or-Sun solver."""

from typing import List, Tuple

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid, area
from .utilsx.loop import single_loop, connected_loop, fill_path
from .utilsx.rule import adjacent, count
from .utilsx.region import full_bfs
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def moon_sun_area() -> str:
    rule = "{ sun_area(A) } :- area(A, _, _).\n"
    rule += ":- sun_area(A), area(A, R, C), sun(R, C), not moon_sun_loop(R, C).\n"
    rule += ":- sun_area(A), area(A, R, C), moon(R, C), moon_sun_loop(R, C).\n"
    rule += ":- not sun_area(A), area(A, R, C), sun(R, C), moon_sun_loop(R, C).\n"
    rule += ":- not sun_area(A), area(A, R, C), moon(R, C), not moon_sun_loop(R, C).\n"

    adj_diff = "adj_area(A1, A2) :- area(A1, R1, C1), area(A2, R2, C2), A1 < A2, adj_loop(R1, C1, R2, C2).\n"
    adj_diff += ":- adj_area(A1, A2), sun_area(A1), sun_area(A2).\n"
    adj_diff += ":- adj_area(A1, A2), not sun_area(A1), not sun_area(A2).\n"
    return (rule + adj_diff).strip()


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ moon_sun_loop(R, C) } :- grid(R, C).")
    solver.add_program_line(fill_path(color="moon_sun_loop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(connected_loop(color="moon_sun_loop"))
    solver.add_program_line(single_loop(color="moon_sun_loop", visit_all=True))

    for (r, c), clue in E.clues.items():
        _type = "sun" if clue == "s" else "moon"
        solver.add_program_line(f"{_type}({r}, {c}).")

    areas = full_bfs(E.R, E.C, E.edges)
    for id, ar in enumerate(areas):
        solver.add_program_line(area(_id=id, src_cells=ar))
        edges = []
        for r, c in ar:
            for dr, dc, direc in ((0, -1, "l"), (-1, 0, "u"), (0, 1, "r"), (1, 0, "d")):
                r1, c1 = r + dr, c + dc
                if (r1, c1) not in ar:
                    edges.append(f'grid_direction({r}, {c}, "{direc}")')
        edges = "; ".join(edges)
        solver.add_program_line(f":- {{ {edges} }} != 2.")

    solver.add_program_line(moon_sun_area())
    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
