"""The Yajitatami solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_reachable_src
from noqx.rule.shape import all_rect_region, avoid_edge_crossover


def yaji_region_count(target: int, src_cell: Tuple[int, int], arrow_direction: str) -> str:
    """Generates a constraint for counting the number of {color} cells in a row / col."""
    src_r, src_c = src_cell
    rule = ""

    if arrow_direction == Direction.LEFT:
        rule += f':- not edge({src_r}, {src_c}, "{Direction.LEFT}").\n'
        rule += f':- #count {{ C1 : edge({src_r}, C1, "{Direction.LEFT}"), C1 <= {src_c} }} != {target}.'

    if arrow_direction == Direction.RIGHT:
        rule += f':- not edge({src_r}, {src_c + 1}, "{Direction.LEFT}").\n'
        rule += f':- #count {{ C1 : edge({src_r}, C1, "{Direction.LEFT}"), C1 > {src_c} }} != {target}.'

    if arrow_direction == Direction.TOP:
        rule += f':- not edge({src_r}, {src_c}, "{Direction.TOP}").\n'
        rule += f':- #count {{ R1 : edge(R1, {src_c}, "{Direction.TOP}"), R1 <= {src_r} }} != {target}.'

    if arrow_direction == Direction.BOTTOM:
        rule += f':- not edge({src_r + 1}, {src_c}, "{Direction.TOP}").\n'
        rule += f':- #count {{ R1 : edge(R1, {src_c}, "{Direction.TOP}"), R1 > {src_r} }} != {target}.'
    return rule


def rect_constraint() -> str:
    """Generate a cell relevant constraint for rectangles with the width/height of 1."""

    rule = f':- rect(R, C, "{Direction.TOP_LEFT}"), rect(R + 1, C, "{Direction.LEFT}"), rect(R, C + 1, "{Direction.TOP}").\n'
    rule += f':- grid(R, C), rect(R, C, "{Direction.TOP_LEFT}"), #count {{ R1, C1: adj_edge(R, C, R1, C1) }} = 0.'
    return rule


class YajitatamiSolver(Solver):
    """The Yajitatami solver."""

    name = "Yajitatami"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VTLbtswELzrKwKe98CXJEo3N7VzcZy2cVAEgiDIjtoYsaFEtoqChv69y6UaBVWAomjrXgqCy+FwuZzla//Ulk0FBosywEFgUVpSlTyhyvuy3By2VXoGk/ZwXzcIAK5mM/hUbvdVkPVeeXC0SWonYC/SjEkGVAXLwb5Pj/YytQuw1zjEQCA3RyQYSITTAX6kcYfOPSk44oUP6KbdIlxvmvW2KuaeeZdmdgnMrfOGZjvIdvWXivkQ1F/Xu9XGEavygMns7zeP/ci+vasf2t5X5B3YiZc7fUWuGuSqZ7nqdbny78tN8q7Dbf+Agos0c9pvBmgGeJ0eO6fryGTspqrCbac7IYwYck+pgYrCkVccjbzieEwZT/GBMuMVk2RECS49J15wIvyBwyQEpXJLdkZWkl1ipmAV2bdkOdmQ7Jx8prgBIlYgDAaWuIAJEUc9jhDHHsfhC6wB+z3GubHu/Q36JM9Yck4YW5BCeizwLQnlsdQgZThg5dfFFqQ2HmuMo13Mzt0tJ/mcrCYbUSqxO9JfOvQ/sGtKYNaJ+amsTEb0kwwlPG0/DzI2vftcnS3qZldu8dEs2t2qar738ZfqAvaVUc3wOEH//7j+0cfljoCf+Cb/7sPKcHfxMYC9AvbYFmWxrvGS8fzkMvGt5cE3",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(rect_constraint())
        self.add_program_line(avoid_edge_crossover())

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))
            fail_false(isinstance(clue, int) and label.startswith("arrow"), "Please set all NUMBER to arrow sub.")
            arrow_direction = label.split("_")[1]
            self.add_program_line(count_reachable_src(int(clue), (r, c), main_type="bulb", color=None, adj_type="edge"))
            self.add_program_line(yaji_region_count(int(clue) + 1, (r, c), arrow_direction))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
