"""The N Cell solver."""

from typing import List

from . import utilsx
from .utilsx.encoding import Encoding
from .utilsx.fact import display, grid
from .utilsx.rule import (
    adjacent,
    connected,
    connected_parts,
    count_connected_parts,
    rev_op_dict,
)
from .utilsx.helper import tag_encode
from .utilsx.solution import solver


def encode(string: str) -> Encoding:
    return utilsx.encode(string, has_borders=True)


def fill_num(low: int, high: int) -> str:
    """
    Generate a rule that a cell numbered between low and high.
    """
    num = f"num({low}..{high}).\n"
    num += f"1 {{ number(R, C, N): num(N) }} 1 :- grid(R, C)."
    return num


def order_region() -> str:
    """
    Make sure region id is ordered, to avoid duplicate.
    """
    constriant = ":- num(N1), num(N2), N1<N2, #min{ (R, C): number(R, C, N1) } = (R1, C1), #min{ (R, C): number(R, C, N2) } = (R2, C2), (R1, C1) >= (R2, C2)."
    return constriant


def count_number(target: int, op: str = "eq") -> str:
    """
    Generates a constraint for counting the number in a grid.
    A grid fact should be defined first.
    """
    op = rev_op_dict[op]
    return f":- num(N), #count {{ R, C: number(R, C, N) }} {op} {target}."


def connected_number(adj_type: int = 4) -> str:
    """
    Generate a rule to get all the connected components of {color} cells.
    """
    adj = tag_encode("adj", adj_type)
    constraint = "reachable(R, C, R1, C1) :- grid(R, C), grid(R1, C1), R = R1, C = C1.\n"
    constraint += f"reachable(R, C, R1, C1) :- grid(R, C), reachable(R, C, R2, C2), {adj}(R2, C2, R1, C1), num(N), number(R, C, N), number(R2, C2, N), number(R1, C1, N).\n"
    constraint += ":- num(N), number(R, C, N), number(R1, C1, N), not reachable(R, C, R1, C1)."
    return constraint


def num_same_adj(r: int, c: int, number: int, adj_type: int = 4) -> str:
    adj = tag_encode("adj", adj_type)
    return f":- #count{{ R, C: {adj}({r}, {c}, R, C), num(N), number({r}, {c}, N), number(R, C, N) }} != {number}."


def display_region() -> str:
    """Generates a rule to show region ids."""
    return "#show number/3."


def solve(E: Encoding) -> List:
    size = int(E.params["region_size"])
    assert E.R * E.C % size == 0, "It's impossible to divide grid into regions of this size!"
    region_num = E.R * E.C // size

    solver.reset(mode="region", R=E.R, C=E.C)
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(fill_num(0, region_num - 1))
    solver.add_program_line(order_region())
    solver.add_program_line(adjacent())
    solver.add_program_line(count_number(region_num))
    solver.add_program_line(connected_number())

    for (r, c), clue in E.clues.items():
        solver.add_program_line(num_same_adj(r, c, 4 - clue))

    solver.add_program_line(display_region())
    # print(solver.program)
    solver.solve()
    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
