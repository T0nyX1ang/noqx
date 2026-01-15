"""The Ant Mill solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.variety import nori_adjacent


def ensure_antmill_loop(color: str = "gray") -> str:
    """A rule to ensure the shaded 1x2 rectangles form a single loop."""
    rule = f"adj_count(R, C, N) :- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_x(R, C, R1, C1) }} = N.\n"
    rule += f":- grid(R, C), grid(R1, C1), {color}(R, C), {color}(R1, C1), adj_count(R, C, N), adj_count(R1, C1, N1), adj_4(R, C, R1, C1), N + N1 != 2."
    return rule


class AntMillSolver(Solver):
    """The Ant Mill solver."""

    name = "Ant Mill"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VXvb6JMEP7uX/Fmv3aTY/klkrwf1Npee9baqvGUEIMWlRZcD8H2xfi/d3axkQVsmsv9eC+5IMPwPMvM7Ex8dvMtdkIXE4n9FAPDEy6VGPyWDZ3f0uHqe5Hvmv/gehwtaQgOxrcdPHf8jYuvR8t2k9afz+tft0Y0HpNLKb6Sho8Xj2f3wZcrTwnJRcfo3nRvPHlR/9xs3OmtM70bbwaRu70LSONxMO7Pu8NFTf6v1RmryfhW0q7H80/b+uDfinUowa7skpqZ1HFyaVqIIIxkuAmycXJn7pIbMxnhpAcUwoaNURD7kTejPg0Rxwisa6cfyuC2ju6Q88xrpiCRwO8cfHBH4NKXSSN965pW0seI5W3wL5mLArp1WSJWF3uf0WDqMWDqRNC5zdJbI6wAsYkf6FN8WErsPU7qafW9D1YPQd6qZ25aPfNKqmebYtXPvHDmu5P2j99Bzd7vYTD3sIeJabHtDI6ucXR75g5sh1vC7cjcIVWVIY6Kj+1FqlYCVQuQruUhTZKKkFGAiAKQIkByAdIVllGE1EIsnZcqrtJJflVVqhUgwmIJH1blwrarCqsrA0HTLnjrZG770FmcKNyecytxq3Hb5mta3A65bXKrcqvzNVU2mw9ODynQXhl2CA+DFQeP4kR/UomWkqqTeGl/HmZXLNSLw7kzc+Fv1ls6axeBsKEN9SebFJ+4L84sQmaqrVlGwFZxMHVBHTKQT+na91ZlEd4oAfQWKxq6pRQD3YfFqVCMKgk1peFDrqZnx/fFvfBjR4BSdRKgKATpybw7YUifBSRwoqUAZGRKiOSucs2MHLFE58nJZQuO7dhX0AviN/xfZTbAv6fQ//QUYkOSvvss+j3iakHDVQ0ntxit44kzgWZDv6o2LidgKIzQpRyhHYiqmidqByIfSof58FAkT8BsSnPoMMbSHDqMozyHeiqHdiLHIcUpHE6Bj61/q0gprP/l8+eCQsN31P1I5uESjQf0HZnPsGX4CUXPsHm8IN+s2KKCA1oi4oDmdRygopQDWFBzwE4IOoua13RWVV7WWaqCsrNUWXG37Mor",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(nori_adjacent(color="gray", adj_type=4))
        self.add_program_line(ensure_antmill_loop(color="gray"))
        self.add_program_line(grid_color_connected(color="gray", adj_type=8))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            if d == Direction.TOP and r > 0:
                if symbol_name == "ox_B__3":
                    self.add_program_line(f":- gray({r}, {c}), not gray({r - 1}, {c}).")
                    self.add_program_line(f":- not gray({r}, {c}), gray({r - 1}, {c}).")
                if symbol_name == "ox_B__4":
                    self.add_program_line(f":- gray({r}, {c}), gray({r - 1}, {c}).")
                    self.add_program_line(f":- not gray({r}, {c}), not gray({r - 1}, {c}).")

            if d == Direction.LEFT and c > 0:
                if symbol_name == "ox_B__3":
                    self.add_program_line(f":- gray({r}, {c}), not gray({r}, {c - 1}).")
                    self.add_program_line(f":- not gray({r}, {c}), gray({r}, {c - 1}).")
                if symbol_name == "ox_B__4":
                    self.add_program_line(f":- gray({r}, {c}), gray({r}, {c - 1}).")
                    self.add_program_line(f":- not gray({r}, {c}), not gray({r}, {c - 1}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
