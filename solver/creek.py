"""The Creek solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_covering
from noqx.rule.reachable import grid_color_connected


class CreekSolver(Solver):
    """The Creek solver."""

    name = "Creek"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VXPj9o8EL3zVyCfWmkOSez8vFR0u+2FZr+vUK1WUYQCawpqULaBVFsj/vcdT6KNiffQHkpVqTIePZ6fx4+xjfffmqKW4Hr6wyNwwMUmYkGdhz51p2vz7aGUyRgmzWFT1QgAblJYF+VejjI9EVs+Oqo4URNQH5KMuQyYRz0H9X9yVB8TlYKa4RCDCLlpK/IQXvfwlsY1umpJ10GctjhAeIdwta1XpVxMcRSZ/5JMzYHpdd7SbA3ZrvouWedDf19Vu+VWE8vigL9lv9k+dCP75r762nRaNz+BmrR2Zy/Y5b1dDVu7Gv0uu/L+i3x8yWmcn05Y8U/odZFk2vbnHkY9nCVHjGlyZNwJ9dw36AwwAybkTqwZ3KdnxnU1w03GH2o8PtR4lMdkhNP57BnKbOYRnqURVh7ybM7yLT8+acw8fjRkAvJjZg5odTNPaDkMbY21VmjVMKLVzbUiSxOTnzPGqnxMdTY0wiHGWF04VDFT4w0rL6z9Ep49i6p6phlWXnBLwy2Nte+i3eVnDR5Gl47kHcX3FD2KczyxoDjFdxQdij7FKWmuKd5SvKIoKAakCfWZ/8lbwXwsuAcswN8QtVfkAt4yv/u7PGvh38flo4zNmnpdrCT+PaXNbinrcVrVu6Jk+BScRuyRUc+4flj+vQ6Xfx109Z1feiP+/OXMsLBBCOoG2EOzKBarqmSAZdM8Xp0hf3H3eIPZelvLdflj/GpTHYq6GS9lsXvN8tET",
        },
        {"url": "https://puzz.link/p?creek/10/10/qbdccdbdbibiceeeddcblbbcdcdddboabbb", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(grid_color_connected(color="not gray"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_covering(num, (r, c), Direction.TOP_LEFT, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
