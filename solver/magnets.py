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
    return constraint


class MagnetsSolver(Solver):
    """The Magnets solver."""

    name = "Magnets"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VbbbhMxEH3PVyC/YiTb49vmrZSWl1IuKULVKopCukBFQyBpENoq/86MdzYuS0MJlxYQ2qxz9mRuPmNvvPiwHM8rqRV9IEr8xsvqmG4TfboVX0en52dV/47cWZ6/mc0RSPl4f1++Gp8tql6pk68e9i7qol/vyPphvxRaSGHw1mIo66f9i/pRv96T9QB/EjIid9AYGYR7Gb5IvxPabUitEB8yRniMcHI6n5xVo4OGedIv6yMpKM/95E1QTGcfK8F10PNkNn15SsR0/Ppddb5gerE8mb1dijb+StY7qVa2v6JgyAXDumC4umDzmwsuhqsVqv4MSx71S6r+eYYxw0H/YkVFXQgw5IqN0U1rBFgi4BLhWzVaInZcrO0QDoiwmQjdLFF3CK1UJ69WRSexNrHLQOh6uW512quvmG452tsvKkZxdJLoOI37aTRpPEIFZQ1pfJBGlUaXxoNks4fCGquksThNg+veasSmwSZmTLxzDXZOGl802MdLuMCtBw2OIE0RGlz4SzggjoyjBN3EB60vYdzXWmfeNHnxWwIUGRvP2CMOjIME2/oajAOMYW1DeU3BNReFBGoo2SjKa7M94zSX2GKLmHWILscJOvOEA+sWDL2O2N6vcyUNHfMO9QnMB5VzEe+4Zoe6hbZHkHmL8S1k3rIvqIwt1uxYcxfXteH8UJPIumEvuNcJm1Zn1AdYH4wJHDNhYJ0BewRtTJd9CWvukca5a+6RDtlXUd9d1l+1PGR7worzKrOOaSLWqVjniPrEuMZtHLIxkXsUqdeQ+xJaTP1lPYPL9oSDzzaB9QyoZ+Bee5V5h+vfq6yzK7KN53o8rg3f7imXbYD2Hce0IdsD9TRke8v1WM/8il7ktJV302jT6NMWD/QK/c6XrKBCYvOq/fl3yrVFlTgX/cUVbvZ52CvFYDl/NZ5U+Pe0d/K6unM4m0/HZ/h0uJy+rOb5eXc2fT9bnJ5XAg8Kq574JNJdAp07/p8dbufsQB1QW50gbmBZX1NOWR9L3Lj1YyneL0fj0WSGywuF254fbMn/w3nDlvyVcQ6JL8VdXLx80PraIKDBvW8bbIr8d3dk07zidYLEbziOftTxhzIW1zkWf5jmvyrvlb3bxG+7m25rXgPpNvTr1/Cb4v/Pi/yN/6fiaXHY+ww=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(["math_G__2", "math_G__3", "gray"]))
        self.add_program_line(adjacent())
        self.add_program_line(magnet_constraint())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
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
