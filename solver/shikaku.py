"""The Shikaku solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region, count_rect_size


class ShikakuSolver(Solver):
    """The Shikaku solver."""

    name = "Shikaku"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VRNb9pAEL3zK9Ce5+D9wKx9Iyn0QknbUEWRZSFD3AYF5BRwVS3iv+ftGDBuiaoqaqpK1bKPNzP7MfvWs+uvZbbKSQb+py3hH81Iy13ZkHuwb+P5ZpHHbeqVm/tiBUJ0NRjQ52yxzlvJflTa2roodj1yb+NEKEHcpUjJfYi37l3sRuSuERIk4RuCSUEKtF/TG457dlk5ZQA+qngX9BZ0Nl/NFvlkWC30Pk7cmITf54JneyqWxbdcVNPYnhXL6dw7ptkGh1nfzx/3kXV5VzyU+7Ey3ZHrVen2z6Sr63Q9rdL17E+lm999ydfl9FyuUbrbQfOPyHYSJz7xTzW1Nb2Ot8BRvBW6g6kRdatrEcbCtEczVDDDo9ntNkwbwtS1GTXMSPuk2jj0wWF+cMhANtaTgd/OnNh+g+YMv0fDI33GJ2tov+3JGqaZswyDExsiSJbilnHAqBjHUIqcZnzDGDB2GIc8ps94w3jJaBhDHtP1Wv/Wbbw8HREaKBRZXF0HB/VEGU3KQHtNQitLWmEEuLLwR1BH//IMia4eg2br/Hu+tJWIPsqnPSpWy2yBEhqVy2m+Oth4sHYt8V1wx7eM9+//G/Y33jCvf/DKtfPSUk4g7bHayF2ReCwn2WRW4DuDfhw+FOAz4UNNng+jpJ8JmOinwKuLg2dC4Pt7yHCTaesJ",
        },
        {
            "url": "https://puzz.link/p?shikaku/24/14/h5x6i.j8g6lag4j.l9i8j6i4l3z9g6i4i4h56h6i4i6j8h4n3h6zn4j4r6j4g6j8i8hci6j8q6h2r8k5l8k8j.l9j4l.lataock36kck",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(f":- {{ top_left(R, C) }} != {len(puzzle.text)}.")

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
                self.add_program_line(count_rect_size(num, (r, c), adj_type="edge"))

            all_src.append((r, c))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
