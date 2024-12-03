"""The Fill-a-pix solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent(_type=8, include_self=True))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(count_adjacent(num, (r, c), color="gray", adj_type=8))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Fill-a-pix",
    "category": "shade",
    "aliases": ["fillapix", "mosiak"],
    "examples": [
        {
            "data": "m=edit&p=7VdNbxoxEL3zKyKffdix9/uWpkkvKWlLqihaIUToRkEFkUKoqkX894yfaXfWm0rtoUkPEexoeJ7xvBnP2mbzbTtd15oS97W5jjTxJ41yPJTzb35+fi7nD4u6PNLH24e71ZoVrS/OzvTtdLGpB9XBajzYNUXZHOvmXVkpUloZfkiNdfOx3DXvy2aomxEPKZ0zdu6NDKunrXqFcaedeJAi1ocHndVrVmfz9WxRT8498qGsmkutXJw38HaqWq6+1+rAw/2erZY3cwfcTB84mc3d/P4wstl+WX3dHmxpvNfNsac7eoKubek61dN12hN0XRb/mG4x3u+57J+Y8KSsHPfPrZq36qjcsRyWOxVHzpVXhvzaqNg4wAogDoE0BHIHxAIoHJC0QIIoEqDAJUGUqAXSkEcKC+GSgocAMvBwVT8AeZhcjrDSAlGkhQ2BMP08CS3AQwJZABTgIZgW4CEmLVAxAVAUmlAEah0EVETRiMJIZMI6kgE9sRhkULhMIBYzSxvbs/Gtk0oEtRKJU4LayHmS3jxJ2C2Uhu1Caa8afvU7NshL5p6GDUEZaii9Mswj+fg2kojvAYkUfQTRc4lgnqJFjF/TDoJ5OggqL6pqCF6CsyFkIaIbgpeIbgh8Ojaos4xlMI/0MmFexoYdZSxsJEPfGx0EsSQS9zj7bpF5+V1BevltoWPTq0+KWDKLDJxlLL/uHSTscJOF74XxndCZuRfL7yCyPnnPK4eXjF4guvTq9Y/xe4LgY33/iPfL+vddvBeWwOeXF2/zhM3+GvIM0kBe8lmgGwv5FjKCTCDPYXMKeQV5AhlDprDJ3Gnyh+cNTpqczwbOwfjD5xm4VbG/yfzuw/ed19H/e3Q8qNRou76dzmq+8gy3y5t6fTRcrZfTheI75n6gfig8lWXz+PXa+ULXTrcE0V9dPl9+b6q4urxDNBda3W8n08lstVD8z0UDpx7+7Ox5AxsPHgE=",
        },
    ],
}
