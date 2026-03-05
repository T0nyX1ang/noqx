"""The Mochinyoro solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, grid_color_connected
from noqx.rule.shape import all_rect, avoid_rect, count_rect_size, no_rect


class MochinyoroSolver(Solver):
    """The Mochinyoro solver."""

    name = "Mochinyoro"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVRa9swEH73ryj3fA+WZDuOX0bWNXvJ0m3JKMWY4HguDXNw5sRjKPi/73R268ltoYGRwRi2Pr473UmfT+i8/16nVY5CmFeF6CIx9PyAhxCSh9s9y82hyKMLnNSH+7Iigng9neJdWuxzJ+6iEueox5GeoH4fxSAAQdIQkKD+FB31h0jPUS9oClCQb9YGSaJXPb3hecMuW6dwic87TvSWaLapsiJfzVrPxyjWSwSzz1vONhS25Y8cOh3GzsrtemMc6/RAH7O/3+y6mX39tfxWw8MWDepJK3fxIFf2clUvVz3KVc/LlX9EbrErnxM6TpqGCv6ZpK6i2Kj+0tOwp4vo2BhFR1CBSX1DKtpTAU+SQ/TmiEz5aPpqEB54A8fItfJDYeWH9nJjaZuhlSvcsTUthG/bMrDjlb2cUPZuwlO27Xu2HbiDjxEj8cQzWDM0e3q/2aGVQWUWXOxbximjZFzSWaBWjO8YXUafccYxV4w3jJeMHmPAMSNzmq88bzDFkQiKauC1h38GbbGS3EOGj//vehMnhkVd3aVZTld0Xm/XeXUxL6ttWgB1w8aBn8AjVhTu/W+QZ2+QpvjuSW3y79/imOpKd0lfI+zqVbrKygLo74rsVy/4T40/1f90/bNXjVpM4vwC",
        },
        {
            "url": "https://puzz.link/p?mochinyoro/17/17/hdzmenajfzh71zw4zu6i5zu3zw-108zh2jcn9zmbh",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(invert_c(color="black", invert="white"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="not black", adj_type=8, grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(all_rect(color="white"))
        self.add_program_line(no_rect(color="black"))

        all_src: List[Tuple[int, int]] = []
        tag = tag_encode("reachable", "bulb", "src", "adj", 4, "not black")
        fail_false(len(puzzle.text) > 0, "No clues found.")
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="not black"))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_rect_size(num, (r, c), color="not black"))

            all_src.append((r, c))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
