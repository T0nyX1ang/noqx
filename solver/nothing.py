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
