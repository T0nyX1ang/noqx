"""The Aquapelago solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import count_reachable_src, grid_color_connected, grid_src_color_connected
from noqx.rule.shape import avoid_rect


class AquapelagoSolver(Solver):
    """The Aquapelago solver."""

    name = "Aquapelago"
    category = "shade"
    aliases = ["aquapelago"]
    examples = [
        {
            "data": "m=edit&p=7VZBb9pMEL3zK6I5z8Frr43xpaJp+C6U9CtUUbSykHEdBcXU1OCqWsR/z8ysFWOVqpEqcagis2+GN7PLm9nVmt33JqsLVBF/ghg9VPREOpIRxiMZXvss1vuySK5w3Owfq5ocxNvJBB+yclcMTJuVDg52lNgx2v8SAwoQfBoKUrT/Jwf7MbEztHMKAWripi7JJ/emc+8kzt61I5VH/sz5PO2e3Hxd52WxnFKUmE+JsQsE/p33Mptd2FQ/Cmh18Pe82qzWTKyyPRWze1xv28iu+Vo9NW2uSo9ox07u/IzcoJPLrpPL3hm5XMXfyy231Tmho/R4pIZ/JqnLxLDqL50bd+48OYD2IdEIeigmDMXE2plIzEiJUcrlqKFLUqNArO+5NN93s/zYLRl4sbPK5QXaxYOwjYe8HsmYtTJIO2+kOxeiyO1sS7C2HsEqDbw7IUiIAd0RrNzAsCOkht4iUo3h4/jCcF2Uc0JJiX15Um1vntRtIOgY6UCf4V70fl+60ltH+mMgPGVE9cs61DOVHAjvBSeCvuCCdhZtIPhB0BMMBaeScyN4J3gtqAUjyRny2Xj16aFyfISId9jt5AW0Ge3LjfT7J3yL/8vxdGBg3tQPWV7Q9TdrNquivppV9SYrgd40xwH8BBkmoHT99vK5+MuHm++98hK52L3xBzmG+hoFaG8Rts0yW+ZVCfTPBZnXv/IXV08XH3xr6vVTtiogHTwD",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(avoid_rect(2, 2, color="not black"))
        self.add_program_line(grid_color_connected(color="not black", adj_type=4, grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color="black", adj_type="x"))
                self.add_program_line(count_reachable_src(num, (r, c), color="black", adj_type="x"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
