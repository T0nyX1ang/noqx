"""The Bosnian Road solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route
from noqx.rule.shape import avoid_checkerboard, avoid_rect
from noqx.rule.variety import nori_adjacent


class BosnianRoadSolver(Solver):
    """The Bosnian Road solver."""

    name = "Bosnian Road"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7Vbvb7JIEP7uX9Hs1+7l5YdQJLlcrLV927PUVo1XiTFoUWlBegjaYvq/d3aWBheh1y/X3CVvkNnZZ4bZZ2f1wfXfiRO5VJbYRzUojHDVZQNvxdDxlrKr78W+ax7RZhIvwwgcSm8sOnf8tUuv7pedVtjcnjX/2hjxaCRfSMmlNHw8fzy+C/689NRIPreM7nX32lMWzZ+t01u9fax3k/Ugdje3gXz6OBj1593hoqG8tq1RPR3dSNrVaP5j0xz8XrMzCuPaLm2YaZOmF6ZNZEKJArdMxjS9NXfptZlaNO1BiFADsA5PUsBt5+4Q48xrcVCWwLcyH9x7cGdeNPPdSYcjXdNO+5SwdU7xaeaSINy4JOPB5rMwmHoMmPrbZYatk4fwKcmyoBQJEj/2ZqEfRgxk2BtNm5x874M8I5eRV3PyzOXkmVdCnj32r5FvlJN/gyO5A/oT02Y7GeSukbs9c0dUiZgGJeoJDjqf6SofdByMBg6yxKeyks1VJRs1PmoGH3U2h/JWVt4mfwAn/oXAhQSALclb9gHA4iIA69pEywFGyCb1HEBqQlUkKVRBumIOIy4Uxi2IOWwzewhsSzZ3YO/RnqNV0PahqTRV0Z6hldBqaDuY00Y7RNtCW0erY84JO5YvHxxQVSjRYFd13uxv4GarXIvES/v/YeOaTXpJNHdmLvyqrCSYutGRFUaB4xOQM7IO/cmaxyfuizOLickVdT8iYCusIUB+GD773qqswkdIAL3FKozc0hAD3YdFVSkWKik1DaOHAqet4/viXvBlI0BcqAQojkCF9uZOFIVbAQmceCkAUyeGF9N66T2LldxVoZmxI1J0npzCakHejrcaeSF42ypV2EH+evf859497HikLwrZt2nXP9CxodeaQtMbSp6TiTOBPWGzSnFoaykOp4C4WpFfhcsVdYp4lg//Cb+WX6/gqVXU0SvyTyryjfG3nyIKQhh9os55sAiXaDSgn8j0XrQMr1DkvWgRP5BfRvZQgQEtEWFAizoM0KEUA3igxoBVCDKrWtRkxqooy2ypA2VmS+2Ls01evdVvr85qQca1dw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(fill_line(color="black"))
        self.add_program_line(single_route(color="black"))
        self.add_program_line(grid_color_connected(color="black", adj_type="line"))
        self.add_program_line(nori_adjacent(("le", 2), color="black", adj_type=4))
        self.add_program_line(avoid_checkerboard(color="black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            self.add_program_line(f"hole({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="black", adj_type=8))

        for (r, c, _, _), color in puzzle.surface.items():
            if color == Color.GRAY:
                self.add_program_line(f"hole({r}, {c}).")
            else:
                self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
