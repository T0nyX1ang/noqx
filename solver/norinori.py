"""The Norinori solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.variety import nori_adjacent


class NorinoriSolver(Solver):
    """The Norinori solver."""

    name = "Norinori"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZXNbtpAFIX3PEU061l4fmzPeEdT6IYmbaGqIgshhzgNqpEp4Koy8rv3zPi6s0FJpEasKstXn6/PwPHhejj8bIp9yQ0OZXjEBQ6lpT9lZP0Z0bHYHKsyu+Lj5vhU7wGc306n/LGoDuUoJ9VydGpt1o55+yHLmWCcSZyCLXn7OTu1H7N2wts5bjFu0Jv1IgmcBPzm7zu67psiAt8QA++A681+XZWrWd/5lOXtgjP3Pe/8aodsW/8qGflw1+t6e79xjfviiIc5PG12dOfQPNQ/GjZ8RcfbcW93fsauCnbVX7vqvF35JnarXX3OqF12HQL/AqurLHeuvwY0AefZqXOOXBW+3vk69VX6uoCUt8rX975Gvsa+zrxmkp2YSCQXqWaZxO+aai5MQpyATc9GcWFjYmgsaUwKtsQG4xX1bBMwrbXoi76P+2BJDI0wxNBI0ghoJGmEACtijLDsfUqJvqK+RF8NfQWOiTW49ykVNJo0ChpNGhWDU2L40eRHY21MazU0MWl0CrbE8JxEIas0DVkZHbIyQ25xyNa4bNOQ4ZCzdTnTWqtD5shTWNJbl3nIdshfRvAZJSG3IWfh8ieNsCFn6XIWIcMhZwmNIo2CRpFGucxlyHDIXKOvqe+2GU2foxVl3rlXyo3bta/a18SPYerm+ZUTz2T/cDG8mbca/xe95TLxu2g44steL0c5mzf7x2JdYsuYPHwvr27q/baoGPbmbsR+M3/mmByu/2/XF9+uXfjRhTftf32jcuSKuW5vOds1q2K1riuG/3r+XD+OXq2/+NPiNV2O/gA=",
        },
        {
            "url": "http://pzv.jp/p.html?norinori/20/10/ahkcfeorctdhkqdffmk9jprqnqd57ea6us16ok4jboec2oku7ck43rbqseje3kc16cvv8f7i7f",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))

        self.add_program_line(adjacent())
        self.add_program_line(nori_adjacent(color="gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(2, color="gray", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
