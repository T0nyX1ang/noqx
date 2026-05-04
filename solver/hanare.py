"""The Hanare-gumi solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, fill_num, grid
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type


def hanare_constraint(color: str = "white") -> str:
    """Generate a constraint for hanare-gumi."""
    rule = f"row_pair(R, R1, C) :- number(R, C, _), number(R1, C, _), R1 > R, R1 - R - 1 = #count {{ R2: {color}(R2, C), R2 >= R, R2 <= R1 }}.\n"
    rule += ":- row_pair(R, R1, C), number(R, C, N), number(R1, C, N1), |N - N1| != R1 - R - 1.\n"
    rule += f"col_pair(R, C, C1) :- number(R, C, _), number(R, C1, _), C1 > C, C1 - C - 1 = #count {{ C2: {color}(R, C2), C2 >= C, C2 <= C1 }}.\n"
    rule += ":- col_pair(R, C, C1), number(R, C, N), number(R, C1, N1), |N - N1| != C1 - C - 1.\n"
    return rule


class HanareSolver(Solver):
    """The Hanare-gumi solver."""

    name = "Hanare-gumi"
    category = "num"
    aliases = ["hanaregumi"]
    examples = [
        {
            "data": "m=edit&p=7ZZdb9owFIbv+RWVr30Rf8V27rqO7qaj2+g0VQghSumKBqKDMk1B/Pe9do5jTSLqqn1p0hTivDk+sd/kPDHZft5NN3MuivBTjuOITQsXd+nKuBe0XS0el/PqhJ/uHu/XGwjOL8/P+d10uZ33RpQ17u1rX9WnvH5VjZhgnEnsgo15/bba16+rus/rIboYl4hdNElB9rP80PafNUFRQA9IQ15Dzhab2XI+uWgib6pRfcVZmOdFvDpItlp/mTPyEc5n69XNIgRupo+4me394oF6trvb9acdS1MceH3a2B0csauyXdXaVcftyt9v148PBzz2dzA8qUbB+/ssXZbDan8Ivvas1LjUoNaxMswanOr2VMTudI5LRLzwOrbnsZWxvcK4vFaxfRnbIrYmthcxp4/ppJBcypJVEjgIDe1IgzIlGy0tl1qQRlynuIdWjVYYR9M4uuDSaNIK2pI20J40CC4L0hizpDENckrKMcixlGPgwZIHg3yb8uHBkocSHix5KMNbQjkWfhz5sfDjyI/F/Tq6X4u5PM3lkOMpxyHHU46DN0/enOOqoPGdhyYPHq9rQXN55AjK8cgRTY4qkCM0aQndeFbhVZcUFwLakFbQlrSGdqQNtCddcqUK0ha6eVYYD5ryJXI05aCmSqcc+KSaKtRRUR1xHVeG4hpxQ3HUVKWaYkwpk0YtyAOO0FQvJTJLgY3EkhaZJS0zS4GTlqXAW+JBZa4M6mJMZoa8RTYSYyXmKmmuUmTGAhuJscBG4sqKzFVgw9L41mSunMhcOXh2KnPiKN/ZzJULHPqWDelpLm9briIPBdWiEC1XYKplKbIhRGaDuMIxcxU4SVwFTkTiB7UWiZnAJDEjAz9UU9Su5Qe1a/lB7ZRKDBSZmcCAprk05tI0F2rX8qMDb4GNQ1iJw5JzFlsd2zIuRTYsgD+4RDIqLK0bVFrb3Jlt+lzT5xvLokxHRUfT2BlECz+5ej55WyPV/G9/v5l/Lzbujdhwt7mbzub4m+vffpyfDNab1XSJs8FudTPfpHN8ZRx67CuL+0iFj5b/Hx5/6cMjlKB41ufHH3gnnrAzqocca3V9ydnDbjKdzNZgDM8uxovjcXwDHI1bdzzuZUd+xziuY16sLl0dqqvDdEzdEXddt/bM/K5H1PVIu0rwC8b548BhHR73vgE=",
        },
        {"url": "https://puzz.link/p?hanare/10/10/3162k3o9gjhb7mfbiie020t0a0vv2e400l8q6zzzzm9q", "text": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(hanare_constraint())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, (ar, _) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(len(ar), len(ar) + 1), _type="area", _id=i, color="white"))
            self.add_program_line(count(1, _type="area", _id=i, color="not white"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color == Color.WHITE, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"white({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")
            self.add_program_line(f"not white({r}, {c}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
