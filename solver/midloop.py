"""The Mid-loop solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import direction, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import loop_straight, loop_turning, single_loop


def midloop_constraint(r: int, c: int, d: str) -> str:
    """
    Generate a midloop constraint.

    A loop_turning rule should be defined first.
    """
    rule = ""

    max_u = f"#max {{ R0: grid(R0, {c}), turning(R0, {c}), R0 < {r} }}"
    max_l = f"#max {{ C0: grid({r}, C0), turning({r}, C0), C0 < {c} }}"
    min_r = f"#min {{ C0: grid({r}, C0), turning({r}, C0), C0 >= {c} }}"
    min_d = f"#min {{ R0: grid(R0, {c}), turning(R0, {c}), R0 >= {r} }}"

    if d == Direction.CENTER:
        rule += f':- line_io({r}, {c}, "u"), line_io({r}, {c}, "d"), Ru = {max_u}, grid(Ru, _), Rd = {min_d}, grid(Rd, _), {r} - Ru != Rd - {r}.\n'
        rule += f':- line_io({r}, {c}, "l"), line_io({r}, {c}, "r"), Cl = {max_l}, grid(_, Cl), Cr = {min_r}, grid(_, Cr), {c} - Cl != Cr - {c}.\n'

    if d == Direction.TOP:
        rule += f":- Ru = {max_u}, grid(Ru, _), Rd = {min_d}, grid(Rd, _), {r - 1} - Ru != Rd - {r}.\n"

    if d == Direction.LEFT:
        rule += f":- Cl = {max_l}, grid(_, Cl), Cr = {min_r}, grid(_, Cr), {c - 1} - Cl != Cr - {c}.\n"

    return rule


class MidLoopSolver(Solver):
    """The Mid-loop solver."""

    name = "Mid-loop"
    category = "loop"
    examples = [
        {
            "data": "m=edit&p=7ZVRb9owEMff+RSVX2tpcRJCiLQHSqFrRyktIAYRQgYCpE0wCwntgvjuPRsqSHCqdp2qTZpCjuN3xr47O/8sf0Y0cDBR+EczMXzDpRNT3KppiFvZXS039BzrBJeicMYCcDC+qVbxhHpLB191Z7UyKz2el36szLDXIxdKdKl07qv3p3f+90tXC0i1bjauG9euOi19K5/dGpVToxEt26GzuvXJ2X2715o0OtOi+qtS7+lx70bJX/UmX1al9tecvcuhn1vHRSsu4fjCspGKsLgJ6uP41lrH11bcxXETQgiTPkZ+5IXuiHksQC8sroFHEFbBrezdjohzr7yFRAG/vvPB7YI7coOR5wyazS1qWHbcwogvfib+zl3ks5XDV4P/id8j5g9dDoY0hP4tZ+4CYQ0Cy2jMHqLdUNLf4Li0LaH2lhJ0MclLCdzdlsA9SQm8so+X4Llz50mSfbG/2cDO3EH+A8vmpbT3rrl3m9YabF1YImzXWiOjANOosMw+N0gXFUwpNotSTDQtg+elXM8rGZxkcFXOi7qU53X5eEOVjze0DJ6Rp2HK8zSK8noLRN63gnR+2Jmq2B9V2BZsH441Yc+FVYTNC1sTYyrCdoQtC6sLa4gxBX4AfvuIvDcdpPMuF03YHhXaIRwD63DOtDdmamtbLUxe+X+P9XM2qsFje1JngU89eKKbM7pwECgpWjJvsIyCCR05A+eJjkJkbcX8MJJg88gfOqBEB8hjbMF1QTLDSygB3emcBY40xKEznmZNxUOSqYYsGKdyeqSel6xFvOgSaHveEygMQOUOftMgYI8J4tNwlgAHop6YyZmnmhnSZIr0gaZW8/ft2OTQExK3rWH1/2vvb37t8V1SPk3Z/ozQ2tDsnSLi+AajRTSgA+g2gqOGPxY0VOWdAdDqrED+KPDpjRSPJgte0cl9MI0lagn0FcE8iMp4hjYeRNP8SAh5ssdaCFQih0DTigjoWBQBHukisAxp5LOm1ZFnlRZIvtSRRvKlDmXSRr475sWjfu4Z",
        },
        {
            "url": "https://puzz.link/p?midloop/18/10/jd9flfzxfnfjfzp7f7fhfzzzbfzvflf3fzzpffzv3b7fififzznfjfgfzi9fgbbfzifufrf",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line(shade_c(color="midloop"))
        self.add_program_line(fill_line(color="midloop"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="midloop", adj_type="loop"))
        self.add_program_line(single_loop(color="midloop"))
        self.add_program_line(loop_turning(color="midloop"))
        self.add_program_line(loop_straight(color="midloop"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(symbol_name.startswith("circle_SS"), "Invalid symbol type.")

            if d == Direction.CENTER:
                self.add_program_line(f":- not straight({r}, {c}).")
                self.add_program_line(midloop_constraint(r, c, d))

            if d == Direction.TOP:
                self.add_program_line(f':- not line_io({r}, {c}, "u").')
                self.add_program_line(f':- not line_io({r - 1}, {c}, "d").')
                self.add_program_line(midloop_constraint(r, c, d))

            if d == Direction.LEFT:
                self.add_program_line(f':- not line_io({r}, {c}, "l").')
                self.add_program_line(f':- not line_io({r}, {c - 1}, "r").')
                self.add_program_line(midloop_constraint(r, c, d))

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
