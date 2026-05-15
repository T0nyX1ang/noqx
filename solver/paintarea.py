"""The Paintarea solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_same_color, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect


class PaintareaSolver(Solver):
    """The Paintarea solver."""

    name = "Paintarea"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZRRb9MwFIXf+ysmP/shduLYzgsqo+WldECL0BRVVdplrKJVRroglKr/nWPnuqnQpIGA8YKy3B3fnNo3X669/9IUdck1rtjwiAtccZT4O43cX7jmm4dtmV3wYfNwV9UQnF+Nx/y22O7LQU6uxeDQ2qwd8vZ1ljPBOJO4BVvw9l12aN9k7Yi3Mzxi3CA36UwSctTLj/65U5ddUkTQU9KQ15DrTb3elstJl3mb5e2cM7fOS/9rJ9mu+loyqsON19VutXGJVfGAl9nfbe7pyb65qT43LCxx5O2wK3f2SLlxX258Kjd+vFz598u1i+MR2N+j4GWWu9o/9NL0cpYdjq6uA5MKP3Vf2n8ZJq2b6QU7JVKBRHwamghDSUNMIfxE1z6OfZQ+zrEOb2MfX/kY+ah8nHjPCMuLWHGRpCyTmBFdJxLb6QR5RfkEeRXylos06rTS0IY0PCl5FDyaPOhaoQVp+DX5U3gMeTQ8hjwaL2di0pjT0Jwafkt+A48lj7FcRpS3ETTNYyU0eWwMnZBOoJXX8HIpJGnkhaJ3TMAh6BRak0b9iek5qMAB9StaV8GvdM8kcHMc0sAB3zuVPZPAMD1jqM+4OSY6MDljqM8YmjOGBvMb2bMKPMFH2MAHHitPfMCFOPQMPZ8o8Ol54v+JJ1hCuz45ut3n2urSx8TH1Lebdk3/k9uCyW7iGPxNt0d+v82frC2XiT9uw6X+/GgxyNmsqW+LdYmTY3TzqbyYVvWu2GI0bXarsg5jHNzHAfvG/O33fvL/LP9HZ7n7BNEvnejP0K1PlJODLo719oqz+2ZZLNcVegzsXB59/mP+2avHdlsMvgM=",
        },
        {
            "url": "https://puzz.link/p?paintarea/18/10/fesmfvrsi3vrvsntsvuttippjvnvrnvdferjbmtvtmnftnrnvrfbanmunev6vffddd8a1zj2b0t2b2a2c1o1d2b1c3zx2d2a2a3t",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(grid_color_connected(color="gray", adj_type=4, grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="gray"))
        self.add_program_line(avoid_rect(2, 2, color="not gray"))
        self.add_program_line(area_same_color(color="gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, (ar, _) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
