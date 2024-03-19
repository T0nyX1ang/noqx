"""The Nagare solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import direction, display, grid
from .utilsx.loop import fill_path, connected_loop, directed_loop
from .utilsx.rule import adjacent, shade_c
from .utilsx.solution import solver

rev_direction = {"l": "r", "r": "l", "u": "d", "d": "u"}


def nagare_wind(r: int, c: int, d: str, E: Encoding) -> str:
    d = d.lower()
    clues = E.clues
    if d in "lr":
        cols = range(0, c) if d == "l" else range(E.C - 1, c, -1)
        c1, c2 = cols[0], cols[-1]
        for c_ in cols:
            if clues.get((r, c_)):
                c1 = c_ + cols.step
        if d == "r":
            c1, c2 = c2, c1
        return (
            f':- nagare({r}, C), {c1} <= C, C <= {c2}, not grid_out({r}, C, "{d}"), not grid_in({r}, C, "{rev_direction[d]}").'
        )
    else:
        rows = range(0, r) if d == "u" else range(E.R - 1, r, -1)
        r1, r2 = rows[0], rows[-1]
        for r_ in rows:
            if clues.get((r_, c)):
                r1 = r_ + rows.step
        if d == "d":
            r1, r2 = r2, r1
        return (
            f':- nagare(R, {c}), {r1} <= R, R <= {r2}, not grid_out(R, {c}, "{d}"), not grid_in(R, {c}, "{rev_direction[d]}").'
        )


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="nagare"))
    solver.add_program_line(fill_path(color="nagare", directed=True))
    solver.add_program_line(adjacent(_type="loop_directed"))
    solver.add_program_line(connected_loop(color="nagare"))
    solver.add_program_line(directed_loop(color="nagare"))

    for (r, c), clue in E.clues.items():
        if clue in "lurd":
            solver.add_program_line(f"nagare({r}, {c}).")
            solver.add_program_line(f'grid_in({r}, {c}, "{rev_direction[clue]}").')
            solver.add_program_line(f'grid_out({r}, {c}, "{clue}").')
        elif clue in "LURD":
            solver.add_program_line(f"not nagare({r}, {c}).")
            solver.add_program_line(nagare_wind(r, c, clue, E))
        else:
            # clue == "black"
            solver.add_program_line(f"not nagare({r}, {c}).")

    solver.add_program_line(display(item="loop_sign", size=3))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
