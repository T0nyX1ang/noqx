"""The Kurarin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_type
from noqx.rule.neighbor import adjacent, count_covering
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route


class KurarinSolver(Solver):
    """The Kurarin solver."""

    name = "Kurarin"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7Vbrb6M4EP+ev2Llr2vpsM0rSPch7bZ7u5emyZKo1yAU0ZQ2dKH0CKR7RPnfd2xShcdk1Z5O95BOhGH4zTAPO/7Z69+LIAsp0+RP2BSecOnMVje3TXVr+2sa5XHovKODIl+lGSiUXo7oXRCvQ/r5ejU8TQfPHwa/bex8PmcfteKTdvVw/vD+S/Lrp0hk7Hxkjy/GFxG/H/xyejIxz96b42I9y8PNJGEnD7P59G58dd/nf5yN5no5v9SMz/O7nzaD2c89b1+C39uWfaec0PKj4xFOqLoZ8Wk5cbblhVNe09IFE6G2T0lSxHm0TOM0Iwpj4DcEjRHKQT07qFfKLrXTCmQa6KO9Duo1qMsoW8bhwnUrz7HjlVNKZPIT9blUSZJuQpkNvlPvyzS5iSRwE+QwfOtV9ESoAMO6uE2/FntX5u9oOahacF/Tgq6CvLQg1aoFqSEtyHprLQyrQH9lB31/t4PZ+QI9LBxPtjM7qPZBdZ0tyJGSTMlrZ0uEgDAccjWGmIg+wKwDM8NEca5L3OjihnUEl/ER3OJoOdyWZSL+fQ2tR2gM9Rca3q7O8fp1YeP+lsyL+Ft4Xt2WfXVxQ5PxEZzj42boeF6T4eNpch0dH1NIvNuXaR2J08f7sjS8L4vhdVoM78viR+KovyeGGziu4+NpGVj9sATO1ULgSk5hndBSKPlBSU1JQ8mh8jlT8krJUyV1JU3lY8mV9sq1SOSSseVfBh7dhfnW2iAcxOtDQAEbCnQrlKbDPItX1u2Bv9yFmpfx38P8nkfcIrsLliEw6TB6DN+N0iwJYnhzV8FTSGA7I+s0Xqwrr0X4LVjmxKl21LqlgT0WyU0I20ENitP0KYYESIQXUwOM7h/TLERNEgxv74+FkiYk1E2a3bZqeg7iuNmLOmw0oGodNKA8g72m9h5kWfrcQJIgXzWA2r7UiBQ+tgYzD5olBl+DVrbkMBy7HvlG1O0JyuV0/n/2+DefPeRMaX/6BPLPkLBXDl+YkpaXlDwVi2ABI07gqEtfjECeuNEUHDfoXLzVIMy35jj2BewAmMEFQwuHeVS41cJ1/2+fJrX40+wHTHwwtmGEjwH9ASXXrBh+hH1r1jbeoVpZbJdtAUUIF9A25wLUpV0AO8wL2BHylVHb/CuralOwTNVhYZmqTsSe3/sO",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(fill_line(color="not gray"))
        self.add_program_line(single_route(color="not gray"))
        self.add_program_line(grid_color_connected(color="not gray", adj_type="line"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(
                not (d == Direction.CENTER and symbol_name == "circle_SS__5"),
                f"Gray circle cannot be placed in the center of ({r}, {c}).",
            )
            target = 2 if d == Direction.TOP_LEFT else 1

            if d == Direction.CENTER and symbol_name == "circle_SS__1":
                self.add_program_line(f"not gray({r}, {c}).")

            if d == Direction.CENTER and symbol_name == "circle_SS__2":
                self.add_program_line(f"gray({r}, {c}).")

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__1":
                self.add_program_line(count_covering(("lt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__2":
                self.add_program_line(count_covering(("gt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__5":
                self.add_program_line(count_covering(target, (r, c), d, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="gray"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
