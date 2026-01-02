"""The Shingoki solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import direction, display, fill_path, grid, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.loop import loop_segment, loop_sign, loop_straight, loop_turning, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected


def count_shingoki(target: int, src_cell: Tuple[int, int]) -> str:
    """
    Generate a constraint to count the length of "2-way" straight lines.

    A shingoki loop rule should be defined first.
    """
    r, c = src_cell
    rule = f':- segment({r}, {c}, N1, N2, "T"), |{r} - N1| + |{c} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "V"), |{r} - N1| + |{r} - N2| != {target}.\n'
    rule += f':- segment({r}, {c}, N1, N2, "H"), |{c} - N1| + |{c} - N2| != {target}.\n'
    return rule


class ShingokiSolver(Solver):
    """The Shingoki solver."""

    name = "Shingoki"
    category = "loop"
    aliases = ["trafficlights"]
    examples = [
        {
            "data": "m=edit&p=7VZtj6JIEP7ur9j01+3kaEAGSe6D4+re7jmOs6PxRmIMOqjMgHgIzhxm/vtWFXq8NG5uc5fNXXJByuKporpe4Gn2vydO5HKh4E8zOfzDoQuTTtU06FROx8iLfdd6x9tJvAkjUDi/7fX4yvH3Lv/8sOl3wvbLh/ZvBzOeTsVHJfmkTJ56T++/BL9+8rRI9Abm8GZ446nr9i+d6zuj+94YJvtx7B7uAnH9NJ6OVsPJuqX+0R1M9XR6qzQ/T1c/Hdrjnxv2KYdZ45i2rLTN04+WzVTG6RRsxtM765jeWOmAp/dgYlwA1gdNMK6C2s3VCdlR62SgUEAfnHRQH0BdetHSd+f9DBladjriDNe5prtRZUF4cFl2G10vw2DhIbBwYmjVfuPtTpZ98hg+JydfCMiCxI+9ZeiHEYKIvfG0nZXQrylBy0tANSsBtZoSsLK/XYLvbd3Xuuxb9dm/wWS+QP5zy8ZSxrlq5uq9dQQ5sI5MN/BOGJ7IxseaKgJ6DhjiBOhn4AoBI/e4Ot9y9jCVStCWhkAz9xBKdRmh6IhoBUQ935UjZtVHqy4lNCmOQT5/rgWVC6r/AerXmmBTod/FGWVdAe8ySq2RUOqPFMHAuE0JxdZJKPVPikBNlHxbuJqUA/VXipA1WXLOOi1FFqI25WwKNTCOQoZpHvKSNBQZ1uvz1lu1sWmOFRjG2KNhqiRH8HzzVCP5gaRCskmyTz5dkhOSHZI6SYN8rvAN+a53qPg8fW86zNBgRi2TMw2IH2arkaZDu7S/mKoN/rhblI/mfw+bNWzWB7Z7NwijwPGB8wZJsHCj/Pp+4+xcBnsP24f+fJ9EK2fpzt1XZxkzK9v+ipYStqVYJcgPwx3Sa02Es6kEeuttGLm1JgTdx/WlUGiqCbUIo8dKTi+O75droU+DEpQ9/yUojmCzKFw7URS+lJDAiTcloLA3liK520ozY6ecovPsVFYL8na8Ndgro9PWuPr/h8K/+UMBp6T8MKr7Z5jXhmYDZ/L0lrNdMnfmUBSDx4yj4USil43Aq5LxhxdIr0wYfYO/cmMVrmExQL9BZAVrHX6BswrWKi4RFCYrcxSgNTQFaJWpAJLJCkCJrwC7QFkYtcpamFWVuHApibtwqSJ9IRf4znZJPM9mja8="
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line(shade_c(color="shingoki"))
        self.add_program_line(fill_path(color="shingoki"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="shingoki", adj_type="loop"))
        self.add_program_line(single_loop(color="shingoki"))
        self.add_program_line(loop_sign(color="shingoki"))
        self.add_program_line(loop_straight(color="shingoki"))
        self.add_program_line(loop_turning(color="shingoki"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            self.add_program_line(f"shingoki({r}, {c}).")
            self.add_program_line(loop_segment((r, c)))

            if symbol_name == "circle_L__1":
                self.add_program_line(f":- turning({r}, {c}).")
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count_shingoki(num, (r, c)))

            if symbol_name == "circle_L__2":
                self.add_program_line(f":- straight({r}, {c}).")
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count_shingoki(num, (r, c)))

            if symbol_name == "circle_L__5":
                num = puzzle.text.get(Point(r, c, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count_shingoki(num, (r, c)))

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_io", size=3))

        return self.program
