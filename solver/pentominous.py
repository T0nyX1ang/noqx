"""The Pentominous solver."""

from typing import List

from noqx.puzzle import Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
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


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    shaded = len(puzzle.surface)
    assert (puzzle.row * puzzle.col - shaded) % 5 == 0, "The grid cannot be divided into 5-ominoes!"

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="hole"))
    solver.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_shapes("omino_5", color="grid"))
    solver.add_program_line(avoid_adj_same_omino(omino_num=5, color="grid"))

    for (r, c, _, _), color in puzzle.surface.items():
        solver.add_program_line(f"hole({r}, {c}).")

        for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
            prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
            direc = "left" if c1 != c else "top"
            solver.add_program_line(f"{prefix}edge_{direc}({r2}, {c2}).")

    shape_dict = {}
    for i, (o_name, o_shape) in enumerate(OMINOES[5].items()):
        shape_dict[o_name] = i
        solver.add_program_line(general_shape("omino_5", i, o_shape, color="grid", adj_type="edge"))

    for (r, c, d, pos), shape_name in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        assert shape_name in shape_dict, f"Shape {shape_name} is not defined!"
        t_be = tag_encode("belong_to_shape", "omino_5", "grid")
        solver.add_program_line(f":- not {t_be}({r}, {c}, {shape_dict[shape_name]}, _).")

    for (r, c, d, _), draw in puzzle.edge.items():
        assert d is not None, f"Direction in ({r}, {c}) is not defined."
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Pentominous",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VRRb9owEH7nV1T3fA9xHIKTN9bBNInRbtAxZkUo0HRFA6ULzTQZ8d97Pocmk4jWqVqnSVPw+fN3Z/L5nLvdtzItMhSe/UmFNNMTCMXDVyEPr3qm6/tNFp9hv7y/zQsCiBfDId6km13W0VVU0tmbKDZ9NG9iDT4gDwEJmvfx3ryLzQTNhFyAAXEjQgLQJzio4Yz9Fp07UniExxUmOCe4WherTbYYOeYy1maKYN/zindbCNv8ewZuG69X+Xa5tsQyvafD7G7Xd5VnV17nX8sqViQHNH0nd3BCrqzlWujkWnRCrj3FH5YbJYcDpf0DCV7E2mq/qqGq4STeQy+EOEBQyk0RT5HHk/ACmilwTIHSt/8+Jrnu+kBKS8waBP2VhssG0bPEx5pQHDGsiahribc1ITx6tYZ5kyFNGqYNpktiNVw1GY753GBClmuz+8iw3k9Hho4l4j3ZOdshW5/tlNKDRrJ9zdZj22U74pgB2xnbc7YB25BjejbBT7wCl9/ny4GwR1mIFEKoKIkOiCOgdFjgK0E1TAtJWATo+5RLxlTf9ootjjz0I9pJWAYBSptvxtQUuvRJyF+eXEvXOn5+uv8el3Q0TMriJl1lVGmD6y/Z2TgvtumGVuNyu8yK45oa3aEDP4CHlrZv/u99f6n32SvwXrj8ntsNNGX3sTzRXCDclYt0scrpU6MUOndVsa1uV8Rt7qquW9zHUm91u+o/7Q57wW86grBth/LbHKLN4bW9PHr6y1/8e6A2mXQeAA==",
        }
    ],
}
