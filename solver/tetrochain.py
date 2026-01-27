"""The Tetro Chain-Y solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, general_shape
from noqx.rule.variety import yaji_count


def avoid_adjacent_same_omino(num: int = 4, color: str = "black") -> str:
    """Generates a constraint to avoid adjacent ominos with the same type."""
    tag = tag_encode("belong_to_shape", "omino", num, color)
    rule = f":- not {color}(R, C + 1), not {color}(R + 1, C), {tag}(R, C, T, _), {tag}(R + 1, C + 1, T, _).\n"
    rule += f":- not {color}(R, C), not {color}(R + 1, C + 1), {tag}(R + 1, C, T, _), {tag}(R, C + 1, T, _)."
    return rule


class TetroChainYSolver(Solver):
    """The Tetro Chain-Y solver."""

    name = "Tetro Chain-Y"
    category = "shade"
    aliases = ["tetrochainy"]
    examples = [
        {
            "data": "m=edit&p=7VVRb9MwEH7Pr6juCaRDimOna/NWxspLyYAWTVMURWnItLCUjKRB4Kr/fXeXSA20D+yBTUjI9ZevX87nz+fabb61aZ2jcvmjJ0hPakZNpHuTsXS3b6tiW+bBCGft9raqiSBezud4k5ZN7kR9VOzs7DSwM7Rvgwg8QOkKYrQfgp19F9gQ7ZJeARrSFsQUoEf04kCv5D2z805ULvGwS6iIXhPNijor82TRKe+DyK4QeJ7XMpopbKrvOXQp5HtWbdYFC+t0S4tpbov7/k3Tfq7u2j5WxXu0s87u8oRdfbDLtLPL7IRdXsVftjuN93sq+0cynAQRe/90oJMDXQY7wjDYgRnzUC9hr7xDlNFXki3hCvfS2O2ihpJ/NPDMHEvTo1xTSW8SPZAklz8cqFyZ0gxHKlcmMIk70PSJOP17PlqskiVfC84FPcEVVQStFnwj6Ar6gguJuRC8EjwXNIJjiTnjmv5h1YHtegiaimC6LXgCb5HuzvOvzf/3tNiJYNnWN2mW088/bDfrvB6FVb1JS6D7Zu/AD5Aeab6+/l9Bz3QF8Ra4j7qInv+ERlRdOif2EuG+TdIkq0qgfzFk3fiP07U60p98tXTs4Wf6pbhLbTt6waxJv77ib/R8CbHzAA==",
        },
        {"url": "https://puzz.link/p?tetrochain/9/9/c33d37k32d35k31d32k22d41t34", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="black", adj_type=8, grid_size=(puzzle.row, puzzle.col)))

        self.add_program_line(all_shapes("omino_4", color="black"))
        self.add_program_line(avoid_adjacent_same_omino(4, color="black"))
        for i, o_shape in enumerate(OMINOES[4].values()):
            self.add_program_line(general_shape("omino_4", i, o_shape, color="black", _type="grid", adj_type=4))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            self.add_program_line(f"not black({r}, {c}).")
            fail_false(isinstance(clue, int) and label.startswith("arrow"), "Please set all NUMBER to arrow sub.")
            arrow_direction = label.split("_")[1]
            self.add_program_line(yaji_count(int(clue), (r, c), arrow_direction, color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
