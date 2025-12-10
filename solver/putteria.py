"""The Putteria solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent


def putteria_fill_constraint() -> str:
    """Generate a constraint for the number filling in putteria."""
    return ":- area(A, _, _), #count { R, C : area(A, R, C), number(R, C, N) } != 1."


def avoid_num_adjacent(adj_type: int = 4) -> str:
    """
    Generate a constraint to avoid adjacent cells with the same number.

    An adjacent rule should be defined first.
    """
    rule = f":- number(R, C, _), number(R1, C1, _), adj_{adj_type}(R, C, R1, C1)."
    return rule


class PutteriaSolver(Solver):
    """The Putteria solver."""

    name = "Putteria"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VVNb9s4EL37VwQ88yB+itItmzq9ZJ1unSIIBMNwHKUxasOpP4pChv973lBDyAFsZIFFtzkUsujH0XD4OG80Wn/fTla1LHCZIDOpcJmQxTtY+mV83cw287o8k+fbzdNyBSDl9eWlfJzM13WvYq9Rb9cUZXMum49lJZSQQuNWYiSbf8pd83fZ9GUzxCMhA2xXrZMG7HfwNj4ndNEaVQY8YAx4BzidrabzenzVWj6VVXMjBe3zV1xNUCyWP2rBPGg+XS7uZ2S4n2xwmPXT7JmfrLcPy29b9lWjvWzOW7qDI3RNR5dgS5fQEbp0il9Mtxjt90j7ZxAelxVx/9LB0MFhuRPGizJIYW38c+3MB/zBYcAOlTgDzVa26PrKQIteGWj5K4PKMlhMN1cac9fNNcW03dzQ85znIKLKHca7OF7GUcfxBgeRjYnjhzhmcXRxvIo+fRxCoWxVkYtSI2LwwAXjXGoiR7jIgA1j2FWyB2DFuAAGOWCdKWAQj1gDO8YGGDkhrBBTtzG1gl0nuwVu+WiFvUy7l9awG7ZrB4xURgwOtuWgNThY5mCw1vFaCw6OOVjsRbpEDH/P/g6cPXN22MvzXg57kWyEPeLkHMcjTs5xPHzy5OOB2xxqj/iB4+fwCeyTg1vB3HLwL5g/GokuOCcBfArmU6DRZAkb4HZfyn/SC1pBI45DOWe9Yp5ZI+gDfJDzpBHlPGmkwF8d5F+lPGNt0kuTXryWtEjaafjr5I+zJ+1Ii6QXWqc2zNmQXkkj8Ew6Wpw96UjaWd7Xkta8lrRL+jqsdbyWdHRJU9Kd1zrS/UDfVA8O53V8XtLXs7+nGkhawyfVgwcHf6BvnnQk3dmHNE01kFMNsA9pmuohwCewT4BPqgd611I9QOuuBsCnYD4Fcl5QzvES38ZX+SKONo4+vuI5dbJ/2evahvbfu8mbdCq8rfTZPLyo2b0jy6hXieF29TiZ1viC9B++1meD5WoxmWM22C7u61Wa4wO+74mfIt6xh9s/3/Tf9E0nCbL3Vu1v0KmaoUQ3aa6leN6OJ+PpEjWG3JEdXemo3drjdnPC/5T9VJxT+x7h+b9nE+0DBDabejWbiFHvBQ==",
        },
        {"url": "https://puzz.link/p?putteria/7/7/4dvovcel0eprhelnrgk.zzi", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_num_adjacent())
        self.add_program_line(unique_num(color="not gray", _type="row"))
        self.add_program_line(unique_num(color="not gray", _type="col"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, (ar, _) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(len(ar), len(ar) + 1), _type="area", _id=i, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"gray({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(f"number({r}, {c}, {num}).")
            else:  # compatibility with puzz.link
                self.add_program_line(f"gray({r}, {c}).")

        self.add_program_line(putteria_fill_constraint())
        self.add_program_line(display(item="gray", size=2))
        self.add_program_line(display(item="number", size=3))

        return self.program
