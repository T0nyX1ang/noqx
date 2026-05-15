"""The Kurarin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_type
from noqx.rule.neighbor import adjacent, count_covering
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route


class KurarinSolver(Solver):
    """The Kurarin solver."""

    name = "Kurarin"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7Vbfb9owEH7nr6j8fA+xz4mTvHVdtxdG14WqQlGEUpaKaGFhQKYpiP99ZweGCocE07Qf0mR8uXx3Pt9n52yWX5p8UYD07A9DoCc1LUPXVRi47m3bsFxVRXwF181qWi9IAbgbwHNeLQvopVuvrLduo7i9h/ZtnAolwHUpMmjv43X7Lm5H0CZkEhBmIGZNtSondVUvhMMk+fVJkwIUqbd79dHZrXbTgdIjfbDVSR2ROikXk6oYJ0nn+T5O2yEIO/krN9yqYlZ/LUQ3zr1P6tlTaYGnfEUMl9NyLgDJsGw+1p8asZtiA+11RyE5h4J2QXYU8AcF5CmolxT6XaBfySDKNhvanQ/EYRynls7DXg33ahKvNzYtK6WTo3gtECmMgoMlFhgRLI9g6QcsrrTF/WPcNyfwiMeNYtNRIfL+kcfmg55k/dHj6WrF568x5P2Nx/sbfl4dKhb3vZDHFb9uvubnDSS/noHS7PoEqFlegTkRJ+J5GY/nZSSfp5E8L6NOxEF+3w36PK759TQ+lz+VwBtXCMrJIdUJtOjkayc9J30n+87n1slHJ2+c1E4GzsfYSjuzFoUtmdB+MvQ4LsxLc6NwFC8K7TcOSGzRaZr2Gc/MO8XuonjZ/H8Py3qpSJrFcz4p6CTtl5+Lq0G9mOUVvSXTfF4Ius42PfFNuJ4iKDvo/w33N99wdqe8n77n/kypp21/V4/Q3oGYN+N8TCsu6A8V7IxUorwxQMUbtMJLDRhcOsepEXTOcIaEDAc4bnFzgOvst28THW5Z7zs=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(fill_line(color="not gray"))
        self.add_program_line(single_route(color="not gray"))
        self.add_program_line(grid_color_connected(color="not gray", adj_type="line"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(
                not (d == Direction.CENTER and symbol_name == "circle_SS__5"),
                f"Gray circle cannot be placed in the center of ({r}, {c}).",
            )
            target = 2 if d == Direction.TOP_LEFT else 1

            if d == Direction.CENTER and symbol_name == "circle_SS__1":
                self.add_program_line(f"not gray({r}, {c}).")

            if d == Direction.CENTER and symbol_name == "circle_SS__2":
                self.add_program_line(f"gray({r}, {c}).")

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__1":
                self.add_program_line(count_covering(("lt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__2":
                self.add_program_line(count_covering(("gt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__5":
                self.add_program_line(count_covering(target, (r, c), d, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="gray"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
