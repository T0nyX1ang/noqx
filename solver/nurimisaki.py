"""The Nurimisaki solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import (
    bulb_src_color_connected,
    count_reachable_src,
    grid_color_connected,
)
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def avoid_unknown_misaki(known_cells: List[Tuple[int, int]], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to avoid dead ends that does not have a record.

    A grid rule and an adjacent rule should be defined first.
    """

    included = ", ".join(f"|R - {src_r}| + |C - {src_c}| != 0" for src_r, src_c in known_cells)
    main = f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} = 1"

    if not known_cells:
        return f"{main}."
    return f"{main}, {included}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not black"))
    solver.add_program_line(avoid_rect(2, 2, color="black"))
    solver.add_program_line(avoid_rect(2, 2, color="not black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    all_src: List[Tuple[int, int]] = []
    for (r, c), num in puzzle.text.items():
        solver.add_program_line(f"not black({r}, {c}).")
        solver.add_program_line(count_adjacent(1, (r, c), color="not black"))
        all_src.append((r, c))

        if isinstance(num, int):
            solver.add_program_line(bulb_src_color_connected((r, c), color="not black"))
            solver.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black"))

    solver.add_program_line(avoid_unknown_misaki(all_src, color="not black"))
    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Nurimisaki",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VRNb5tAEL3zK6w5z4Fl+fLe3DTuxaUfuIoihCJMiYICJQVTVWvx3zM7ICETX3poFFUV3qe3b2aXt4N3up991hYohPnJEG0khq7n8xDC4WFPz748VoVa4aY/PjQtEcRP2y3eZ1VXWMmUlVonvVZ6g/qDSkAAgkNDQIr6izrpj0pHqGMKAbqk7cYkh+j1TG84btjVKAqbeDRyn+gt0bxs86q421GUlM8q0XsE8553vNpQqJtfBUw+zDxv6kNphEN2pMN0D+XTFOn6781jP+WKdEC9Ge3GF+zK2a6ho13D/prd6qm5ZHSdDgMV/CtZvVOJcf1tpuFMY3UijNQJZEBLffTHbwKeTVM5T12z8YpcT0KwPouH3iIuxHKFcOQLxbxz3kRIsczwTMaZ4i/WBC8ywnOFzif4lLeMW0aHcU9FQC0Z3zPajB7jjnOuGW8YrxhdRp9zAlPGPyr0K9hJJN3PC4/376qplUDct/dZXtB1iPr6ULSrqGnrrALqPIMFv4EH/XWokf1vRq/ejEzx7bd2U96aHbq78KNvy7rssscSUusZ",
        },
        {
            "url": "https://puzz.link/p?nurimisaki/15/15/v.h.h.h.h.zr.j.h.i.zk.l.q.m.j.l.r.i.i.i.zr.h.h.h.h.v",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?nurimisaki/22/15/j.zj3j.h.v.n.g..k3q4z4l.l2w3n4h.u5g3o3k.m.h.g4u.p.k3h.j.p3n.i3k.t.u4o.h3h.g3r4",
            "test": False,
        },
    ],
}
