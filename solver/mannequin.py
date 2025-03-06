"""The Mannequin Gate solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected


def distance_in_area(grid_size: Tuple[int, int]) -> str:
    """Generate a rule to calculate the distance between grids in an area."""
    r, c = grid_size
    rule = "dist(R, C, R, C, -1) :- grid(R, C).\n"
    rule += "dist(R, C, R0, C0, N) :- grid(R, C), grid(R0, C0), dist(R0, C0, R, C, N).\n"
    # The following r + c upper bound is not rigorous.
    # TODO Actually it's better to pre-calculate the distance in python for this puzzle.
    rule += f"dist(R, C, R0, C0, N) :- grid(R, C), grid(R0, C0), N < {r + c}, (R0, C0) != (R, C), area(A, R, C), area(A, R0, C0), N - 1 = #min{{ N1 : adj_4(R0, C0, R1, C1), area(A, R1, C1), dist(R, C, R1, C1, N1) }}.\n"
    return rule.strip()


def mannequin_constraint(color: str = "black") -> str:
    """
    Generate a rule to enforce the Mannequin Gate constraint.

    An area_adjacent rule and a dist rule are required.
    """
    rule = f"area_num(A, N) :- area(A, R0, C0), area(A, R1, C1), {color}(R0, C0), {color}(R1, C1), (R0, C0) < (R1, C1), dist(R0, C0, R1, C1, N).\n"
    rule += ":- area(A, _, _), area_num(A, N0), area_num(A, N1), N0 < N1.\n"
    rule += ":- area_adj_4(A1, A2), area_num(A1, N), area_num(A2, N).\n"
    return rule.strip()


class MannequinSolver(Solver):
    """The Mannequin Gate solver."""

    name = "Mannequin Gate"
    category = "shade"
    aliases = ["mannequingate", "manekingeto"]
    examples = [
        {
            "data": "m=edit&p=7VRBb9pMEL3zK6I9z2F3bRrbl4qm8F0oaQtVFFkWMsRpUKHmM7iqFvHf82a8liuVKGkjcaoWj57fzozfzA67+7/Oq4L6WEFEmgyWtZE8oeZfu2ar/bpILmhQ7x/KCoDoejSi+3y9K3qp98p6BxcnbkDuvyRVRpGyeIzKyH1KDu5D4obkpthSFIEbN04WcNjBG9lndNWQRgNPPAa8BVyuquW6mI8b5mOSuhkp/s47iWaoNuWPQnkd/L4sN4sVE4t8j2J2D6ut39nVd+W32vua7Ehu0MidnpAbdHIZNnIZnZDLVbxe7npbnhIaZ8cjGv4ZUudJyqq/dDDq4DQ5wE6Sg7KaQwOoaE5F2aAt2hPhJRNvO6IvIbolkMhIuluxI7FW7AxfIxeIfS9Wi+2LHYvPECLiEC3Cdy0S6oCMsQ02FtjzhvnQ+8TAUCEYA/or1j5Wc6zxsezT5oyAY4+RhxvA2GLUrfe38Lfe3yIP96TlA+8fwD/gPKjhRiq5EhuKfSMVXnK3X3gechJIbJEzag7n9Z19VlvKZfvVfxnKeqma1tV9viwwgsO7r8XFpKw2+Rpvk3qzKKr2Hf/9Y0/9VPKkOD8K/10HZ78OuPn6jy6FM8zdM3JSjEF7K5C7JrWt5/l8WWLG0DvZbS+KJ7b/PnhKNn6C17/xZ+8b/rLqe12tFmWtst4j",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(area_adjacent())
        self.add_program_line(distance_in_area(grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(mannequin_constraint(color="gray"))

        areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(areas.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(target=2, color="gray", _type="area", _id=i))
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(f"area_num({i}, {num}).")

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"gray({r}, {c}).")
            else:
                self.add_program_line(f"not gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
