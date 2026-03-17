"""The Meandering Numbers solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent


def meander_constraint(_id: int, area_size: int) -> str:
    """Generate a constraint for the meandering numbers."""
    if area_size == 1:
        return f":- area({_id}, R, C), not number(R, C, 1)."

    mutual = f"area({_id}, R, C), area({_id}, R1, C1), number(R1, C1, N1), adj_4(R, C, R1, C1)"
    rule = f"meander({_id}, R, C) :- number(R, C, N), #count {{ R1, C1 : {mutual}, |N - N1| = 1 }} != 2."
    rule += f":- area({_id}, R, C), number(R, C, 1), #count {{ R1, C1 : {mutual}, N1 = 2 }} != 1."
    rule += f":- area({_id}, R, C), number(R, C, {area_size}), #count {{ R1, C1 : {mutual}, N1 = {area_size - 1} }} != 1."
    rule += f":- area({_id}, R, C), meander({_id}, R, C), not number(R, C, 1), not number(R, C, {area_size})."
    return rule


class MeanderSolver(Solver):
    """The Meandering Numbers solver."""

    name = "Meandering Numbers"
    category = "num"
    aliases = ["meanderingnumbers"]
    examples = [
        {
            "data": "m=edit&p=7VbLbhMxFN3nK6pZe+H3Y3ahpGxKeLQIVVFUpW2gEYkCSYPQRPl3zvVcxywqIYQQFULJOCce+5zre489s/2ym23mQin6miikABLW+XwppfMl+XO5eFjO2xMx3D3crzcAQrw6OxMfZsvtfDDhUdPBvkttNxTdi3bSqEY0GpdqpqJ70+67l203Et0FbjVCoe+8H6QBRxW+z/cJnfadSgKPGQNeAd4uNrfL+fV53/O6nXSXoiGdZ3k2wWa1/jpvOA76f7te3Syo42b2gMVs7xef+c52d7f+tGuKxEF0wz7c8SPhmhquOYZrHg9X//lw0/RwQNrfIuDrdkKxv6swVnjR7g8U175R1mGuQbGpNOhU+dZVbs9yq3N7iZmiM7l9nluZW5fb8zxmBEJtjdAuNq1Gwa0T2kvGAVgzTsC2xy4KHUyPvQR2jDVwYGyBE2NwRuYM0IqsFdCfSj+0EmsFaCXWilEYyVpJArNW0sCslSxwr4WxwqjI2AmjJeMArBkn4J4fY4UxPT/GAjvG4DeBMfgN8xvwW+Y34HfMb8DvmN+A3zG/Bb9nfgd+z/wO/J75Hfg982PvmqB6jHwazifmYZOzlgdnZE4PrchaAfyR+QMdCp4xYuPcggOYx0SsJfFaImJIHAPyaUs+E84TxfGkCNzrWimBS91Ra16Xhq4OpY66+oTqHrimwVbPkAeCZ+yrf8gPofgkVi+RN0oeJNYoS0310SfZA5JzIu3RM9kPknMi/dE/2RuyeCb+4CXkVrGWQt5KHujAVaXWwKZgXb1EPjEcg7HVV+QZwzEYXz1G/jHFV7H6jbzhimfIbzzXQ5f3ZvZJ8ZiHLu9T/Fa/kX98meur9zx0fay+Kj4kXwVee3TVS0lVL9EeTKybyEusmzA+lfEJXiKeA521dOSc5tbm1uejKNAR90uH4O+fej8NZ4Jqqkc+7t/tnQ4mzeju4/xkvN6sZks8rsa71c18U/7j/eAwaL41+cpPIPv/leEvvTJQCeRT2zNPLRzs4ungOw==",
        },
        {
            "url": "https://puzz.link/p?meander/15/15/4i894gi914i2944i894gi914i2944i894gi914i294000000vvv000000vvv000000vvv000000vvv000000i7j1j2g8j2j3l1j6j9l6j5j9g5j6j8l3j1j4g9j9j4l2j3j4l2j7j9g8j7j3l8j4j9g5j3j6l1j6j7l1j2j4g6j9j9i",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")
        n = puzzle.row
        self.add_program_line(grid(n, n))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(avoid_same_number_adjacent(adj_type=8))
        self.add_program_line(unique_num(_type="area", color="grid"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, (ar, _) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i))
            self.add_program_line(meander_constraint(_id=i, area_size=len(ar)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
