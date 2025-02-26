"""The Creek solver."""

from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def creek_covering(target: int, r: int, c: int, color: str = "black") -> str:
    """Generate a constraint to check the {color} covering of cells."""
    return f":- {{ {color}({r - 1}, {c - 1}); {color}({r - 1}, {c}); {color}({r}, {c - 1}); {color}({r}, {c}) }} != {target}."


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(grid_color_connected(color="not gray"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d, Direction.TOP_LEFT)
        validate_type(pos, "normal")
        if isinstance(num, int):
            solver.add_program_line(creek_covering(num, r, c, color="gray"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))

    return solver.program


__metadata__ = {
    "name": "Creek",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VXPj9o8EL3zVyCfWmkOSez8vFR0u+2FZr+vUK1WUYQCawpqULaBVFsj/vcdT6KNiffQHkpVqTIePZ6fx4+xjfffmqKW4Hr6wyNwwMUmYkGdhz51p2vz7aGUyRgmzWFT1QgAblJYF+VejjI9EVs+Oqo4URNQH5KMuQyYRz0H9X9yVB8TlYKa4RCDCLlpK/IQXvfwlsY1umpJ10GctjhAeIdwta1XpVxMcRSZ/5JMzYHpdd7SbA3ZrvouWedDf19Vu+VWE8vigL9lv9k+dCP75r762nRaNz+BmrR2Zy/Y5b1dDVu7Gv0uu/L+i3x8yWmcn05Y8U/odZFk2vbnHkY9nCVHjGlyZNwJ9dw36AwwAybkTqwZ3KdnxnU1w03GH2o8PtR4lMdkhNP57BnKbOYRnqURVh7ybM7yLT8+acw8fjRkAvJjZg5odTNPaDkMbY21VmjVMKLVzbUiSxOTnzPGqnxMdTY0wiHGWF04VDFT4w0rL6z9Ep49i6p6phlWXnBLwy2Nte+i3eVnDR5Gl47kHcX3FD2KczyxoDjFdxQdij7FKWmuKd5SvKIoKAakCfWZ/8lbwXwsuAcswN8QtVfkAt4yv/u7PGvh38flo4zNmnpdrCT+PaXNbinrcVrVu6Jk+BScRuyRUc+4flj+vQ6Xfx109Z1feiP+/OXMsLBBCOoG2EOzKBarqmSAZdM8Xp0hf3H3eIPZelvLdflj/GpTHYq6GS9lsXvN8tET",
        },
        {"url": "https://puzz.link/p?creek/10/10/qbdccdbdbibiceeeddcblbbcdcdddboabbb", "test": False},
    ],
}
