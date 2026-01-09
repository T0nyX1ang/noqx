"""The Nagareru-Loop solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import directed_route

dict_dir = {"1": Direction.LEFT, "3": Direction.TOP, "5": Direction.RIGHT, "7": Direction.BOTTOM}
rev_dir = {
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
    Direction.TOP: Direction.BOTTOM,
    Direction.BOTTOM: Direction.TOP,
}


def nagare_wind(r: int, c: int, d: str, puzzle: Puzzle) -> str:
    """Generate a constraint for the wind direction."""
    if d in (Direction.LEFT, Direction.RIGHT):
        cols = range(0, c) if d == Direction.LEFT else range(puzzle.col - 1, c, -1)

        c1, c2 = cols[0], cols[-1]
        for c_ in cols:
            if puzzle.symbol.get(Point(r, c_, Direction.CENTER)) or puzzle.surface.get(Point(r, c_)):
                c1 = c_ + cols.step
        if d == Direction.RIGHT:
            c1, c2 = c2, c1
        return f':- white({r}, C), {c1} <= C, C <= {c2}, not line_out({r}, C, "{d}"), not line_in({r}, C, "{rev_dir[d]}").'

    if d in (Direction.TOP, Direction.BOTTOM):
        rows = range(0, r) if d == Direction.TOP else range(puzzle.row - 1, r, -1)

        r1, r2 = rows[0], rows[-1]
        for r_ in rows:
            if puzzle.symbol.get(Point(r_, c, Direction.CENTER)) or puzzle.surface.get(Point(r_, c)):
                r1 = r_ + rows.step
        if d == Direction.BOTTOM:
            r1, r2 = r2, r1
        return f':- white(R, {c}), {r1} <= R, R <= {r2}, not line_out(R, {c}, "{d}"), not line_in(R, {c}, "{rev_dir[d]}").'

    raise ValueError("Invalid direction.")


class NagareSolver(Solver):
    """The Nagareru-Loop solver."""

    name = "Nagareru-Loop"
    category = "route"
    aliases = ["nagareru"]
    examples = [
        {
            "data": "m=edit&p=7VdtT9tIEP7Or6j8tZbO++JX6T4ECr32QhoKiCMWikwwEOpgznGAM+K/d2d20jjx0Lv7cBLSoST78szs7LPj3cfZ+Z+LrMpd6cFXRa7nCvMJ4wh/kS/w59HnaFoXefLO7S3q67IyDdf9srfnXmbFPHc/n173d8rew4feH/dRPRqJj97ik3dys3fz/uvs909TVYm9QTTcH+5P5VXvt53tg2D3fTBczI/r/P5gJrZvjkdHl8OTq1j+tTsY6Wb0xfM/jy5/ue8d/7qVEoezracmTpqe23xMUkc6Lv6Ec+Y2B8lTs580p25zaEyOqw3WNy3huNI0d1fNE7RDa8eCwjPtAbVN89Q0s6oqH8bb423rOUzS5sh1YKJtHA5NZ1be544dh/1JOTufAnCe1SZX8+vpHVnmi4vy24J8zRzObFHU00lZlBWAgD27Tc+uob9cA5ChNajVGqBp1wAtZg1AGNYwmVaTIh/3baB/uYT84ip/5NjHPPtn82i+Gv7jJIWlHK+a0ap5mDw5fugk2nUCgVVoe5FvK9uLPVtFWAnPugrPOgkvtrVQtpaSajtaSLIrG0YosivyVxRHkb8mPx3YmhiKkMaFNC4ke0i8QponIntEeER4bOeRnrVL4i2FnU9Kuy4pyY/4S2njSOIpNY3X2ta+5SVD6hMvSbmUxEtG5EfJVcRDeXaconwqQX2x7Ns4Stg4Slq+ivgqyreSFE8Rrpc1jfdpHPFVAc0TWL6K8qRissdkj8keW7v2rF1T3rSw82h6/pp4a2HzpomfpnxqyqdWFI94ap/6AcUNaFxA40LCQ/KnfaApz5q2qY5t3yd+vrD8feLjUx59zJc5BYPkyZQCy1NzIiBeKtwfmnOCR9iBx5j6K9hKER4OxhuSyHlDENWB8UylYScKniEWhzgMDnuUYYNni/OHs8b5wzNp+y95wplsL2vpD3ueiw9ns73eJR5B/G568Cwy/ngmmfh4RjkctIbJs4SzwaxLgha18/AD34i/xGFPcv4BrJfBQRs4ni/kDc88kwfUAA4HTWBxWC+Hw/bkcMhzN2+oKcxzR43hcNAWZl+pCHh286ngzDI4ag3DE7WFiY9aw/BBTWHyrAP+PKK2cHHgncLsW9Qejie8c5j94Hv8/kFN6sQxurSH6iSxPDIvb7dRWH7A0sPSx7KPPrtYnmC5g6XGMkCfEF7///APQlcg/yM6qW//7/79x3/ze/P7//mdbaXO4aK6zCa5uQj0p7f5u0FZzbLC9A6vs7vcMfcxZ14W47n1GueP2aR2EnslbFvWsNvF7Dw3N4cWVJTlXWEmYCIsTWvg9Oq2rHLWBCBcXl4IBSYm1HlZXWxwesiKYn0teF1eg+wVaw2qK3N/avVRWdeQWVZfrwGt6+JapPx2I5l1tk4x+5ZtzDZbpeN5y3l08GcEXpgL8dvl+fVenuExea/tDfna6OAOL6ufyM3KuAkzomPQn+hOy8rhL0hMy7qJd/QEyHYlxaCMqhh0U1gM1NUWA3bkxWAvKAxE3RQZYLWpMzBVR2pgqrbapGdb3wE=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white", directed=True))
        self.add_program_line(adjacent(_type="line_directed"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line_directed"))
        self.add_program_line(directed_route(color="white"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            shape, style = symbol_name.split("__")
            _d = dict_dir[style]

            if shape == "arrow_B_B":
                self.add_program_line(f"white({r}, {c}).")
                self.add_program_line(f'line_in({r}, {c}, "{rev_dir[_d]}").')
                self.add_program_line(f'line_out({r}, {c}, "{_d}").')
            if shape == "arrow_B_W":
                self.add_program_line(f"not white({r}, {c}).")
                self.add_program_line(nagare_wind(r, c, _d, puzzle))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"not white({r}, {c}).")

        self.add_program_line(display(item="line_in", size=3))
        self.add_program_line(display(item="line_out", size=3))

        return self.program
