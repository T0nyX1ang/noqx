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
            "data": "m=edit&p=7VbBjpswEL3zFas5+4BtIMSXKt1ue0nZtkm1qiwUEcpqoxLRktBWjvj3jsdkEaugzWWjVqocz4wfL8MbT2xl96PJ6oJx335kzNDjCHhMU8QRTb8by82+LNQVmzX7h6rGgLHbhN1n5a5gnu5YqXcwU2VmzLxTGjgwEDg5pMx8VAfzXpmEmQU+AhYjNnckgeFNH97RcxtdO5D7GCddjOEXDPNNnZfFau6QD0qbJQP7ntf0bRvCtvpZQKfDrvNqu95YYF3+euiwXfO1+tbAY3LYNuV+k1dlVQNl4mnLzMyJXxzFi1687MXLR/HytHjxkuKnp8W32JJPKH+ltK3kcx/GfbhQB5A+qJiBnJCL3CqSzkXk4ik57rslF91ais6Hzoex85Fdt7Z8l17DK9TkfhD0ogEQ+cc2HAH5FIgsEPaAFaQh6AGSNshKIgdZSO6QY4UPElMJQ04UDhAsi6tDaxtq7VuyguwSN5UZSfYNWZ9sSHZOnBuyd2SvyQZkI+JMbFvObhxKFQxCrCpwm30BbVq662I4wn8PSz0Ni6a+z/ICT1XSbNdFfZVU9TYrAa+z1oPfQFNLJiz9/w33191wtj3+mcflYifkGTka9zoUzNwy+N6sshXWRJt1EhcjuOxwOcIfw/lInqd4x8c/B+fxgxGd4UieaIQ/GeHH6cW7iFdd6v0B",
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
