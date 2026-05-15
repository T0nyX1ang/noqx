"""The Koburin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route


class KoburinSolver(Solver):
    """The Koburin solver."""

    name = "Koburin"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VZNb5tAEL37V0R7ngP7YcBcKjeNe6FOW7uKImRZmBIFFRcXm6pay/+9swPULoEoqJUTVRXe0ds3u943s8yI7bcizGPg3PykCxYgAjW0aXAuaFjVM092aexdwLjY3Wc5AoDryQTuwnQbD4Jq1WKw1yNPj0G/9QLGGTCBg7MF6A/eXr/z9BT0DF0MFHJ+uUggvDrCG/IbdFmS3EI8rTDCW4RRkkdpvPRL5r0X6Dkwc85r2m0gW2ffY1bpMPMoW68SQ6zCHQazvU82lWdbfM6+FKw+4gB6XMr1W+TKo1z5S65slyv+itx0k7UJHS0OB0z4R5S69AKj+tMRukc48/YHo2jPpF3HWN4KU8IQr46ErQwhTwinsYVbtEecMJw313DZZMSDXUOnydiWYawTxhXN/3Hd39ZgYJzCuyU7ISvIzjF60JLsG7IW2SFZn9Zckb0he0lWkbVpjWPy98QMM4lSVZnnPxHFlIuXNHKBOXJUAuWAwqglMClrhJwtak7ipcknRhNIQXXefIb/LrsYBGxW5HdhFGMZ+cnX+GKa5eswxdm0WK/ivJ5j/zoM2A9GI5CmHf5vaWdvaSb5Vq/G9vxdINAzwMrS18A2xTJcRhm+XZi1APNdFXCHs6zp7p1Y5t07sfLbndg82hxdIpEf9uPtnnxXcpSr+jpGraE94nAs9yU62q/oMceLjKP/DT5zHJ3ZPUfa+x6OnwMPHGfvffjZsBj8BA==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_line(color="not black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(grid_color_connected(color="not black", adj_type="line"))
        self.add_program_line(single_route(color="not black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"hole({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(target=num, src_cell=(r, c), color="black", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"black({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
