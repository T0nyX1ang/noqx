"""The Tetrominous solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, general_shape
from noqx.solution import solver


def avoid_adj_same_omino(omino_num: int = 4, color: str = "grid") -> str:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An split by edge rule, an omino rule should be defined first.
    """
    t_be = tag_encode("belong_to_shape", f"omino_{omino_num}", color)
    constraint = "split_by_edge(R, C, R + 1, C) :- grid(R, C), grid(R + 1, C), edge_top(R + 1, C).\n"
    constraint += "split_by_edge(R, C, R, C + 1) :- grid(R, C), grid(R, C + 1), edge_left(R, C + 1).\n"
    constraint += "split_by_edge(R, C, R1, C1) :- split_by_edge(R1, C1, R, C).\n"
    constraint += f":- grid(R, C), grid(R1, C1), {t_be}(R, C, T, _), {t_be}(R1, C1, T, _), split_by_edge(R, C, R1, C1)."
    return constraint


def solve(puzzle: Puzzle) -> List[Solution]:
    shaded = len(puzzle.surface)
    assert (puzzle.row * puzzle.col - shaded) % 4 == 0, "The grid cannot be divided into 4-ominoes!"

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="hole"))
    solver.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))

    for (r, c), color_code in puzzle.surface.items():
        solver.add_program_line(f"hole({r}, {c}).")

        for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
            prefix = "not " if ((r1, c1), color_code) in puzzle.surface.items() else ""
            direc = "left" if c1 != c else "top"
            solver.add_program_line(f"{prefix}edge_{direc}({r2}, {c2}).")

    shape_dict = {}
    for i, (o_name, o_shape) in enumerate(OMINOES[4].items()):
        shape_dict[o_name] = i
        solver.add_program_line(general_shape("omino_4", i, o_shape, color="grid", adj_type="edge"))

    for (r, c), shape_name in puzzle.text.items():
        assert shape_name in shape_dict, f"Shape {shape_name} is not defined!"
        t_be = tag_encode("belong_to_shape", "omino_4", "grid")
        solver.add_program_line(f":- not {t_be}({r}, {c}, {shape_dict[shape_name]}, _).")

    for r, c, d in puzzle.edge:
        solver.add_program_line(f":- not edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    solver.add_program_line(all_shapes("omino_4", color="grid"))
    solver.add_program_line(avoid_adj_same_omino(omino_num=4, color="grid"))
    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Tetrominous",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VNNb9pAEL37V0R7noM/FgN7oylUlahpC1UUWRYyjtOggpwaXFWL+O+8mTX1oVT9iJpeqtU+v30zmDfjnd3nJq9LirGiAfkUYIVxLDvQWrbfrsV6vynNFY2a/UNVgxDNJhO6zze70kvbrMw72KGxI7KvTKoCRSrEDlRG9p052DfGJmTnCCnS0KYuKQQdd/RG4syunRj44EnLQW9Bi3VdbMrl1ClvTWoXpPh/Xsivmapt9aVUrQ8+F9V2tWZhle9RzO5h/dhGds1d9alpc4PsSHbk7I4v2I06u0ydXWYX7HIVf9nuMDse0fb3MLw0KXv/0NFBR+fmoMJQGU0qcg/tHj1+ICHhBM1vncGm+2xK91l43Qlxj4V5J/TlJ1zZWZCMxVnAmwNzAN4KTgRDwQWckY0EXwr6gj3BqeSMBW8ErwW1YCw5fa7tF6t3JT7dDpqEpgwHqC7GjHD9EfOIcG45dG5U9FPraRjK2LnV+3OeefgqTX2fFyVuyfjuY3mVVPU23+CUNNtVWZ/PGNKjp74q2Slc43L/n9t/M7f8Cfxnvr9PHacU3f129cnOSD02y3xZVLhqaGEbdtPww7AbkMvhSMe/GcBEfhd49q5hmDPvBA==",
        }
    ],
}
