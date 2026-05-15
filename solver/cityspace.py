"""The City Space solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import border_color_connected, bulb_src_color_connected, count_reachable_src, grid_color_connected
from noqx.rule.shape import all_rect, avoid_rect


def constrain_rect_shape():
    """Constrain rectangle shapes for City Space."""
    rule = f':- rect(R, C, "{Direction.BOTTOM_RIGHT}").\n'  # the shapes should be 1xn
    rule += f':- rect(R, C, "{Direction.TOP_LEFT}"), not rect(R, C + 1, "{Direction.TOP}"), not rect(R + 1, C, "{Direction.LEFT}").'  # the shapes cannot be 1x1
    return rule


class CitySpaceSolver(Solver):
    """The City Space solver."""

    name = "City Space"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VRtb9owEP7Or6j8tZaWN94iTVNKoWtHU1pArEQRMjRA2gQzJ6FdEP+9ZwcWEkK1aVO3D5PJ6e45+3x35p7gW0SYg6uw1BqWsAxLlTTxVST+262eG3qOfoKNKJxTBgrGN60WnhIvcPDV/bzdoMbzufF1VQuHQ/lCii6lwWPr8fTO/3LpqkxumbXOdefaVWbG58bZbaV5WulEQT90Vre+fPbYH/amncGsrnxvmkMtHt5I5avh9MPK6H8sWdsc7NI6ruuxgeML3UIKwtvPxvGtvo6v9djEcRdcCMs2Rn7khe6EepShHRa3QZMRVkBtpupA+LnWSEBZAt3c6qDegzpx2cRzRu0E6ehW3MOI330mTnMV+XTl8MvgmLAn1B+7HBiTENoXzN0lwio4guiBPkXbrbK9wbGRVNDdVaC9XQEE2VXA1aQCrhVUwAv7/Qq8JS3IvW5vNvAsd5D9SLd4If1UraVqV1+DNPU1UjQ4qsL/DI5DNFXKmBo3tdSsgln9YVa4V+Z/08SuqpndNe5Od9e5iT5BuTugkgEgIVmkdS9kS0hFyB5kjWNVyHMhJSHLQrbFnqaQAyEbQmpCVsSeKq/7JzsjeqJAL8pI15I2vUNulsI7l67yn7fskoW6EZuSiQP/JzPyxw47MSnziYdgmlFAvVGQ+EfOC5mESE8IZd+TwRYiRgbyKF167qIows6VAd3ZgjKn0MVB52F2LBR3FYQaU/aQy+mZeF62FkG0GSgZxwwUMpi1PZswRp8ziE/CeQbYY5ZMJGeRa2ZIsimSJ5K7zU/bsSmhFyQ+mE2FP+R/6v0nqZc/kfRLBPz3Wc+CVgP3xDcYLaMRGUGbRac4rpZzOJRdiMMjFeLlI7hiv3sXxFBR9gbDpc48XMBzgL5BdXveIvwIq+158/gBhfFkD1kM0AIiAzTPZQAd0hmAB4wG2BFS41HzvMazylMbv+qA3fhV+wQHQ0lg4OzSKw=="
        },
        {"url": "https://pzplus.tck.mn/p.html?cityspace/9/9/g2h4h2l6r6g5k6oakbg9r6l2h2h4g", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="not black", adj_type=4))
        self.add_program_line(border_color_connected(puzzle.row, puzzle.col, color="black", adj_type=8))
        self.add_program_line(avoid_rect(2, 2, color="not black"))
        self.add_program_line(all_rect(color="black"))
        self.add_program_line(constrain_rect_shape())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="not black", adj_type=4))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
