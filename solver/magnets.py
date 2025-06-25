"""The Magnets solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent


def magnet_constraint() -> str:
    """Generate the magnet constraint."""
    constraint = ":- math_G__2(R, C), math_G__2(R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__3(R, C), math_G__3(R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__2(R, C), area(A, R, C), not math_G__3(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__3(R, C), area(A, R, C), not math_G__2(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- gray(R, C), area(A, R, C), not gray(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    return constraint.strip()


class MagnetsSolver(Solver):
    """The Magnets solver."""

    name = "Magnets"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VZdj9pGFH3nV0Tz2qnkmbE9Y79tt2xftqQtG0UrCyFCnHTVpU5hqSqv+O859/oOUBdCSduNGkXg8fHhzv04d8bM6rf1bFlrk9DXBY07PqkJfNmQ85XI5+bu4b4un+mL9cPPzRJA6+dXV/rN7H5VDyqaic9k8NgWZXuh2+/KShmllcVl1ES3P5aP7fdlO9TtGD8pHcBdd0YWcLiDL/l3QpcdaRLgkWDAW8D53XJ+X0+vO+aHsmpvtKI43/BsgmrR/F4ryYOe583i1R0Ri9nbX+uHldCr9evml7UYmslGtxecq9gfSNjtEibYJUzoQMJUx3+ZcDHZbKD6T0h5WlaU/YsdDDs4Lh8xjspH5SxNRWNM1xrlUiLcHpFHNSIRelNSnrJHZI6IdEf4fpRgeoRJkl5ckxS9wMZy5H3G+f6srJ+dydnzn5h+OibnErYZQxzDEt3yeMWj5fEGCurW8fgtjwmPGY/XbDOEsDZNtE1RpsW6Tw0wghK22E4RE59lHc4ybXOUTDiHzRYX2HoQlHBw2hYomXCBLbnFHhiFMw7amc6/M2YPY1+bLh/mbRcXd+1cF4uxRb8Z58Cdf9y1k1rgD366fHDf2lBcW0jORaEdNZRsEooLeaO9YK4lRJwCiw4BOkQ/HvpEnjCtI8aWXkdijzwlFmuYCZ9BHy+8Ry9iLOIzyTmDbj72CPlEPoX/VDQnnlY4YUc9FZwiZ1ps7Ae1S26oD5p0PO7QTXjCNuoMfZzoA59OfDJ2orNDj2h3sk/qi8wlbKRHBrUb6ZFBj+LchPou/SX9k8iT/mJPOJG4CfU06ok8E9E5QJ8gNQJHP2Rjg/QoUK9FK+qLj5j6K3p69CXaE/YSi2y86Omhp5de59A58hnWP23hqHMW9wVscsknx9qgTc19oTUgNtAQz8KjlmjvqKex17BPJZ8Ua4N5bOKXvJUveUx5zHmLe3qF/s2XrKJEQveq/efvlJNJVahF/nzl45/2eTKo1Hi9fDOb1/h7Gr5+Wz8bNcvF7B5Po/XiVb3cPV82i3fN6u6hVjgobAbqD8VX5ejc8eXs8GnODtSB5KwTxBMs6xPpVO2txsZtn2v1bj2dTecNlheEO58fn8l/xnH9mfxBPyPiK/UVFq8ctP5q4GHw9YcNjnn+f3fkWF3hlCDhAxOnHzvxoyIWpyYWn+nuO9i7Y/y5u+lT1TXWOGod9P/v8Mf8f4kL/sn/U3FanAzeAw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(["math_G__2", "math_G__3", "gray"]))
        self.add_program_line(adjacent())
        self.add_program_line(magnet_constraint())

        areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(areas):
            fail_false(len(ar) == 2, "All regions must be of size 2.")
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")

            if r == -1 and 0 <= c < puzzle.col:
                self.add_program_line(count(int(num), color="math_G__2", _type="col", _id=c))

            if r == puzzle.row and 0 <= c < puzzle.col:
                self.add_program_line(count(int(num), color="math_G__3", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row:
                self.add_program_line(count(int(num), color="math_G__2", _type="row", _id=r))

            if c == puzzle.col and 0 <= r < puzzle.row:
                self.add_program_line(count(int(num), color="math_G__3", _type="row", _id=r))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"gray({r}, {c}).")

        self.add_program_line(display(item="math_G__2"))
        self.add_program_line(display(item="math_G__3"))
        self.add_program_line(display(item="gray"))
        return self.program
