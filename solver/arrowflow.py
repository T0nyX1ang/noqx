"""The Arrow Flow solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, shade_cc
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected


def arrow_flow_adjacent() -> str:
    """Generate a rule to define the adjacency for arrow flow."""

    # the definition is designed to be compatible with the reachable propagation
    rule = "adj_line_directed(R, C, R, C + 1) :- grid_all(R, C), grid_all(R, C + 1), arrow_N_W__5(R, C).\n"
    rule += "adj_line_directed(R, C, R, C - 1) :- grid_all(R, C), grid_all(R, C - 1), arrow_N_W__1(R, C).\n"
    rule += "adj_line_directed(R, C, R + 1, C) :- grid_all(R, C), grid_all(R + 1, C), arrow_N_W__7(R, C).\n"
    rule += "adj_line_directed(R, C, R - 1, C) :- grid_all(R, C), grid_all(R - 1, C), arrow_N_W__3(R, C)."
    return rule


class ArrowFlowSolver(Solver):
    """The Arrow Flow solver."""

    name = "ArrowFlow"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7Vbvb7JIEP7uX9Hs125yLChFkvugVt9732uprRpPiTFoUWnB9RBsD+P/3plFC4u0uTS5X8kFd5h5Zpid2V0e3P4eO6FLmYI/zaBwh6vKDDFUQxdDOV59L/Jd84I24mjFQ1Aovet06MLxty79MVrdtHjj5brx286IxmP2TYm/K8OnztPlQ/Drd08LWccyurfdW09dNn5pNe/19qXejbeDyN3dB6z5NBj3F93hsq7+0bbG1WR8p9R+jBc/7RqDnyv2sYZJZZ/UzaRBk2+mTRihRIXByIQm9+Y+uTUTiyY9cBFanVASxH7kzbnPQyIwBnE36YMqqO1MHQo/aq0UZAro1lEHdQSqE4b8ZWpNmynUNe2kTwlO3hSPo0oCvnNxNiwO7TkPZh4CMyeC9duuvA2hGji28SN/jo+hbHKgSSNtYXRqASb5rAVIcmoB1bQF1EpawM7yLQy/1oK/4SXF1yeHA2zMA5Q/NW3sZJCpRqb2zD0xGDGrlNS19FYVN1bT4Q4RFkRoEGFX4RyKfSUahNhaZl6BabybuiIF65A2F6xjMJ7uo23ANDm3UQfz6t2sq5KXKZhMzdn4NL4gJxsfZzlANQCoZbaGCXMJtJqcoIbxembrcudMx9ZP8bA6zNyDHOEqYtuASycSfB0RoQrZh0WniSbktZCKkDUhb0RMW8ihkC0hq0LqIuYKt+1Pbmy6eVKRGhZZy4oUZ+4vKtLWUu6SL9yL/xg2qdikF4cLZ+7C22fFwcwNLyweBo4Pdm/lbFwCLEi23J9u07ip++rMI2KmRJz3SNha5JIgn/ON763LMpxcEugt1zx0S10Iuo/Lj1KhqyTVjIePhZpeHN+XexEfKQmae+Hcl6EoBIbK2eLQSUjgRCsJyBGylMldFxYzcuQSnWenMFuQLcehQl6JGMAl8PL//8n6136ycJOUL/PbP0O3Nqw1cF1yR8kmnjpTWGcC/4v+9irFsefhJxyUOYtwCRMB+gkZ5bxl+Ae8k/MW8TOSwWLPeQbQEqoBtMg2AJ0TDoBnnAPYB7SDWYvMg1UVyQenOuMfnCpPQTZZx6E34zGZVN4A",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_cc(colors=["arrow_N_W__1", "arrow_N_W__3", "arrow_N_W__5", "arrow_N_W__7"]))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(arrow_flow_adjacent())
        self.add_program_line(avoid_unknown_src(adj_type="line_directed", color="grid"))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__1", adj_type=4))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__3", adj_type=4))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__5", adj_type=4))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__7", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(grid_src_color_connected((r, c), adj_type="line_directed", color="grid"))
            if isinstance(num, int):
                self.add_program_line(f"hole({r}, {c}).")
                self.add_program_line(count_reachable_src(num + 1, (r, c), adj_type="line_directed", color="grid"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name.startswith("arrow_N") and symbol_name.split("__")[1] in ["1", "3", "5", "7"]:
                self.add_program_line(f"{symbol_name.replace('B', 'W')}({r}, {c}).")

        self.add_program_line(display(item="arrow_N_W__1", size=2))
        self.add_program_line(display(item="arrow_N_W__3", size=2))
        self.add_program_line(display(item="arrow_N_W__5", size=2))
        self.add_program_line(display(item="arrow_N_W__7", size=2))

        return self.program
