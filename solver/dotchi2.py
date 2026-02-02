"""The Dotchi Dotchi Loop solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, defined, display, fill_line, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_straight, route_turning, single_route


def black_white_area(color: str = "white") -> str:
    """Genearate a constraint to determine the area of the black or white."""
    rule = f"black_area(A) :- area(A, R, C), black_clue(R, C), {color}(R, C).\n"
    rule += f":- black_area(A), area(A, R, C), black_clue(R, C), not {color}(R, C).\n"
    rule += f":- black_area(A), area(A, R, C), white_clue(R, C), {color}(R, C).\n"

    rule += f"white_area(A) :- area(A, R, C), white_clue(R, C), {color}(R, C).\n"
    rule += f":- white_area(A), area(A, R, C), white_clue(R, C), not {color}(R, C).\n"
    rule += f":- white_area(A), area(A, R, C), black_clue(R, C), {color}(R, C)."

    rule += ":- area(A, _, _), not black_area(A), not white_area(A)."
    return rule


def dotchi2_constraint() -> str:
    """Generate a constraint for dotchi dotchi loop."""
    rule = ":- black_area(A), area(A, R, C), black_clue(R, C), not turning(R, C).\n"
    rule += ":- not black_area(A), area(A, R, C), white_clue(R, C), not straight(R, C)."
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
        self.add_program_line(dotchi2_constraint())
        self.add_program_line(black_white_area(color="white"))

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
