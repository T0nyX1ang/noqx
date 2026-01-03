"""The Uso-tatami solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_reachable_src
from noqx.rule.shape import all_rect_region, avoid_edge_crossover


def rect_constraint() -> str:
    """Generate a cell relevant constraint for rectangles with the width/height of 1."""
    return ":- topleft(R, C), left(R + 1, C), top(R, C + 1)."


class UsotatamiSolver(Solver):
    """The Uso-tatami solver."""

    name = "Uso-tatami"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VVdb9owFH3Pr6j8fB9i59svE+tgL4xuK1NVRREKNFujgdIRMlVG/Pce36QN0mDVhsReJstHx+fa5vjG19Q/mnxdUIzmxeSSRPN8xV25CXe3a9Nysyz0BQ2azX21BiG6Go3oa76sCyftZmXO1iTaDMi816lQgrhLkZH5pLfmgzYTMtcICZLQxmBSkAId9vSG45ZdtqJ0wScdB70FXZTrxbKYjVvlo07NlIT9nbe82lKxqn4Wol3G40W1mpdWmOcbHKa+Lx+6SN3cVd+bbq7MdmQGrd3hAbteb9fS1q5lB+zaU5xst7j7VtTN/JDXJNvtkPPPcDvTqTX+padxT6/1FjjRW6FCu/QNjLQfRqjICtGeEFsh3BMSKwS94LlW8PcEaQVvT1BWwMd/Ebzn7LIAM5It3TKOGBXjFI7JeIzvGF3GgHHMc4aMN4yXjD5jyHMie+Y/ysrpdpACX+gkxumCmGSEDHmvWkxVyDXXt+C848xJxRC362JSrVf5Ejds0qzmxfp5jHreOeJRcE89LPH/l/i/KHGbf/fMV/rUCkuR2pdqIHNF4qGZ5bNFhXuG/LXhCP86MW7QkXCsSCZ4aI6EgwSbI0dHwiE2j45vHqICIjxafxn+/eavWDvl3Hhqfgmc/dvj9RJNXW3yTb4qReY8AQ=="
        },
        {"url": "https://puzz.link/p?usotatami/8/8/7b23b6b4b2f2d4a21a2b4b3a3e8e5b3b2b32b3", "test": False},
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
        self.add_program_line(f":- {{ topleft(R, C) }} != {len(puzzle.text)}.")

        all_src = []
        tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(("ne", num), (r, c), main_type="bulb", color=None, adj_type="edge"))

            all_src.append((r, c))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
