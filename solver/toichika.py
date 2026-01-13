"""The Toichika solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, tag_encode, validate_direction
from noqx.rule.neighbor import adjacent, area_adjacent


def toichika_pair(color: str) -> str:
    """Generate a rule to create Toichika pairs and constraints."""
    rule = "pair(R, C1, R, C2) :- arrow_N_W__5(R, C1), arrow_N_W__1(R, C2), C2 > C1.\n"
    rule += f":- pair(R, C1, R, C2), grid(R, C), C1 < C, C < C2, {color}(R, C).\n"
    rule += "pair(R1, C, R2, C) :- arrow_N_W__7(R1, C), arrow_N_W__3(R2, C), R2 > R1.\n"
    rule += f":- pair(R1, C, R2, C), grid(R, C), R1 < R, R < R2, {color}(R, C).\n"

    # every arrow symbol should belong to a pair
    rule += ":- arrow_N_W__1(R, C), not pair(_, _, R, C).\n"
    rule += ":- arrow_N_W__3(R, C), not pair(_, _, R, C).\n"
    rule += ":- arrow_N_W__5(R, C), not pair(R, C, _, _).\n"
    rule += ":- arrow_N_W__7(R, C), not pair(R, C, _, _).\n"

    # paired numbers must not be in adjacent rooms
    tag = tag_encode("area_adj", 4, None)
    rule += f":- pair(R1, C1, R2, C2), {tag}(A1, A2), area(A1, R1, C1), area(A2, R2, C2).\n"
    rule += f":- pair(R1, C1, R2, C2), {tag}(A2, A1), area(A1, R1, C1), area(A2, R2, C2).\n"

    return rule


class ToichikaSolver(Solver):
    """The Toichika solver."""

    name = "Toichika"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VdrTyJJFP3ur5jU16lk69EvSPYDOjg7syPqqHGFENJiqziN7Tags23873Nu9W2hAZ1HnH0kG6DqcOr2vedWFXWLyZ+zOE+kVvS2kUSPl6cj9zFR4D6KX4ejaZo0X8nWbHqZ5QBS7m5vy/M4nSTy/cnlh62sdfem9cdtNO129Vs1e6eOr7avXn8c//5uZHO93Yn2dvZ2Ruai9dvW5n7Qfh3szSZH0+R2f6w3r466h+d7xxcN81e70/WK7q7y33fPf7ltHf260WMN/Y37otEsWrJ42+wJLaQw+GjRl8V+877YaRZtWRxgSMioL8V4lk5HwyzNcuE4DbsP5YMGsD2Hx26c0FZJagXcYQx4AhjneXY36Aw2S2qv2SsOpaDgm+5xgmKc3SYUjcTR92E2Ph0RcRpPMX+Ty9GNkBYDk9lZ9mnGprr/IItWmcLJN6YAJ1UKBMsUCK1JgTJbTOH45VNo9B8esDwfkcSg2aN8juYwmsOD5j3ajmu1a0+a98JquAnl0hyLwIL2V2itAvB2lbfE6yUeIbZdIOPaQ+iQhXXtG9cq1/qu/eBs2pBkjC+NgUODbWbwWzAh41AaD3oJe2qObQNYlVh7sI/YHr8lz7C9kcZnnz78P2LY+/4cB/xsgGeDBmP4D9l/iLiRV+LILmD4jzBpDmtgjutDf/VsBP8Rx4qgIWIN7vfOOYbkk7FPcdmnR5pZj4V/j/1ozAmtocuX5qGyhx+/8gObkG1CPBtW2pBjhT2aB87d0txyXuTTsn6Ka9neIl+P9XvQ73EsD7ECjhVQLNYZUr6sP4LPRjWfeLbCAXyGlU+a/0obrWP1LPxHrDOis7LkrWpIq0s/6KU1pX700trSHj0w22OPPWKtYV/qdFiXcdGDL/WgBy5zRC8t7z300lb7h9a0wTob0KNYj4IexfaK/FexoO0RW2DWTLja88jRKtajoEezHg09vC4WazTHsDdVjsC8/9EDl3sDPTDHwrpbXnfnU3OO2FeW9xV62LNOsq8w6VHVnqd8GTcoX/avKMfKP80/68H+sbx/0ANTXBwAx+4Y2HKt59rAHQ8hHWLfeMwJEhitOewo6cVTzZ3GP3ZKfVVqD78iqur1l//f4/obPXEwy8/jYYK61D67SF51snwcp/jWmY1Pk3z+/eAyvkkEbgtikqWDSfnUIPkcD6eiWV5YFkdq3LXzVaPSLLtJR9frPFRDNXJ0cZ3lydohIhNof8IVDa1xdZrlZ0ua7uI0refiLnM1ajjKh2mdmuao5Avf3RasMeN4elkjFqp+zVNyvTSZ07guMf4UL0Ubz6fjYUN8Fu6DOm5oef+/2v2rr3a0VOqHL3g/6XT7ipweZhy3l2JXipvZIB5gtgX+RcjneFT2f4THjeu7dL4U/1Tcp3RqXB2+bwB3xp/Ley/BH6z6D/t/+352x2SWP1Oz5oPL9JrKBfaZ4rUwuo5/ok4tjC7zK0WJxK7WJbBrShPY5eoEarVAgVypUeCeKFPkdblSkarlYkWhVuoVhVosWb3+xhc=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent())
        self.add_program_line(area_adjacent())
        self.add_program_line(shade_cc(colors=["gray", "arrow_N_W__1", "arrow_N_W__3", "arrow_N_W__5", "arrow_N_W__7"]))
        self.add_program_line(toichika_pair(color="not gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(1, color="not gray", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"gray({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            fail_false(
                symbol_name.startswith("arrow_N") and symbol_name.split("__")[1] in ["1", "3", "5", "7"],
                f"Invalid symbol at ({r}, {c}).",
            )
            self.add_program_line(f"{symbol_name.replace('B', 'W')}({r}, {c}).")

        self.add_program_line(display(item="gray", size=2))
        self.add_program_line(display(item="arrow_N_W__1", size=2))
        self.add_program_line(display(item="arrow_N_W__3", size=2))
        self.add_program_line(display(item="arrow_N_W__5", size=2))
        self.add_program_line(display(item="arrow_N_W__7", size=2))

        return self.program
