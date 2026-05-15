"""The Retsurin solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route


def count_row_col_xor(target: int, src_cell: Tuple[int, int], color: str = "black") -> str:
    """A rule to ensure that only the number of the shaded color equals to the target, but not both."""
    src_r, src_c = src_cell
    rule = f":- N1 = #count {{ C : {color}({src_r}, C) }}, N2 = #count {{ R : {color}(R, {src_c}) }}, N1 = N2.\n"
    rule += f":- N1 = #count {{ C : {color}({src_r}, C) }}, N2 = #count {{ R : {color}(R, {src_c}) }}, (N1 - {target}) * (N2 - {target}) != 0."

    return rule


class RetsurinSolver(Solver):
    """The Retsurin solver."""

    name = "Retsurin"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VTfi9swDH7vX3HoWQ927PyoX0Z3u+4l621rxzFCKGmW48KSpUubMVzyv0+227XNjlG4Yww2jCX5k4X1SVibr13WFsgZcoEiQtK0JI/QFx5G+832a1Fuq0Jd4aTbPjQtGYi30yneZ9WmwFGyv5aOdnqs9AT1a5WAB2g3hxT1O7XTb5SeoZ6TCzBKEequ2pZ5UzUtWIzTvZgsDuiReXM076zfWNcO5Izs2d4m8yOZednmVbGMHfJWJXqBYN5+aaONCXXzrQAXZs95U69KA6yyLTHcPJRrQEGOTfep+dzB4YUe9cQxiA8M5O8ZiCMD8ZOBeJyB9ywMqnXzSO7jtO+pLe8p+6VKDJEPRzM6mnO1A858UBF1TAinfeZ0wJ0OI9K9yXsHgoFrMnctBsENwE4Ab3hDGCA4AcaDECkHIYEchET80JQ9YJNO4MUJ4t45RXw2RAI+RAy5M8Rj5wSIOFe73vTKyKmVnpULKiJqYeUrK5mVvpWxvXNj5Z2V11ZKKwN7JzRtuLRRgqoiqVohKdeOp+QGYUgFG1ODpY8yACUuzDYRbmqcL//fwtJRAvOuvc/ygr5kXH4prmZNW2cVnWZdvSraw5nGYz+C72B3ItAzwf8n5l85MU2L2IXf8ek/8HmmQ6LnKCTqW4R1t8yWVGZbKYPLcIALg8eHLz9wMuekufCL449zpjGTjn4A",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_line(color="not black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="not black", adj_type="line"))
        self.add_program_line(single_route(color="not black"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"hole({r}, {c}).")

            if isinstance(clue, int):
                self.add_program_line(count_row_col_xor(clue, (r, c), color="black"))

            # empty clue or space or question mark clue (for compatibility)
            if isinstance(clue, str) and (len(clue) == 0 or clue.isspace() or clue == "?"):
                continue

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            if color == Color.BLACK:
                self.add_program_line(f"black({r}, {c}).")

            if color == Color.GRAY:
                self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
