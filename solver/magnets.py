"""The Magnets solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.solution import solver


def magnet_constraint() -> str:
    """Generate the magnet constraint."""
    constraint = ":- math_G__2(R, C), math_G__2(R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__3(R, C), math_G__3(R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__2(R, C), area(A, R, C), not math_G__3(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__3(R, C), area(A, R, C), not math_G__2(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- gray(R, C), area(A, R, C), not gray(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    return constraint.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_cc(["math_G__2", "math_G__3", "gray"]))
    solver.add_program_line(adjacent())

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        assert len(ar) == 2, "All regions must be of size 2."
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__2", _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "BOTTOM clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__2", _type="row", _id=r))

    for (r, c), num in filter(lambda x: x[0][0] == puzzle.row and x[0][1] >= 0, puzzle.text.items()):  # filter bottom number
        assert isinstance(num, int), "LEFT clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__3", _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == puzzle.col and x[0][0] >= 0, puzzle.text.items()):  # filter right number
        assert isinstance(num, int), "RIGHT clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__3", _type="row", _id=r))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")

    solver.add_program_line(magnet_constraint())
    solver.add_program_line(display(item="math_G__2"))
    solver.add_program_line(display(item="math_G__3"))
    solver.add_program_line(display(item="gray"))
    solver.solve()
    return solver.solutions


__metadata__ = {
    "name": "Magnets",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7VZdj9pGFH3nV0Tz2qnkmbE9Y79tt2xftqQtW0UrCyFCnBR1qVNYqsor/nvOvb4D1GVDSNuNmlbg8fHhzv04d8bM+tfNbFVrk9DXBY07PqkJfNmQ85XI52Zxf1eXz/TF5v6nZgWg9fOrK/16dreuBxXNxGcyeGiLsr3Q7TdlpYzSyuIyaqLb78uH9tuyHep2jJ+UDuCuOyMLONzDF/w7ocuONAnwSDDgLeB8sZrf1dPrjvmurNobrSjOVzyboFo2v9VK8qDnebN8uSBiOXvzS32/Fnq9edX8vBFDM9nq9oJzFfsjCbt9wgS7hAkdSZjq+CcTLibbLVT/ASlPy4qy/3EPwx6OyweMo/JBOUtT0RjTtUa5lAh3QORRjUiE3pSUpxwQmSMi3RO+HyWYHmGSpBfXJEUvsLEc+ZBxvj8r62dncvb8B6afjsm5hF3GEMewRLc8XvFoebyBgrp1PH7NY8JjxuM12wwhrE0TbVOUabHuUwOMoIQttlPExGdZh7NM2xwlE85hs8MFth4EJRyctgVKJlxgS+6wB0bhjIN2pvPvjDnA2Nemy4d528XFXTvXxWJs0W/GOXDnH3ftpBb4g58uH9x3NhTXFpJzUWhHDSWbhOJC3mgvmGsJEafAokOADtGPhz6RJ0zriLGl15HYI0+JxRpmwmfQxwvv0YsYi/hMcs6gm489Qj6RT+E/Fc2JpxVO2FFPBafImRYb+0HtkhvqgyYdjzt0E56wjTpDHyf6wKcTn4yd6OzQI9qd7JP6InMJG+mRQe1GemTQozg3ob5Lf0n/JPKkv9gTTiRuQj2NeiLPRHQO0CdIjcDRD9nYID0K1GvRivriI6b+ip4efYn2hL3EIhsvenro6aXXOXSOfIb1T1s46pzFfQGbXPLJsTZoU3NfaA2IDTTEs/CoJdo76mnsNexTySfF2mAem/gFb+VLHlMec97inl6hH/iSVZSI6V61f/2dcjKpCrXIn698/NM+TwaVGm9Wr2fzGn9Pw1dv6mejZrWc3eFptFm+rFf758tm+bZZL+5rhYPCdqB+V3xVjs4d/58dPs3ZgTqQnHWCeIJlfSKdqr3V2Ljtc63ebqaz6bzB8oJw5/PjM/nPOK4/kz/qZ0R8pb7A4pWD1p8NPAy+fL/BY57/3R15rK5wSpDwnonTj534URGLUxOLz3T3He3dY/y5u+lT1TXWOGod9f/38I/5/0/FffL/TpwKJ4N3",
        },
    ],
}
