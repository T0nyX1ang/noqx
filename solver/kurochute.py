"""The Kurochute solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected


def count_sight(src_cell: Tuple[int, int], distance: int, color: str = "black") -> str:
    """Generate a rule to count the number of color cells in the distance of sight."""
    r, c = src_cell
    cells = ((r + distance, c), (r - distance, c), (r, c + distance), (r, c - distance))
    cell_str = ";".join(f"{color}({r0}, {c0})" for r0, c0 in cells)
    return f":- {{ {cell_str} }} != 1."


class KurochuteSolver(Solver):
    """The Kurochute solver."""

    name = "Kurochute"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZLj9owEL7zK1Y+zyHjR16Xim6XXijbFqrVKkIoS7Na1KDQQKrKiP/esUMJE3FopYpeVpFH882Mxx/jsc32e5PXBaACRFAxBID0GSVBmxBQRn4Ex2+22pVFegPDZvdS1aQA3I9G8JyX22KQHaPmg71NUjsE+z7NBAoQkgaKOdhP6d5+SO0E7JRcAjTZxm2QJPWuUx+832m3rRED0idHndRHUperelkWi3Fr+ZhmdgbCrfPWz3aqWFc/CnHk4fCyWj+tnOEp39GP2b6sNkfPtvlafWvE7yUOYIct3ekFuqqjq0501WW68p/QLTfVJaLJ/HCggn8mqos0c6y/dGrcqdN0f3CM9kKFbuobYtHuilAJGeQJauTQhWMHY4LqBE3Mgo1LpU8wRBYcaZYqcplNB2PmjSXLnGiWOTEMYqBZNAaGJcOAJ0fEHjZ8vkSeX3KudCh4fK9oqB378Az3+OiIY8P3AMOA+8Owh3vrR735ccLjkx6/pJcv4fESJds5ia6+0Rk+rxc1Fvr2evRy5KX0ckbdB1Z5+c7LwEvj5djH3Hn54OWtl9rL0MdErn//sMN9b0tqQyVS3bb7FbhlKvS35qXPvHrmg0xMm/o5XxZ0gU2a9VNR30yqep2Xgt6Kw0D8FH74ftOvz8fVnw9X/OCvHpH/f+IzqqtRYO9BbJpFvlhWpaD/HuDsdB779quzp2thPvgF",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent(color="black"))
        self.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(count_sight((r, c), num))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
