"""The Skyscrapers solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, validate_direction, validate_type


class SkyscrapersSolver(Solver):
    """The Skyscrapers solver."""

    name = "Skyscrapers"
    category = "num"
    aliases = ["building", "skyscraper"]
    examples = [
        {
            "data": "m=edit&p=7VRNT8JAEL33V5A5z6G7/aQ3RPCC+AGGkKYhgDUQIdWWGrNN/7uzA7bU6MGDysG0+/LezGz37Uc3e87naYxC6Nfy0URiaDsuNyEkN/PwjNe7TRy0sJPvVklKBPGq38eH+SaLjVBwXxEZhWoHqoPqIghBAIKkJiBCdRMU6jJQQ1QjSgHVohrsiyTRXk0nnNesuw8Kk/jwwIlOiS7X6XITzwb7yHUQqjGCHueMe2sK2+QlhoMPrZfJdrHWgcV8R5PJVuunQybL75PHHN6HKFF1vrZr1Xatyq71uV3583bbUVnSst+S4VkQau93NfVrOgqKUvsqwLKpq037xTsDlkvSq6VP0qmkbTalzoIHVcCVFLAq6XuNj7V1VlZSCJ32ay1lU9tes97RebfWvtOwLng450i3j4an6Qqe9JSxzygZx7QmqCzGc0aT0WEccE2PccLYZbQZXa7x9Kp+a91/wU5o+yg+PN5pRSIjhGG+XcRpa5ik2/kG6NIoDXgFbnyU7P975I/uEb0F5qmd6lOzQ/9ZZLwB"
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")
        n = puzzle.row
        self.add_program_line(grid(n, n))
        self.add_program_line(fill_num(_range=range(1, n + 1)))
        self.add_program_line(unique_num(_type="row", color="grid"))
        self.add_program_line(unique_num(_type="col", color="grid"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")

            if r == -1 and 0 <= c < puzzle.col:
                self.add_program_line(f"blocked_t(R, {c}) :- number(R, {c}, N), number(R1, {c}, N1), R1 < R, N1 > N.")
                self.add_program_line(f":- #count {{ R: blocked_t(R, {c}) }} != {n - int(num)}.")

            if r == puzzle.row and 0 <= c < puzzle.col:
                self.add_program_line(f"blocked_b(R, {c}) :- number(R, {c}, N), number(R1, {c}, N1), R1 > R, N1 > N.")
                self.add_program_line(f":- #count {{ R: blocked_b(R, {c}) }} != {n - int(num)}.")

            if c == -1 and 0 <= r < puzzle.row:
                self.add_program_line(f"blocked_l({r}, C) :- number({r}, C, N), number({r}, C1, N1), C1 < C, N1 > N.")
                self.add_program_line(f":- #count {{ C: blocked_l({r}, C) }} != {n - int(num)}.")

            if c == puzzle.col and 0 <= r < puzzle.row:
                self.add_program_line(f"blocked_r({r}, C) :- number({r}, C, N), number({r}, C1, N1), C1 > C, N1 > N.")
                self.add_program_line(f":- #count {{ C: blocked_r({r}, C) }} != {n - int(num)}.")

            if 0 <= r < puzzle.row and 0 <= c < puzzle.col:
                self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
