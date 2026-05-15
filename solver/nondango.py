"""The Nondango solver."""

from noqx.manager import Solver
from noqx.puzzle import Point, Puzzle
from noqx.rule.common import area, count, defined, display, grid, invert_c, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.shape import avoid_rect


def avoid_diagonal_3(color: str = "black") -> str:
    """Generate a constraint to avoid diagonal in a row of three."""
    rule = f":- {color}(R, C), {color}(R + 1, C + 1), {color}(R + 2, C + 2).\n"
    rule += f":- {color}(R, C), {color}(R + 1, C - 1), {color}(R + 2, C - 2).\n"
    return rule


class NondangoSolver(Solver):
    """The Nondango solver."""

    name = "Nondango"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7ZZNb9NAEIbv+RXVnvfg2Q/vrm+ltFz6AbQIVVYUpWmgFalS0gaQo/x33t1MiSymqgS0J2R58mQ8nn1nvOv13dfleDHVEYeNutKEwzpTTlOlclZ8nF3fz6bNjt5d3l/NFwCtTw4O9Kfx7G46aDlqOFh1qel2dfemaRUprQxOUkPdvWtW3VHTnevuFJeUJvgON0EGuL/Fj+V6pr2NkyrwMTPwHDi5Xkxm09HRxvO2abszrfI4r8rdGdXN/NtUsY78fzK/ubjOjovZ9yv23S0v51+W6iH5Wne7jwu1W6H2l1ArCzXPKTQN12u0+j2kjpo2q/6wxbjF02a1zoqypWLPm5UyNdI43ZemTJS8thK9VvQmyetI9DrR6yWvFzV4I3rlDGLFPkjeWuxDLdYWxCqCqCGIowVxtCCOFsU+RLG2KI4WxdGSmDeJzy2JXU/ifEjyaGJtVInDUSVmpkpsPJFYCZEomkjOTY/kFvtMJDQa6+ygrDZT7BkWo+5ssa+LrYr1xR6WmH2sS4p4AUdoNcgbDdgyW7BjdmDP7ME1cw0OzAEcmSM4FTaVxyu9Zq7BgTmAI3PMr31mbAG5pZmpAhMzgQ0ztgra6DQG8ZbjLeItx1vEW463iLccby3YMTuwZ4ZOyzotdFquyydNYZMTv/3+JO5J8v26iGuh1NfjWIODBs/31sgZOGew/T4n1pBCvz+Gcxrq1+W4Fgc9nu+tkTNwzuD7zyslzp/6fTYPvbX9/jiu0UGPz/eu84aUp9Jesa7YukyxkHeDv9wvjPi2p38x8Z9U3pq6fJtsD/+y/4eDVu1ffp7uHM8XN+MZtuTTq/HtVOF7Zz1QP1Q5Wzxd7f5/Ar3gJ1Bue/XHE/uZZusTclr0FfO5O9HqdjkajyZzzCd0Lftt+s3/4uqx3IaDnw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="circle_M__1"))
        self.add_program_line(invert_c(color="circle_M__1", invert="circle_M__2"))
        self.add_program_line(avoid_rect(1, 3, color="circle_M__1"))
        self.add_program_line(avoid_rect(1, 3, color="circle_M__2"))
        self.add_program_line(avoid_rect(3, 1, color="circle_M__1"))
        self.add_program_line(avoid_rect(3, 1, color="circle_M__2"))
        self.add_program_line(avoid_diagonal_3(color="circle_M__1"))
        self.add_program_line(avoid_diagonal_3(color="circle_M__2"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(1, color="circle_M__2", _type="area", _id=i))

        for r in range(puzzle.row):
            for c in range(puzzle.col):
                if puzzle.symbol.get(Point(r, c, label="normal")) == "circle_M__1":
                    self.add_program_line(f":- circle_M__2({r}, {c}).")

                elif puzzle.symbol.get(Point(r, c, label="normal")) == "circle_M__2":
                    self.add_program_line(f":- circle_M__1({r}, {c}).")

                elif puzzle.symbol.get(Point(r, c, label="nondango_mark")) != "circle_M__4":
                    self.add_program_line(f"hole({r}, {c}).")

        self.add_program_line(display(item="circle_M__1"))
        self.add_program_line(display(item="circle_M__2"))

        return self.program
