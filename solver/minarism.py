"""The Minarism solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, validate_type


class MinarismSolver(Solver):
    """The Minarism solver."""

    name = "Minarism"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VRNb9pAEL37V0R7nsN+2RjfaJr2krofoYqQZSGTusIq1BRw1S7iv2dmbGpCF1WRmvRSLR495s3MPu+Md/OtKdYlDHCZGCQoXEZafiJJv8MaV9tFmVzAqNnO6zUCgLcpfC4WmzLIuqA82Llh4kbgXieZUAKExkeJHNz7ZOfeJG4C7gYpAQp9122QRnjVw1vmCV22TiURp4gjARHCCcLqa4nKF9X2Zxv6LsncGATt9ILzCYpl/b0UnRL6f1cvZxU5ZsUW32Yzr1Yds2k+1V+aLlble3CjVnDqEWx6wQRbwYROBXdv9OSCh/l+j0f/ASVPk4zUf+xh3MObZIc2TXZCR1GXGwGeKxY0SpInPPJojjFHniHH2N5jJXuoMwePMqce/VuM1ie725CzflVGmYrFTkjsgApoeHCI2A+h4xgJ+5DA0xWahZ5kEIFz7c8wMjxDKNLqIzSV8u0RD5BQPoLk+ogh7eElKMP4iKGfsIpUeUpZTSfsyzD05j7CnlFlLZXyEuc2D717YH9fcZc12zFOKTjD9iVbyTZke80xV2xv2V6ytWwjjhnQnD/ySyDJNOTYSbypjgfvieRl2vI9e1jh3/+XB5lIm+WsXF+k9XpZLPDWuJkXq1LgFb0PxA/BD3ZEgf1/a//DW5vaIB81sc8woX+Qk+H54gwffTUgVs20mN7VOGgyf3a5+E3lwT0=",
        },
    ]

    def program(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")
        n = puzzle.row
        self.add_program_line(defined(item="white_h"))
        self.add_program_line(defined(item="white_v"))
        self.add_program_line(defined(item="black_h"))
        self.add_program_line(defined(item="black_v"))

        self.add_program_line(grid(n, n))
        self.add_program_line(fill_num(_range=range(1, n + 1)))
        self.add_program_line(unique_num(_type="row", color="grid"))
        self.add_program_line(unique_num(_type="col", color="grid"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            if d == Direction.LEFT and c > 0 and symbol_name == "inequality__1":
                self.add_program_line(f":- number({r}, {c}, N), number({r}, {c - 1}, N1), N < N1.")

            if d == Direction.TOP and r > 0 and symbol_name == "inequality__2":
                self.add_program_line(f":- number({r}, {c}, N), number({r - 1}, {c}, N1), N < N1.")

            if d == Direction.LEFT and c > 0 and symbol_name == "inequality__3":
                self.add_program_line(f":- number({r}, {c}, N), number({r}, {c - 1}, N1), N > N1.")

            if d == Direction.TOP and r > 0 and symbol_name == "inequality__4":
                self.add_program_line(f":- number({r}, {c}, N), number({r - 1}, {c}, N1), N > N1.")

        for (r, c, d, pos), num in puzzle.text.items():
            validate_type(pos, "normal")

            if d == Direction.CENTER:
                fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
                self.add_program_line(f"number({r}, {c}, {num}).")

            if d == Direction.TOP and r > 0 and isinstance(num, int):
                self.add_program_line(f":- number({r}, {c}, N), number({r - 1}, {c}, N1), |N - N1| != {num}.")

            if d == Direction.LEFT and c > 0 and isinstance(num, int):
                self.add_program_line(f":- number({r}, {c}, N), number({r}, {c - 1}, N1), |N - N1| != {num}.")

        self.add_program_line(display(item="number", size=3))

        return self.asp_program
