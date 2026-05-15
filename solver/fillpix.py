"""The Fill-a-pix solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent


class FillpixSolver(Solver):
    """The Fill-a-pix solver."""

    name = "Fill-a-pix"
    category = "shade"
    aliases = ["fillapix", "mosiak"]
    examples = [
        {
            "data": "m=edit&p=7VdLbxMxEL7nV1Q+++Cx16+9oFJaLiUFUlRVqyhKw1aNSJSSdBHaKP8de5yym3GR4ADlUG09mn6e8Xwejx/ZfG2m65qDjn/KccEhfEY4bOAEtsfvcv6wqMsjftw83K3WQeH84uyM304Xm3pQ7a3Gg23ry/aYt2/LigHjTIYGbMzbD+W2fVe2Q96OQhfjLmDnyUgG9bRTr7A/aicJBBH04V4P6nVQZ/P1bFFPzhPyvqzaS85inNfoHVW2XH2r2Z5H/H+2Wt7MI3AzfQiT2dzN7/c9m+bz6kvDHkPseHuc6I6eoKs6uuonXfU0Xfn36frxbhfS/jEQnpRV5P6pU12njsrtLvLaskJE17AykNaGFTICqgcUFDAUcBEoeoCPgO4ALSgAxEVjFNEBBl1e9QBKzBRkDGMIYN3jMu4BR2frgFpIaqEoQPPhNLUwFLAE8IIw9UAG9Z4AIKgJCJUhmmQRgEYCSfMI0pLVAYmJsz1EaWqjMptUS6aPFGTioA0dR2fjaFo+YGj9gMmyYbKRjaVzN7QgwCrqZQ3lYzOGqQb6iM8RjO76CI7jO0SmNT1AigzRJKsSgHCWoEh0CZpEl2AzG09jSUW9JJ2XVLSipCoow1QbB4inSJFxTtXSn1c6JvpeOrfJ8mM8nYUVNJbNolta4dLSfSFTJRyMnMVKJ0g/Py7zcp5G95p6ZfUjPd0XKtVPb3+ptN9VH5EHXuHcBzz9r1GeoZQoL8PlwFuF8g1KgVKjPEebU5RXKE9QFigN2th4vfzmBYRXjwuXRZiDTLfRP+BWFelp86tPv/T+773jQcVGzfp2OqvDG2jYLG/q9dFwtV5OFyw8OncD9p1hq1QwL17eoc/0Do1LIP7oNfr8Z1MVshtOiPaCs/tmMp3MVgsWfspwxCHD/zn7cICNBz8A",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=8))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="gray", adj_type=8, include_self=True))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
