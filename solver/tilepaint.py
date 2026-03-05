"""The Tilepaint solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import area_same_color


class TilepaintSolver(Solver):
    """The Tilepaint solver."""

    name = "Tilepaint"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=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",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(area_same_color(color="gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, (ar, _) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
                validate_type(label, f"corner_{Direction.BOTTOM_LEFT}")
                self.add_program_line(count(num, color="gray", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
                validate_type(label, f"corner_{Direction.TOP_RIGHT}")
                self.add_program_line(count(num, color="gray", _type="row", _id=r))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
