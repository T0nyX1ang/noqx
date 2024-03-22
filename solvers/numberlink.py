"""The Numberlink solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import connected_path, fill_path, single_loop
from .utilsx.rule import adjacent, shade_c
from .utilsx.solution import solver


def no_2x2_path() -> str:
    """
    Generate a rule that no 2x2 path is allowed.

    A reachable path rule should be defined first
    """
    points = ((0, 0), (0, 1), (1, 0), (1, 1))
    return f":- { ', '.join(f'reachable_path(R0, C0, R + {r}, C + {c})' for r, c in points) }."


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    locations = {}
    for (r, c), n in E.clues.items():
        locations[n] = locations.get(n, []) + [(r, c)]

    # check that puzzle makes sense
    assert len(locations) > 0, "Error: The grid is empty!"
    for n, pair in locations.items():
        assert len(pair) <= 2, f"Error: There are more than two occurrences of {n}"
        assert len(pair) >= 2, f"Error: There is only one occurrence of {n}"

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))

    if E.params["visit_all"]:
        solver.add_program_line("numberlink(R, C) :- grid(R, C).")
    else:
        solver.add_program_line(shade_c(color="numberlink"))

    if E.params["no_2x2"]:
        solver.add_program_line(no_2x2_path())

    solver.add_program_line(fill_path(color="numberlink"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(single_loop(color="numberlink", path=True))

    for n, pair in locations.items():
        r0, c0 = pair[0]
        r1, c1 = pair[1]
        solver.add_program_line(f"numberlink({r0}, {c0}).")
        solver.add_program_line(f"numberlink({r1}, {c1}).")
        solver.add_program_line(connected_path((r0, c0), (r1, c1), color="numberlink"))

        for n1, pair1 in locations.items():
            if n1 != n:
                r10, c10 = pair1[0]
                r11, c11 = pair1[1]
                solver.add_program_line(f"not reachable_path({r0}, {c0}, {r10}, {c10}).")
                solver.add_program_line(f"not reachable_path({r0}, {c0}, {r11}, {c11}).")
                solver.add_program_line(f"not reachable_path({r1}, {c1}, {r10}, {c10}).")
                solver.add_program_line(f"not reachable_path({r1}, {c1}, {r11}, {c11}).")

    solver.add_program_line(":- grid(R, C), numberlink(R, C), not reachable_path(_, _, R, C).")
    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
