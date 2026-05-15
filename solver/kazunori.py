"""The Kazunori Room solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import area, display, fill_num, grid
from noqx.rule.helper import fail_false, full_bfs, validate_type
from noqx.rule.neighbor import adjacent


def number_appear_twice() -> str:
    """Generate a constraint for a number appearing twice in an area."""
    return ":- area(A, _, _), number(_, _, N), #count { R, C : area(A, R, C), number(R, C, N) } > 2."


def avoid_2x2_number() -> str:
    """Generate a constraint for avoiding 2x2 number cells."""
    return ":- number(R, C, N), number(R + 1, C, N), number(R, C + 1, N), number(R + 1, C + 1, N)."


def area_num_adjacent(adj_type: int = 4) -> str:
    """Generate a constraint to ensure adjacent cells with the same number in an area."""
    return f":- area(A, R, C), number(R, C, N), #count {{ R1, C1: area(A, R1, C1), number(R1, C1, N), adj_{adj_type}(R, C, R1, C1) }} != 1."


class KazunoriSolver(Solver):
    """The Kazunori Room solver."""

    name = "Kazunori"
    category = "num"
    aliases = ["kazunoriroom"]
    examples = [
        {
            "data": "m=edit&p=7ZVNT9tAEIbv+RVoz3PYL++ufaOU9kLTD0AVsqwoBLdETRSakKpylP/ed9cTDE4rhCropbI8fjyeHb8z3l2vvq/Hy5oCeTKBJCkcxmoy0pJ1Kp2Sj7Pp7awuDuhwfXu9WAKI3g/py3i2qgclB1WDTZMXzSE1b4tSKEFC41SiouZjsWneFc2QmlM8EqTgO2mDNPC4w8/peaSj1qkkeAh2ghzwAjiZLiezenTSJvpQlM0ZifieV2l0RDFf/KgF64j3k8X8chodl+Nb1LK6nt7wk9X6avFtzbGq2lJz+Ge5ppNr7uSa38jlep5Zbl5tt2j7JwgeFWXUft5h6PC02Gyjro0wUsexFt0k9BQJjcr2PGHPk/c92vU9xvQ9VvU92b6n/3abyb7H9TVb389j/UM9KFeloi+SfZOsTvYMPaHGJPs6WZlsluxJijlGq5TLSXmI0ZjGWXjIWc6MGMd+Gzr2WFBBtxw0qdy2nFvS0iXGlXRsdWQVwDlzTtqobmwwzAZ5Ms6TgR2zA3tmj/ycR4aHrFttuIIVs8K7DMfgvYpjVIzRHKPBHKMN2DKjFr3TE+7GRlY59ydHTsk5JXLKXV1Rc+BeWdTItTjU623Hjmt3qN2xP9Mdx7GeNXj0xHMej/yeexJs1ysf+2k79rv86h7j2znV+eP009u42uPUOErWJuvSlPFxkT1tGbarJ24SaYv8+9n6qLxSu7TFd0f2vPfVoBTHV1/rg+FiOR/PsH0N1/PLerm7x/9iOxA/RTpLfF6y/38h/+gXEj+BfNIMfoEZ+4icEt3FnL63ikjcrEfj0WSBySarF5eLNVYNfgE=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(number_appear_twice())
        self.add_program_line(avoid_2x2_number())
        self.add_program_line(area_num_adjacent(adj_type=4))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            fail_false(len(ar) % 2 == 0, f"Area {i} must have an even number of cells.")
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(1, len(ar) // 2 + 1), _type="area", _id=i))

        for (r, c, d, label), num in puzzle.text.items():
            validate_type(label, "normal")

            if d == Direction.CENTER:
                fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
                self.add_program_line(f"number({r}, {c}, {num}).")

            if d == Direction.TOP and r > 0 and isinstance(num, int):
                self.add_program_line(f":- number({r}, {c}, N), number({r - 1}, {c}, N1), N + N1 != {num}.")

            if d == Direction.LEFT and c > 0 and isinstance(num, int):
                self.add_program_line(f":- number({r}, {c}, N), number({r}, {c - 1}, N1), N + N1 != {num}.")

        self.add_program_line(display(item="number", size=3))

        return self.program
