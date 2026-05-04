"""The Mid-loop solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_straight, route_turning, single_route


def midloop_constraint(r: int, c: int, d: str) -> str:
    """Generate a white constraint."""
    rule = ""

    max_u = f"#max {{ R0: grid(R0, {c}), turning(R0, {c}), R0 < {r} }}"
    max_l = f"#max {{ C0: grid({r}, C0), turning({r}, C0), C0 < {c} }}"
    min_r = f"#min {{ C0: grid({r}, C0), turning({r}, C0), C0 >= {c} }}"
    min_d = f"#min {{ R0: grid(R0, {c}), turning(R0, {c}), R0 >= {r} }}"

    if d == Direction.CENTER:
        rule += f':- line_io({r}, {c}, "{Direction.TOP}"), line_io({r}, {c}, "{Direction.BOTTOM}"), Ru = {max_u}, grid(Ru, _), Rd = {min_d}, grid(Rd, _), {r} - Ru != Rd - {r}.\n'
        rule += f':- line_io({r}, {c}, "{Direction.LEFT}"), line_io({r}, {c}, "{Direction.RIGHT}"), Cl = {max_l}, grid(_, Cl), Cr = {min_r}, grid(_, Cr), {c} - Cl != Cr - {c}.\n'

    if d == Direction.TOP:
        rule += f":- Ru = {max_u}, grid(Ru, _), Rd = {min_d}, grid(Rd, _), {r - 1} - Ru != Rd - {r}.\n"

    if d == Direction.LEFT:
        rule += f":- Cl = {max_l}, grid(_, Cl), Cr = {min_r}, grid(_, Cr), {c - 1} - Cl != Cr - {c}.\n"

    return rule


class MidLoopSolver(Solver):
    """The Mid-loop solver."""

    name = "Mid-loop"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VRNj9MwEL3nV6zmPIfYzvetLFsuZRdo0aqKoipbghqRkpI2aOUq/53xJKUgHGkXViuQkOuX1zeOMx/27L+0eVOgcM1PRUhPGp6IeMoo4OkOY1EeqiK5wEl72NQNEcSb6RQ/5tW+QCcdlmXOUceJnqB+laQgAXkKyFC/TY76daKXqOdkAhQZwratDuW6ruoGTpqeEROAkujVmd6y3bDLXhQu8euBE10SXZfNuipW83kvvUlSvUAwH3/BrxsK2/prAf17/H9db+9KI9zlBwpxvyl3gIoM+/ZD/amF0yc61JM+hNlDQvB4k1MI6nsIyh6CfJIQqvJzcW/xPs66jirzjvxfJakJ5f2ZRmc6T46dccmgYFwmRwhC2kbij76RuxBGVjmKrbJQakT3rbrnuyO6GNGlXY89q+579vWBtK8P1Ig+4mcQ2f0MYnu8obDnLbTuT5WZcn0k44LKh1oxvmR0GX3GGa+5YrxlvGT0GANeE5oD8NtH5LHugGeyHEdUHukPJECPzpl6oKep6tvVz8P/97TMSWFG1/bium62eUU3er7JdwVQJ+0cuAeeqUL5v7n+zc3VVMl9tvvzNNc5pWQP9w71DcKuXeUryjbQUcM/MwbSfaSBOsKYwf/F8OyJpIaTOd8A",
        },
        {
            "url": "https://puzz.link/p?midloop/18/10/jd9flfzxfnfjfzp7f7fhfzzzbfzvflf3fzzpffzv3b7fififzznfjfgfzi9fgbbfzifufrf",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))

        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_turning(color="white"))
        self.add_program_line(route_straight(color="white"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(symbol_name.startswith("circle_SS"), "Invalid symbol type.")

            if d == Direction.CENTER:
                self.add_program_line(f":- not straight({r}, {c}).")
                self.add_program_line(midloop_constraint(r, c, d))

            if d == Direction.TOP:
                self.add_program_line(f':- not line_io({r}, {c}, "{Direction.TOP}").')
                self.add_program_line(f':- not line_io({r - 1}, {c}, "{Direction.BOTTOM}").')
                self.add_program_line(midloop_constraint(r, c, d))

            if d == Direction.LEFT:
                self.add_program_line(f':- not line_io({r}, {c}, "{Direction.LEFT}").')
                self.add_program_line(f':- not line_io({r}, {c - 1}, "{Direction.RIGHT}").')
                self.add_program_line(midloop_constraint(r, c, d))

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
