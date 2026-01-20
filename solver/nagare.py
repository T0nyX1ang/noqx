"""The Nagareru-Loop solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false
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
            "data": "m=edit&p=7VjrT9tIEP/OX1H5a1c678OvSPchUOi1l/IoII5EKDLBgFsHc45DWyP+987MTpqHN1xBp7vTtUqyj9/Mzs6Md8azmfw5TatMKB+/Oha+kPCJkph+cSDp5/PnKK+LrPNCdKf1dVnBQIi9nR1xmRaTTLw9ve5tld1Pr7p/3MV1vy9f+9M3/smHnQ8v349/f5PrSu7sxvvv9t/l6qr729bmQbj9MtyfTo7r7O5gLDc/HPePLvdPrhL1ZXu3b5r+nh+87V/+ctc9/nVjwDqcbdw3SafpiuZ1Z+ApT9BPemeiOejcN+86zaloDoHkCQNYD0bSEwqG2/PhCdFxtGVB6cN4l8cwPIVhWlXlp+HmcNNy7ncGzZHwcKNNWo5Db1zeZZ5dR/NROT7PEThPa/DV5Dq/ZcpkelF+nDIv7OGNp0Wdj8qirBBE7EE0XbKBxcwMQY3YED03BIfWEBw5DEGt0ZBRXo2KbNizgp5oR5HfZBd5RZss25C4bXiAB/QerBh2BmjQ8XwYz4eHnXsviLyOEV4oqYvsLA5sZ2eJb7uYOulbVulbJukntpfa9kpxb1dLxXRtxUjNdM38muVo5jfMZ0Lbs4Yy4nURr4uYHrFeEe8TMz1mPGY8sfso39IV662k3U8pa5dSzMf6K2XlKNZTGV5vjO0Dq5eKeM56KfalYr1UzHzsXM16aN+u0+xPLXkuZ3MrR0srRyurr2Z9NftbK5anGTezntcHvI711SHvE1p9NftJJ0xPmJ4wPbF041u6Yb8Zafcx/PwN622k9Zth/Qz707A/jWZ5rKcJeB6y3JDXhbwuYjxifj4Hhv1s+JiaxM4D1i+QVv+A9QnYjwH5C6Jgt3MPraT2FCIC5Q2k+JZ5TiiGPXyMg2AO24REweHgRie6uFGIbsEUU4OoJYViyImjHAeOZ9ShDcWWix9jzcWPz2SRf6YnxuSiWTN+PPMu+Ribi/bO8Bjlt91Dsejgp5h0yKcYdeGYaxx+VhgbDrsU5qJFP3zDV+TPcDyTLv4Q7XXgmBtceq7xG8W8ww+UA1w45gQnjva6cDyeLhz93PYb5RTHc6cc48IxtzjOlY5Rz7Y/NcasA6dc49CTcotDPuUahz6UUxx+NqE7Him3uOTgO8Vxbin3uPTEd47jPAS++/xQTmrJgby0Q9lJUXsEL2/RaGpfUetTG1DbI55tak+o3aLWUBsST4Sv/+8sEBwJUip6LKHwoCqByrXI6y+zeKeAB0e3KDGtAdctU55qG24OZwuqYhQJ3kri7zR3ENiq+q8/wU++n3w/Ht/ZxsA7nFaX6SiD60cP4vTFblmN0wJmh9fpLaJb5fi2nOR15sEN0JuUxXBiVwyzz+mo9jr2ErpIWcJupuPzDG4pC1BRlrd4vXFImJGWwPzqpqwyJwnB7OJqnSgkOUSdl9XFik6f0qJYtoUu6EuQvc8tQXUFl7WFOWXxJWSc1tdLwMIFdUlSdrPizDpdVjH9mK7sNp6742HD++zRD14mEq7gP6/r//XrOj4s/9nv5H+nRBg0PYEvdtHsCe92OkyHYJUH/w6Jxyinj62B0uJpFJC2fg2UI0+jgLS/l/Icrf9XPvhxNOhhXS8CCPJ1D8+sDRT9DIHPIv7jGYReTWX1SJ0wJ67CjmoB0EcKhgWqC19TGyxQV/FWIYDKtmsBQB3lAKCrFQFA7aIAwFZdANia0gClrlYHqNVqgYBbtWoE3GqxTBicbXwF",
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
            shape, style = symbol_name.split("__")

            if d == Direction.CENTER and shape == "arrow_B_B":
                self.add_program_line(f"white({r}, {c}).")
                self.add_program_line(f'line_in({r}, {c}, "{rev_dir[dict_dir[style]]}").')
                self.add_program_line(f'line_out({r}, {c}, "{dict_dir[style]}").')
            if d == Direction.CENTER and shape == "arrow_B_W":
                self.add_program_line(f"not white({r}, {c}).")
                self.add_program_line(nagare_wind(r, c, dict_dir[style], puzzle))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"not white({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            if label == "normal" and not draw:
                self.add_program_line(f':- line_in({r}, {c}, "{d}").')
                self.add_program_line(f':- line_out({r}, {c}, "{d}").')

            if label in ["in", "out"] and draw:
                self.add_program_line(f':-{" not" * draw} line_{label}({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_in", size=3))
        self.add_program_line(display(item="line_out", size=3))

        return self.program
