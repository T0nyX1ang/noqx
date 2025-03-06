"""The Kropki solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, validate_direction, validate_type


def kropki_constraint() -> str:
    """Return the constraint for the Kropki puzzle."""
    white_rule = "|N1 - N2| != 1"
    black_rule = "(N1 - N2 * 2) * (N1 * 2 - N2) != 0"
    empty_rule = "(|N1 - N2| - 1) * (N1 - N2 * 2) * (N1 * 2 - N2) = 0"

    rule = f":- white_v(R, C), number(R, C - 1, N1), number(R, C, N2), {white_rule}.\n"
    rule += f":- white_h(R, C), number(R - 1, C, N1), number(R, C, N2), {white_rule}.\n"
    rule += f":- black_v(R, C), number(R, C - 1, N1), number(R, C, N2), {black_rule}.\n"
    rule += f":- black_h(R, C), number(R - 1, C, N1), number(R, C, N2), {black_rule}.\n"
    rule += f":- grid(R, C), not white_v(R, C), not black_v(R, C), number(R, C - 1, N1), number(R, C, N2), {empty_rule}.\n"
    rule += f":- grid(R, C), not white_h(R, C), not black_h(R, C), number(R - 1, C, N1), number(R, C, N2), {empty_rule}.\n"

    return rule.strip()


class KropkiSolver(Solver):
    """The Kropki solver."""

    name = "Kropki"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VVNa9tAEL37V4Q972E/ZUk3N017SdUPOwQjhJFdFQvbyJWtUtb4v2d2JFCgs4cWklzKssPT0/PozXg/Tj+7sq14DEPHXHAJQxuFU4kEpxjGoj7vq/SGz7rztmkBcP454z/K/ama5IOomFxckroZdx/TnEnGmYIpWcHd1/TiPqVuyd0cXjEugbvvRQrg3Qgf8b1Htz0pBeBswACXADd1u9lXq/m8p76kuVtw5j/0Dn/uITs0vyo2GPHPm+awrj2xLs9QzGlbH4c3p+57s+sGrSyu3M16vxnhV49+Pez9ekT49WW8tN+kuF6h8d/A8SrNvfmHEcYjnKcXiBlGiXGZXpiWBvJI+NpoEVwzrSLgFcFPab0WNG80ncdYWm8DfiJF54l8fkofyB8F6ooCdU0DfqaB/LEM8AnNJwF94uuleLqfJqL7b7A/hH4a0GO9hD6m+2/igD6h67XCf/dPvRX0/2JFHOB9foKXdF1W0v200ucneEXXaxXdT6vodWID+8LqgB9NrytrAn4MtW5hc3/ALa4wLuAE4E5jfI9RYLQY71Fzh/ER4y1GgzFCzdSfIX91yjA8QJgFO3gHPD91XsheriK8w8ZhX/e5mOQs6w7rqr3JmvZQ7uG8nm/LY8XgarxO2G+GM9cgNv9vyze7Lf2fIP75znybzZVDe2F9P9tRnB27VbnaNLDMRPHqdmG/sV3bHHc1KyZP",
        },
        {
            "url": "https://puzz.link/p?kropki/17/17/i970j090443913a1033a299190319301330b0930004aa04163399c03i04d1d61d0d70d7d7941130i4dddddddddc003a34303d50c9cad23134900a5da411dc4014df090ad040jcc000c4900n7ddadbddc00dd90601a010630mdddd9",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
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
        self.add_program_line(kropki_constraint())

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(d in (Direction.TOP, Direction.LEFT), f"Symbol direction at ({r}, {c}) should be top or left.")
            tag_d = "h" if d == Direction.TOP else "v"

            if symbol_name == "circle_SS__1":
                self.add_program_line(f"white_{tag_d}({r}, {c}).")
                self.add_program_line(f"not black_{tag_d}({r}, {c}).")

            if symbol_name == "circle_SS__2":
                self.add_program_line(f"black_{tag_d}({r}, {c}).")
                self.add_program_line(f"not white_{tag_d}({r}, {c}).")

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
