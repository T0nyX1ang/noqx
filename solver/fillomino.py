"""Solve Fillomino puzzles."""

from typing import Dict, List

from .core.common import display, edge, grid, direction
from .core.encoding import Encoding
from .core.neighbor import adjacent
from .core.solution import solver


def fillomino_rules(fast: bool = True):
    """Generate the Fillomino constraints."""

    # propagation of number
    rule = "number(R, C, N) :- grid(R, C), num(N), adj_edge(R0, C0, R, C), number(R0, C0, N).\n"
    # rule = "number(RT, CT, N) :- grid(R, C), num(N), region_id(R, C, RT, CT), number(R, C, N).\n"
    # rule += "number(R, C, N) :- grid(R, C), num(N), region_id(R, C, RT, CT), number(RT, CT, N).\n"
    rule += "numberx(R, C, N) :- grid(R, C), num(N), number(R, C, N).\n"
    rule += ":- grid(R, C), num(N1), num(N2), N1<N2, numberx(R, C, N1), numberx(R, C, N2).\n"
    if fast:
        rule += "num_small(1..5).\n"
        rule += "{ numberx(R, C, N) : num_small(N) } = 1 :- grid(R, C), not number(R, C, _).\n"
    else:
        rule += "{ numberx(R, C, N) : num(N) } = 1 :- grid(R, C), not number(R, C, _).\n"

    # same number, adjacent cell, no line
    rule += ":- numberx(R, C, N), numberx(R, C + 1, N), vertical_line(R, C + 1).\n"
    rule += ":- numberx(R, C, N), numberx(R + 1, C, N), horizontal_line(R + 1, C).\n"

    # different number, adjacent cell, have line
    rule += ":- numberx(R, C, N1), numberx(R, C + 1, N2), N1 != N2, not vertical_line(R, C + 1).\n"
    rule += ":- numberx(R, C, N1), numberx(R + 1, C, N2), N1 != N2, not horizontal_line(R + 1, C).\n"

    # special case for 1
    mutual = ["horizontal_line(R, C)", "horizontal_line(R + 1, C)", "vertical_line(R, C)", "vertical_line(R, C + 1)"]
    rule += f"{{ {'; '.join(mutual)} }} = 4 :- numberx(R, C, 1).\n"
    rule += f"numberx(R, C, 1) :- {', '.join(mutual)}.\n"
    rule += ":- numberx(R, C, 1), numberx(R1, C1, 1), adj_4(R, C, R1, C1).\n"

    return rule.strip()


def fillomino_tree():
    rule = "{ fa(R, C, D) : direction(D) } = 1 :- grid(R, C).\n"
    rule += ':- vertical_line(R, C), fa(R, C, "l").\n'
    rule += ':- vertical_line(R, C+1), fa(R, C, "r").\n'
    rule += ':- horizontal_line(R, C), fa(R, C, "u").\n'
    rule += ':- horizontal_line(R+1, C), fa(R, C, "d").\n'

    rule += 'region_id(R, C, R, C) :- grid(R, C), fa(R, C, ".").\n'
    rule += 'region_id(R, C, RT, CT) :- grid(R, C), grid(RT, CT), fa(R, C, "l"), region_id(R, C-1, RT, CT).\n'
    rule += 'region_id(R, C, RT, CT) :- grid(R, C), grid(RT, CT), fa(R, C, "r"), region_id(R, C+1, RT, CT).\n'
    rule += 'region_id(R, C, RT, CT) :- grid(R, C), grid(RT, CT), fa(R, C, "u"), region_id(R-1, C, RT, CT).\n'
    rule += 'region_id(R, C, RT, CT) :- grid(R, C), grid(RT, CT), fa(R, C, "d"), region_id(R+1, C, RT, CT).\n'
    rule += ":- grid(R, C), #count{ RT, CT: grid(RT, CT), region_id(R, C, RT, CT) } != 1.\n"
    rule += ":- grid(R, C), region_id(R, C, R1, C1), (R, C) < (R1, C1).\n"
    rule += ":- grid(R, C), adj_edge(R, C, R1, C1), region_id(R, C, RT, CT), not region_id(R1, C1, RT, CT).\n"

    rule += 'size_to(R, C, D, N) :- grid(R, C), direction(D), D != ".", num(N), fa(R, C, D), size(R, C, N).\n'
    rule += 'size_to(R, C, ".", 0) :- grid(R, C).\n'
    rule += "size_to(R, C, D, 0) :- grid(R, C), direction(D), num(N), not fa(R, C, D).\n"
    rule += "size_to(R, C, D, 0) :- grid_big(R, C), not grid(R, C), direction(D).\n"
    rule += 'size(R, C, N1+N2+N3+N4+1) :- num(N1), num(N2), num(N3), num(N4), num(N1+N2+N3+N4+1), size_to(R, C+1, "l", N1), size_to(R, C-1, "r", N2), size_to(R+1, C, "u", N3), size_to(R-1, C, "d", N4).\n'
    rule += ":- grid(R, C), num(N1), num(N2), N1<N2, size(R, C, N1), size(R, C, N2).\n"
    rule += ":- grid(R, C), not size(R, C, _).\n"
    # rule += ":- grid(R, C), #count{ N: num(N), size(R, C, N) } != 1.\n"
    rule += ':- fa(R, C, "."), size(R, C, N), not numberx(R, C, N).\n'
    rule += ':- fa(R, C, "."), numberx(R, C, N), not size(R, C, N).\n'
    rule += ":- grid(R, C), numberx(R, C, N), size(R, C, N1), N<N1.\n"
    return rule.strip()


def solve(E: Encoding) -> List[Dict[str, str]]:
    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(f"grid_big(-1..{E.R}, -1..{E.C}).")
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(direction("lrud."))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(fillomino_rules())
    solver.add_program_line(fillomino_tree())

    mx_num = 5
    for (r, c), num in E.clues.items():
        solver.add_program_line(f"number({r}, {c}, {num}).")
        mx_num = max(mx_num, num)

        if num == 1:
            solver.add_program_line(f"vertical_line({r}, {c}).")
            solver.add_program_line(f"horizontal_line({r}, {c}).")
            solver.add_program_line(f"vertical_line({r}, {c + 1}).")
            solver.add_program_line(f"horizontal_line({r + 1}, {c}).")

    solver.add_program_line(f"num(0..{mx_num}).")
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    # solver.add_program_line(display(item="numberx", size=3))
    # solver.add_program_line(display(item="size", size=3))
    solver.add_program_line(display(item="fa", size=3))
    solver.solve()

    return solver.solutions
