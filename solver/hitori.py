"""The Hitori solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c, unique_num
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected


class HitoriSolver(Solver):
    """The Hitori solver."""

    name = "Hitori"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VbLbttKDN37K4xZz2Ko52Pnpkk3qdPWuQgCQTBkV0GE2lAqW0Uhw/8eklJKz7iL3kWTTSGIIDmjw6PDMeXd965sK53g5SfaaMDLDzy+PZPybcbrtt5vqmyqZ93+sWnR0frm6ko/lJtdNcnHXcXk0KdZP9P9hyxXoLTy8AZV6P5zdug/Zv1c9wtcUjrA3PWwyUP3Utw7XifvYkiCQX8++ujeo7uu2/WmWl4PmU9Z3t9qRXXe8dPkqm3zo1IjD4rXzXZVU2JV7vFldo/107iy674237pxLxRH3c8GuosXukRnpOsLXXIHuuT9hi499pfppsXxiLJ/QcLLLCfu/4mbiLvIDmjn2UF5ET5KvebOKC8mpClSe0kkbiJ1Er7BRCQhuOseJnwJfXedKggDn/C9X2FA6KfbA8IXuIDQQwkJPZAwcJ8OLfSQ0KV26HIPCT2W0OUeuvgh4VsJ0vcEwdU3ogpWwn6DiCokEtr8Ixs9InRpReT2LiJtZXvsso8JXYrF9tmICV1qx3bfYvdcJKStgCWutgmhS+cSV5mE8KXRiYuf2ucutc9F6uqakq5SLnW1SQlfdAfjHjww7huAsQ8fGLt3YEhg4QTGPR0AZ1XgrApQFRESgKqcoILbRgCqI9IAkNT2DlttHAbAI+Ge7RVbj+0tTgzd+2zfszVsQ7bXvOeS7R3bC7YB24j3xDRz/nAq8TwKhjnkDSPqFbjlHol1elFTXzEuJrladO1Dua5wrM+77apqp/Om3ZYbhd/R40T9VHxz34N/n9Y3+rRSC8z/+sC+/S8rR3XxfPc3Wj11y3K5bjYK/51pzsdn+Vdnjz8/9Vjvm7ZWxeQZ",
        },
        {
            "url": "https://puzz.link/p?hitori/10/10/1174453399113445756a2345678aa82513328aa85417a698323227a9411566517a43236688115329986a115274aa99886611",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(unique_num(color="not black", _type="row"))
        self.add_program_line(unique_num(color="not black", _type="col"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_adjacent_color())
        self.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(f"number({r}, {c}, {num}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
