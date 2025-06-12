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
    return rule.strip()


def tonton_adjacent_rule(adj_type: int = 4, color: str = "black") -> str:
    """Generate a rule for getting the adjacent tontonbeya areas."""
    shape_dict = {"ox_E__1": "circle", "ox_E__2": "triangle", "ox_E__3": "square"}
    tag = tag_encode("area_adj", adj_type, color)
    rule = f"{tag}(A1, A) :- {tag}(A, A1), A < A1.\n"
    rule += f":- have_{shape_dict[color]}(A), #count {{ A1: {tag}(A, A1) }} != 1.\n"
    return rule.strip()


class TontonbeyaSolver(Solver):
    """The Tontonbeya solver."""

    name = "Tontonbeya"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VVdT9tIFH3Pr6jmtSOtZ/wZS/sQaNJtF0IooCyJUGSCIaY2po4NrBH/veeOJ3LsmFZC6qoPq8iT4zMz9547H8frb0WQhVwY3OOmxw0u8LMEXizJpWWpx9C/0yiPQ/8dHxT5Ks0AOD8ajfh1EK9D/vl8dbCfDh4/DP558PLZTHw0ik/G9HZ0+/5L8venyMzEaOxNDieHkbwZ/LW/d+wM3zuTYn2Whw/Hidi7PZudXk+mN33573A8s8rZkWF/nl3/8TA4+7M31xoues9l3y8HvPzoz5lgnEk8gl3w8th/Lg/9csjLE3Qx7oE7qAZJwGENp6qf0H5FCgN4rDHgOWD6tNir3ib+vDzljHLsqZkEWZI+hExroPdlmlxGRFwGOZZpvYrudc+6uEq/FnosArKkiPNomcZpRiRxL7wcVPLPO+SbtXyClXxCHfKpKi1/+Avk97vlv2BbvqCAhT+nWs5q6NXwxH9GO1atUO25/8xMA1EEr9ebmQKMbDByZ0y/PUZIb4cyXVBmTSHlSCWWqj2FLl6aqv2gWkO1tmoP1JghJArP5qKPjIiOfy6FqTD+uZTIQVi6uCtQTtgSXNp2hW2bS6eaKx2McSBTYW+LR0wX60DYNYB1HBdxXNSuMO6jq/O6yOtaGuOOujqXi1yejun1uWno8aTH0nHUvd7wiGPpOOqu6zgW4tg6jk3a9HiT4ugxArXQTm2w0HXBO6TQcwXmmpu5lEuvlUXroOc6VOMmpoO5eoyABuHUWOqYEjE3+g3MFdVc4SGmsdGDMVKvp8R6SuKxmVO1pfuqtVTrqK126YC+/QjTEurjWd05Roukz6JmhIRmfRYV9baz+NMi5mbl4c0fzu/vwl305mx4dRO+G6dZEsQwmZNVcB8yODtbp/FiXWTXwTJchE/BMmd+9XHZ7mlwd0VyGcKHtqg4Te/j6K4rwqarQUY3d2kWdnYRGULrK6GoqyPUZZpdtTQ9BnHcrEV9dxvUMsqWcZPKM1jy1nuQZeljg0mCfNUgtuy7ESm8ay1mHjQlBl+DVrakXo6XHnti6sERlv9/hn/bzzBtkfFmJ/tFnvQTOXOsNr4+5RFn98UiWKAmhiPGFW9387DTnY7/vCx1S9LsB5ZVd7bpDuMC+wPv2urt4l+xqa3eNr/jSSR215bAdjgT2LY5gdr1J5A7FgXuFZeiqG2jIlVtr6JUO3ZFqbYda86Cb6jlovcd",
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

        areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(areas):
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
