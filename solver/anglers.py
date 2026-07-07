"""The Anglers solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected
from noqx.rule.route import single_route


class AnglersSolver(Solver):
    """The Anglers solver."""

    name = "Anglers"
    category = "route"
    aliases = ["anglerfish"]
    examples = [
        {
            "data": "m=edit&p=7VRNj9MwEL33V6zmPIc4TpqPCyrLlkvoAu1qtYqqKg1ZNSLZlHwg5Kr/nfEkbSpSxFLBigOyPHp+E8dvZuypvjRRmaBLQ7pooKAhLZOnaXg8jW4s0jpL/CucNPWmKAkg3k6n+BhlVYKjUPBmsRztlOerCaq3fggmIE8BS1Qf/J1656sHVHNyAVrEBYQEoEnwpof37NfouiWFQXjWYYIPBOvkqa7a5Xs/VAsEfchr3qoh5MXXBNo9vI6LfJ1Cv5PJqvlUfG7g+GvIm6xO4yIrSuBfieUe1aSVHhyki066BSh76fIoXZ6XbnbS47SMs2QVXKR+HdVUiGqTbs+F4J0PYU9l+UhBrPxQx3PXQ7eHc38HtgW+tdeKCYtDXtoKwtiCtqgHwnE0IXvCM6BNy4EQhtSMfcKIsWZeHRg6TPi7vc7MDqRHPoknxQVbDqjxkHLsIeUOKNf5gaJjp3y4yXZBiUAl2b5ha7C12Qb8zQ3be7bXbC22Y/7G0al8ZrLbNJ/G/7tyQJoUkeciWK7sgGe3wBao8ySfKTmUHorjcC7Hy1EI86Z8jOKELmiQPiVXs6LMo4xWsyZfJ2W/nm+ibQLUM/Yj+AY8qTyCWsP/NvJvthFdIuPF7vefeW4hZZw6C1I/Q3WLsG1W0YoCA6Sk/trZPqRLnH/nTHrz5x3UA37i8OyB48VrRC1mOfoO",
        },
        {
            "url": "https://puzz.link/p?anglers/10/10/t1zw1p1s1h1g1h1u-19l-19s7ocgecic",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.symbol) > 0, "No clues found.")
        fail_false(len(puzzle.text) == len(puzzle.symbol), "Unmatched clues.")
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="grid", path=True))
        self.add_program_line(avoid_unknown_src(color="grid", adj_type="line"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(symbol_name, "tents__3")
            self.add_program_line(f"dead_end({r}, {c}).")

        tag = tag_encode("reachable", "grid", "src", "adj", "line", "grid")
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if not (0 <= r < puzzle.row and 0 <= c < puzzle.col):  # coordinations out of bounds
                self.add_program_line(f"grid({r}, {c}).")

            self.add_program_line(f"dead_end({r}, {c}).")
            self.add_program_line(grid_src_color_connected((r, c), color="grid", adj_type="line"))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num + 1, (r, c), color="grid", adj_type="line"))

            for (r1, c1, _, _), _ in puzzle.text.items():
                if (r1, c1) != (r, c):
                    self.add_program_line(f":- {tag}({r}, {c}, {r1}, {c1}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
