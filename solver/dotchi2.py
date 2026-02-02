"""The Dotchi Dotchi Loop solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, defined, display, fill_line, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_straight, route_turning, single_route
from noqx.rule.variety import classify_area


def dotchi2_constraint() -> str:
    """Generate a constraint for dotchi dotchi loop."""
    rule = ":- black_clue_area(A), area(A, R, C), black_clue(R, C), not turning(R, C).\n"
    rule += ":- white_clue_area(A), area(A, R, C), white_clue(R, C), not straight(R, C)."
    return rule


class DotchiDotchiLoopSolver(Solver):
    """The Dotchi Dotchi Loop solver."""

    name = "Dotchi Dotchi Loop"
    category = "route"
    aliases = ["dotchi2"]
    examples = [
        {
            "data": "m=edit&p=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",
        },
        {"url": "https://pzplus.tck.mn/p.html?dotchi2/7/7/h8ka54i90f0107s01ojj001k50976l003li", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black_clue"))
        self.add_program_line(defined(item="white_clue"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_straight(color="white"))
        self.add_program_line(route_turning(color="white"))
        self.add_program_line(classify_area([("black_clue", "white"), ("white_clue", "white")]))
        self.add_program_line(dotchi2_constraint())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_L__1":
                self.add_program_line(f"white_clue({r}, {c}).")
            if symbol_name == "circle_L__2":
                self.add_program_line(f"black_clue({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
