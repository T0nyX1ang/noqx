"""The San-Anko solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Point, Puzzle
from noqx.rule.common import defined, display, fill_num, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, general_shape


def ensure_same_number_adjacent(adj_type: int = 4) -> str:
    """A rule to ensure two adjacent cells having the same number."""
    return f":- number(R, C, N), number(R1, C1, N1), adj_{adj_type}(R, C, R1, C1), N != N1."


class SanAnkoSolver(Solver):
    """The San-Anko solver."""

    name = "San-Anko"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VbRT9s+EH7vX4H87IfYTpOQN8ZgLyxslAmhqKpKF0S1VmFp89NPqfjfuTuf1cSmGy9jQpra2O73Xa/3+bvE3fxs500lVYRvk0mY4RWrjC6dJXRF/LpebldVfiRP2u1D3cBCysvzc3k/X20qOSo5bDradcd5dyK7T3kplJBCw6XEVHZf8133Oe8mspsAJWQM2IUN0rA82y9viMfVqQVVBOvCrmMprjDdLXxcLJvFqppdQAQgX/Kyu5YCyQ+UAZdiXf9XCa4FPy/q9d0Sgbv5FhRtHpaPzGza7/WPlmMhoVi3q+1yUa/qBkHEnmR3YmUUTgaWyTLMXgYurQxcvSBDv42M45dlPIFNVyBklpeo6dt+me2Xk3wnjBY57LgxdkrslNKUWi61XGq51HJZZCdFk1Ixz2OeM56P7axtKqVtLjVmfsx8wnyCPJRWcGklthcSKByLdC1iAShpEIEVlyLpARQR9wAofwCggkFSqn0QQiqGCOoY/DIp8hD6Vj8zqushoFPlOxhvabwGV2RnaPxIY0TjmMYLijmj8YbGUxpjGhOKSdHXVzsPwrXbarDPdS2VGpOaHoAG9YA/VHpp7DNq+Bq/P2w6KsWkbe7niwru2qJd31XNUVE36/lKwCP0aST+F3SVBnbU/HuqvpOnKloWvfIOs/fW37nJS2gYo2V3KcVjO5vPQAftOeHGw2GvCU88HFqN8NTDxxZP/fwJ437+lHE/f8a4nx92H/Es8nBsBCKUT0ADIAHHkM+wZjiYfIZVw+PeZ1g3PPZ9hpXDceYzrB0OBp9h9XBA+Azrh4PCZ3gH4Fj0LeQtgKPEZ3gPQtcP2a4P+a4PGa9Zf+CMZvmBM9p5H6Ry5gc/ztqDLjIsPWg7c9B9c9B949wPXDHO/cAV49wPXDHO/cAV49wPusw494MuM879oMti537QZTHtQQHVy8GxvY+grxYyzn4TAOJ+FQBd4Xtspm/ywIN/B9PRMw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_num(_range=range(1, 4), color="not black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(ensure_same_number_adjacent(adj_type=4))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(all_shapes("omino_3", color="black"))

        for i, o_shape in enumerate(OMINOES[3].values()):
            self.add_program_line(general_shape("omino_3", i, o_shape, color="black", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"hole({r}, {c}).")

            if color == Color.WHITE:
                self.add_program_line(f"not black({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")

            if Point(r, c) in puzzle.surface:
                self.add_program_line(f":- #sum {{ N, R, C: number(R, C, N), |{r} - R| + |{c} - C| = 1 }} != {num}.")
            else:
                self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
