"""The Pentominous solver."""

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
    assert (puzzle.row * puzzle.col - shaded) % 5 == 0, "The grid cannot be divided into 5-ominoes!"

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
    for i, (o_name, o_shape) in enumerate(OMINOES[5].items()):
        shape_dict[o_name] = i
        solver.add_program_line(general_shape("omino_5", i, o_shape, color="grid", adj_type="edge"))

    for (r, c), shape_name in puzzle.text.items():
        assert shape_name in shape_dict, f"Shape {shape_name} is not defined!"
        t_be = tag_encode("belong_to_shape", "omino_5", "grid")
        solver.add_program_line(f":- not {t_be}({r}, {c}, {shape_dict[shape_name]}, _).")

    for r, c, d in puzzle.edge:
        solver.add_program_line(f":- not edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    solver.add_program_line(all_shapes("omino_5", color="grid"))
    solver.add_program_line(avoid_adj_same_omino(omino_num=5, color="grid"))
    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Pentominous",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VRRb9owEH7nV1T37Ic4DsHJG+tgmsRoN+gYsyIUaLqigdKFZpqM+O+9O4cmk4jWqVqnSVPw+fN3F/z5nLvdtzItMiE9+iktcMYnkJqHr0MeXvVM1/ebLD4T/fL+Ni8QCHExHIqbdLPLOqaKSjp7G8W2L+yb2IAEAT4OCYmw7+O9fRfbibATdIEIkBu5IB/hoIYz9hM6d6T0EI8rjHCOcLUuVptsMXLMZWzsVADt84rfJgjb/HsGlQ5ar/Ltck3EMr3Hw+xu13eVZ1de51/LKlYmB2H7Tu7ghFxVyyXo5BI6IZdO8YflRsnhgGn/gIIXsSHtVzXUNZzEe+iFEAcCtHZTxFPk8SS9AGcMHGOg8unfxyjXXR8oRcSsQeBfGbhsED0iPtaE5ohhTURdIt7WhPRwawPzJoOaDEwbTBfFGrhqMhzzucGELJey+8iw3k9HBo8l4z3aOdshW5/tFNMjrGL7mq3Htst2xDEDtjO252wDtiHH9CjBT7wCl9/ny4Gwh1mItIBQYxIdkEeA6SDga4k1jAuFWAbC9zGXjLG+6YoJR57wI3wTsQoCoSjfjLEpdPGTUL88uVGudfz8dP89LukYmJTFTbrKsNIG11+ys3FebNMNrsbldpkVxzU2ukMHfgAPo6hv/u99f6n30RV4L1x+z+0GBrP7WJ7CXgi4KxfpYpXjp4YpdO6qYlvdrojb3FVdt7iPpd7qdtV/2h32gt90BGHbG9pvc8g2h9e2efT0zV/8e8A2mXQeAA==",
        }
    ],
}
