"""The Patchwork solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_src_color_connected
from noqx.rule.shape import all_rect_region
from noqx.solution import solver


def count_patchwork_src(target: int, src_cell: Tuple[int, int], color: str = "black") -> str:
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    src_r, src_c = src_cell
    return f":- #count{{ R, C: {tag}({src_r}, {src_c}, R, C), {color}(R, C) }} != {target}."


def avoid_same_color_adj_edge():
    rule = ":- grid(R, C), edge_top(R, C), black(R, C), black(R - 1, C).\n"
    rule += ":- grid(R, C), edge_top(R, C), white(R, C), white(R - 1, C).\n"
    rule += ":- grid(R, C), edge_left(R, C), black(R, C), black(R, C - 1).\n"
    rule += ":- grid(R, C), edge_left(R, C), white(R, C), white(R, C - 1).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_rect_region(square=True))
    solver.add_program_line(avoid_same_color_adj_edge())

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
        solver.add_program_line(count_patchwork_src(target=num, src_cell=(r, c), color="black"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="edge_left"))
    solver.add_program_line(display(item="edge_top"))
    solver.add_program_line("upleft1(R, C, 1) :- upleft(R, C).")
    solver.add_program_line(display(item="upleft1", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Patchwork",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VRda9swFH33rxh61oNvZDuO3rqs2UuWrUtGKcIUN3WomYO7OBlDIf+990Ob49GHwaB0MBzde3Jyr3SOrKj7dih3lYaYPibXmPFJIOcxyjMecXhW9b6p7Bt9cdg/tDsEWn+czfSmbLoqcqGqiI5+Yv2V9u+tU6C0GuEAVWh/ZY/+g/UL7Zf4k9I5cnMpGiG87OE1/05oKiTEiBcBI7xBuK5366a6nQvzyTq/0orWecvdBNW2/V6poIO+r9vtXU1E2WyawHWH+/brIVRBcdL+QoQufwql+YNQ0wslKEIJPSOU9P+10Ltyj7vePdSPz8mdFKcTbvhnFHxrHWn/0sO8h0t7VCZWNtfKGEkTTkkiacwpzTllUjIWciyVOUjKOE2kZJJygljmhngUsvQAyPQA0gUgC4AJdUaWgCTwqSwCaajPQl1G66CPBfnAuWWv5VyxB0fH7BeBsw4qyNeAIIeDFjLplOkJ8jloYU+DHnblVHrGkK/fGNZy3kVehwy5Hq5F/s/koHOwR4w3HGccRxxX+IK1NxzfcYw5phznXHPJ8ZrjlGPCMeOaMR2RPzxE8gpeQI4zchcNn/Tf44rIqeVhtynXFf6Bp+32se3qfaXwnjxF6ofi4Qxdu/+vzhe/Omnz49d29l+bHPw3FtET",
        },
    ],
}
