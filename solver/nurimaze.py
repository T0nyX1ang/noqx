"""The Nurimaze solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, display, fill_line, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_same_color
from noqx.rule.reachable import border_color_connected, grid_color_connected
from noqx.rule.route import single_route
from noqx.rule.shape import avoid_rect


class NurimazeSolver(Solver):
    """The Nurimaze solver."""

    name = "Nurimaze"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=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"
        },
        {
            "url": "https://puzz.link/p?nurimaze/10/10/vvvvvtv6rtlrvrvvvuvtvrvvvvvvrnvv7fvve3m3845394c3c2k4946371a46",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false("S" in puzzle.text.values() and "G" in puzzle.text.values(), "S and G squares must be provided.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(colors=["gray", "white", "empty"]))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(area_same_color(color="gray"))
        self.add_program_line(border_color_connected(puzzle.row, puzzle.col, color="gray", adj_type=8))
        self.add_program_line(avoid_rect(2, 2, color="gray"))
        self.add_program_line(avoid_rect(2, 2, color="not gray"))
        self.add_program_line(grid_color_connected(color="not gray", adj_type=4))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(single_route(color="white", path=True))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if clue == "S":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"dead_end({r}, {c}).")

            if clue == "G":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"dead_end({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__1":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"white({r}, {c}).")

            if symbol_name == "triup_M__1":
                self.add_program_line(f"not gray({r}, {c}).")
                self.add_program_line(f"not white({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="gray"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
