"""The Shikaku solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region
from noqx.solution import solver


def shikaku_cell_constraint(target: int, src_cell: Tuple[int, int]) -> str:
    """
    Generate a cell-relevant constraint for shikaku.

    A bulb_src_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {count_r}, {count_c}, CR * CC != {target}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)

    assert len(puzzle.text), "No clues found."
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_rect_region())
    solver.add_program_line(f":- {{ upleft(R, C) }} != {len(puzzle.text)}.")

    for (r, c), clue in puzzle.text.items():
        solver.add_program_line(f"clue({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

        if isinstance(clue, int):
            solver.add_program_line(shikaku_cell_constraint(clue, (r, c)))

    for r, c, d in puzzle.edge:
        solver.add_program_line(f":- not edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
    solver.add_program_line(f":- clue(R, C), clue(R, C), (R, C) != (R1, C1), {tag}(R, C, R, C1), {tag}(R1, C1, R, C1).")
    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Shikaku",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VRNb9pAEL3zK9Ce5+D9wKx9Iyn0QknbUEWRZSFD3AYF5BRwVS3iv+ftGDBuiaoqaqpK1bKPNzP7MfvWs+uvZbbKSQb+py3hH81Iy13ZkHuwb+P5ZpHHbeqVm/tiBUJ0NRjQ52yxzlvJflTa2roodj1yb+NEKEHcpUjJfYi37l3sRuSuERIk4RuCSUEKtF/TG457dlk5ZQA+qngX9BZ0Nl/NFvlkWC30Pk7cmITf54JneyqWxbdcVNPYnhXL6dw7ptkGh1nfzx/3kXV5VzyU+7Ey3ZHrVen2z6Sr63Q9rdL17E+lm999ydfl9FyuUbrbQfOPyHYSJz7xTzW1Nb2Ot8BRvBW6g6kRdatrEcbCtEczVDDDo9ntNkwbwtS1GTXMSPuk2jj0wWF+cMhANtaTgd/OnNh+g+YMv0fDI33GJ2tov+3JGqaZswyDExsiSJbilnHAqBjHUIqcZnzDGDB2GIc8ps94w3jJaBhDHtP1Wv/Wbbw8HREaKBRZXF0HB/VEGU3KQHtNQitLWmEEuLLwR1BH//IMia4eg2br/Hu+tJWIPsqnPSpWy2yBEhqVy2m+Oth4sHYt8V1wx7eM9+//G/Y33jCvf/DKtfPSUk4g7bHayF2ReCwn2WRW4DuDfhw+FOAz4UNNng+jpJ8JmOinwKuLg2dC4Pt7yHCTaesJ",
        },
        {
            "url": "https://puzz.link/p?shikaku/24/14/h5x6i.j8g6lag4j.l9i8j6i4l3z9g6i4i4h56h6i4i6j8h4n3h6zn4j4r6j4g6j8i8hci6j8q6h2r8k5l8k8j.l9j4l.lataock36kck",
            "test": False,
        },
    ],
}
