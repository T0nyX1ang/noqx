"""The All or Nothing solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, display, fill_line, grid, shade_c
from noqx.rule.helper import full_bfs, validate_type
from noqx.rule.neighbor import adjacent, area_border, area_same_color
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import count_area_pass, single_route


def avoid_area_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """Generates a constraint to avoid same {color} cells on the both sides of an area."""
    return f":- area(A, R, C), area(A1, R1, C1), adj_{adj_type}(R, C, R1, C1), A < A1, {color}(R, C), {color}(R1, C1)."


class NothingSolver(Solver):
    """The All or Nothing solver."""

    name = "All or Nothing"
    category = "route"
    aliases = ["allornothing"]
    examples = [
        {
            "data": "m=edit&p=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",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(area_same_color(color="white"))
        self.add_program_line(avoid_area_adjacent(color="not white"))
        self.add_program_line("nothing(A) :- area(A, R, C), not white(R, C).")

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, (ar, _) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            self.add_program_line(count_area_pass(1, _id=i).replace(":-", f":- not nothing({i}),"))

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
