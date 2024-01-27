"""The Lits solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.regions import full_bfs
from .utilsx.rules import (
    area_adjacent,
    adjacent,
    area,
    avoid_rect,
    connected,
    count,
    display,
    grid,
    omino,
    shade_c,
)
from .utilsx.solutions import solver


def valid_omino(num: int = 4, color: str = "black"):
    """
    Generates a rule for a valid omino.

    A grid rule or an area rule should be defined first.
    """

    count_valid = (
        f"#count {{ R, C : area(A, R, C), {color}(R, C), omino_{num}(T, V, DR, DC), R = AR + DR, C = AC + DC }} = {num}"
    )
    return f"valid_omino_{num}(A, T, AR, AC) :- area(A, AR, AC), omino_{num}(T, V, _, _), {count_valid}."


def avoid_adjacent_same_omino(num: int = 4, color: str = "black", adj_type: int = 4) -> None:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An area adjacent rule, an omino rule should be defined first.
    """
    return (
        f":- area_adj_{adj_type}_{color}(A, A1), A < A1, "
        + f"valid_omino_{num}(A, T, _, _), valid_omino_{num}(A1, T1, _, _), T = T1."
    )


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def solve(E: Encoding) -> List:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(omino(4, ["L", "I", "T", "S"]))
    solver.add_program_line(shade_c("darkgray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(connected(color="darkgray"))
    solver.add_program_line(avoid_rect(2, 2, color="darkgray"))

    areas = full_bfs(E.R, E.C, E.edges)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(4, color="darkgray", _type="area", _id=i))

    solver.add_program_line(connected(color="darkgray", _type="area"))
    solver.add_program_line(valid_omino(4, color="darkgray"))
    solver.add_program_line(area_adjacent(color="darkgray"))
    solver.add_program_line(avoid_adjacent_same_omino(4, color="darkgray"))

    for (r, c), clue in E.clues.items():
        if clue == "darkgray":
            solver.add_program_line(f"darkgray({r}, {c}).")
        elif clue == "green":
            solver.add_program_line(f"not darkgray({r}, {c}).")

    solver.add_program_line(display(color="darkgray"))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
