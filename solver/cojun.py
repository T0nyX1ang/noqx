"""The Cojun solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent


class CojunSolver(Solver):
    """The Cojun solver."""

    name = "Cojun"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7ZVdb9MwFIbv+ysmX/si/khs566MjptRPrYJTVE1dV1gFa0K/UAoVf8773GO64EmIYSAXaAo1nucY+f1c2Jn83k3XbfS4zJeFlLhMlbHWxch3gVfl/Ptoq1P5HC3vV+tIaR8dXYm308Xm3bQcNZksO9C3Q1l96JuhBJSaNxKTGT3pt53L+tuJLsLPBJSoe+8T9KQoyzfxeekTvtOVUCPWUNeQ87m69mivTnve17XTXcpBb3nWRxNUixXX1rBPiierZa3c+q4nW6xmM39/BM/2ezuVh93Ir3iILthb3f8iF2T7ZqjXfO4Xf3n7YbJ4QDsb2H4pm7I+1WWPsuLen8gX3uhKww1qHWsjDAKoTqG1iDUOSy/e6oKjdjmWBU/xDRb+SC2D8bDgIo2rmN7Flsd20u4lJ2J7fPYFrEtY3sec0Ywryp8pw4mNGas8GJX9dqh33O/wwu9YY21eMsaq/Yla4z1PNYjJ3COR39I/VhIcKwddGDtsTeKXgcLzfmhhOb8UEF71shXKR/7iiBBYxy0Z+2gA2vkaM5RBbRmjX2pLWvMafo5kQttWBvokjW8md6bNsixnGMwj+V5DDxY9mDhv3SsMX/FnqsAzkVmm/gTT2czT5fYlrkuxDbVgtgm/r6CdkeeyocjwyP/QMx95sbMwZXOpswn8VRYo3rASpnMKrFVxDZxKzJnYpg4E8PE2SDHqMzQ6MwwMTfEPOXbzJ/YmsST+PNYOl9TLSzybZn5W66XpbqksY5rdKDzhrbCaWxtbKu4RRxt8186CH5/N/7UTqOr+FfJV/l348mgEaO7D+3JeLVeThc4QMe75W27TjH+WIeB+CriHQ9F+/8n9o9+YlSC4ql9wU/NDvbUZPAN"
        },
        {
            "url": "https://puzz.link/p?cojun/21/12/a5jqlrdnesrffdain5ldmiattp7mfoldndfu6mtmcqbll97afve4shdk14tnr3hbsrvv1bfsrajvmi5ucfra97rrstbnsb03j3zzl2i5zzs4zs5q4zzzj2l4zi",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(unique_num(_type="area", color="grid"))
        self.add_program_line(avoid_same_number_adjacent(adj_type=4))
        self.add_program_line(":- area(A, R, C), area(A, R + 1, C), number(R, C, N1), number(R + 1, C, N2), N1 < N2.")

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
