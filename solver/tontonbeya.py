"""The Tontonbeya solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import area_color_connected


def tonton_cluster_rule() -> str:
    """Generate a rule to make clusters have the same number of shapes."""
    cnt_circle = "#count { (R, C): area(A, R, C), ox_E__1(R, C) }\n"
    cnt_triangle = "#count { (R, C): area(A, R, C), ox_E__2(R, C) }\n"
    cnt_square = "#count { (R, C): area(A, R, C), ox_E__3(R, C) }\n"

    rule = "have_circle(A) :- area(A, R, C), ox_E__1(R, C).\n"
    rule += "have_triangle(A) :- area(A, R, C), ox_E__2(R, C).\n"
    rule += "have_square(A) :- area(A, R, C), ox_E__3(R, C).\n"
    rule += f":- have_circle(A), have_triangle(A), N1 = {cnt_circle}, N2 = {cnt_triangle}, N1 != N2.\n"
    rule += f":- have_circle(A), have_square(A), N1 = {cnt_circle}, N2 = {cnt_square}, N1 != N2.\n"
    rule += f":- have_triangle(A), have_square(A), N1 = {cnt_triangle}, N2 = {cnt_square}, N1 != N2.\n"
    return rule


def tonton_adjacent_rule(adj_type: int = 4, color: str = "black") -> str:
    """Generate a rule for getting the adjacent tontonbeya areas."""
    shape_dict = {"ox_E__1": "circle", "ox_E__2": "triangle", "ox_E__3": "square"}
    tag = tag_encode("area_adj", adj_type, color)
    rule = f"{tag}(A1, A) :- {tag}(A, A1), A < A1.\n"
    rule += f":- have_{shape_dict[color]}(A), #count {{ A1: {tag}(A, A1) }} != 1.\n"
    return rule


class TontonbeyaSolver(Solver):
    """The Tontonbeya solver."""

    name = "Tontonbeya"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VRNb9swDL3nVxQ682BKtmX7lnbOLl27LR2GwgiCtPWWYAmc5WMoHOS/70lmo3UNUKBAhx4Gw/QzJZKPFKn1z+1kVRNHlJHJKCLGEzN+Yk06jv0byXM128zr4oT62820WQEQXQ4G9G0yX9fUq2TbqLdr86LtU/u+qBQrUhovqxG1n4pd+6FoS2qHWFKUQXfebdKAZYBf/bpDZ52SI+ALwYDXgM39+LT7+1hU7RUpF+PUWzqoFs2vWgkH93/bLG5mTnEz2SCT9XS2lJX19q75sVUH92qxnW9mt828WSnvj0d7avsd/esj9E2gbw70zXH6OtAvX4F+fpz+HsfyGQmMi8rl8iXALMBhsds7nk6yl9fFTpkIXphCvZVhaPQjjX6yJ/97D+vsicpYqExQIeTAB9ZeXoEXtcbLd15GXiZenvs9JShylhDniAjv+JJm4zG+pLXtsLZoZ+5wzKSTpMNJQjrtbHWKPWkmOPtDD5826rCNgMWPhR+rBWNkrMS1iGtjwRgjK7EsYmXiM8vJRCbwicWPH70HvXEjKNiNo/iJ4ScRP0ke4hoOexi5GA6YJS+Mt2axZdiaB1sXS2oVuzqIbcqBP6ewlT0MDpwGrMWnzgP/CLbc2XIGnxGHuFrqqVFP7fR7NznuSM+8jL1M/VFb16Avb2FXQmnPbuaUK5L0YvnQnubQi+XLe/HZJCrTXbOPn+Tt6Ea9SpV33+uTi2a1mMxxyQynk2WtcLPve+pe+ReF0v8v+zd72bsjil48L6/U+c/QqVBt3HHtJanldjwZIyeFFiOvT47rMbRPFv55WpjpUe83",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(colors=["ox_E__1", "ox_E__2", "ox_E__3"]))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(area_adjacent(adj_type=4, color="ox_E__1"))
        self.add_program_line(area_adjacent(adj_type=4, color="ox_E__2"))
        self.add_program_line(area_adjacent(adj_type=4, color="ox_E__3"))
        self.add_program_line(tonton_adjacent_rule(adj_type=4, color="ox_E__1"))
        self.add_program_line(tonton_adjacent_rule(adj_type=4, color="ox_E__2"))
        self.add_program_line(tonton_adjacent_rule(adj_type=4, color="ox_E__3"))
        self.add_program_line(area_color_connected(color="ox_E__1", adj_type=4))
        self.add_program_line(area_color_connected(color="ox_E__2", adj_type=4))
        self.add_program_line(area_color_connected(color="ox_E__3", adj_type=4))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

        self.add_program_line(tonton_cluster_rule())

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            symbol, style = symbol_name.split("__")
            validate_type(symbol, ("ox_B", "ox_E"))
            fail_false(style in ["1", "2", "3"], f"Invalid symbol at ({r}, {c}).")
            self.add_program_line(f"ox_E__{style}({r}, {c}).")

        self.add_program_line(display(item="ox_E__1"))
        self.add_program_line(display(item="ox_E__2"))
        self.add_program_line(display(item="ox_E__3"))

        return self.program
