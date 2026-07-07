"""The No Three solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected


def no_consecutive_same_distance(color: str = "black") -> str:
    """Generate a rule to avoid consecutive black cells with the same distance."""
    min_r = f"MinR = #max {{ R0: grid(R0, C), {color}(R0, C), R0 < R }}"
    max_r = f"MaxR = #min {{ R0: grid(R0, C), {color}(R0, C), R0 > R }}"
    min_c = f"MinC = #max {{ C0: grid(R, C0), {color}(R, C0), C0 < C }}"
    max_c = f"MaxC = #min {{ C0: grid(R, C0), {color}(R, C0), C0 > C }}"
    rule = f":- grid(R, C), black(R, C), {min_r}, {max_r}, grid(MinR, C), grid(MaxR, C), R - MinR = MaxR - R.\n"
    rule += f":- grid(R, C), black(R, C), {min_c}, {max_c}, grid(R, MinC), grid(R, MaxC), C - MinC = MaxC - C."
    return rule


class NoThreeSolver(Solver):
    """The No Three solver."""

    name = "No Three"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VXRbtMwFH3PV6D7fB8SOwmb38oYvIwOSNFUWVWVZh6NSJWSNAi56r/v+iYoYjgSm8TgAVk+Oj0+iX2ua6f92uWNwZSaPMMQI2oiTblHccw9HNqiPFRGvcBZd9jWDRHE6zne5VVrMNCDaxUc7bmyM7RvlYYIEAT1CFZoP6ijfafsEm1GQ4AxaVe9SRC9HOkNjzt20YtRSHw+cKJLokXZFJVZZ1nvfK+0XSC4iV7x447Crv5mYFiI+13Uu03phE1+oDTtttwPI213W3/pBi/NAbuuOpRFXdWNE512QjvrM2Q/MriZhwxyzOBon8ExTwb32IMMLtYjM5jbz6btNr4A5/4AJ9qdjxRhrbRL82mkZyPN1JFwzhgxLtUR0pjeEtHsP5UdojiZ0FO/nkz4kwl/6vcL4feLREzo0qtLMaFL/3uk9PmpRm+4UoJxQYVEKxlfM4aMCeMVey4ZbxgvGGPGlD0v3Vb85mZRLUAJtzRQ8a8794fWpoXg26JvydP5KtCQdc1dXhj6J2fbfG+AbpFTAN+Bu5Zki/9fLP/2xeJ2Knzy9fJ3DpCmekuJ9hph363zNWUC+oQh6+JxOh2Hh/qzp6VTuQruAQ==",
        },
        {"url": "https://puzz.link/p?nothree/10/10/genceemeienei6eiemeeemeiemenemeiemeeemei6eieneiemecene", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent(color="black"))
        self.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(no_consecutive_same_distance(color="black"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(symbol_name.startswith("circle_SS"), "Invalid symbol type.")

            if d == Direction.CENTER:
                self.add_program_line(f"black({r}, {c}).")

            if d == Direction.TOP:
                self.add_program_line(f":- {{ black({r - 1}, {c}); black({r}, {c}) }} != 1.")

            if d == Direction.LEFT:
                self.add_program_line(f":- {{ black({r}, {c}); black({r}, {c - 1}) }} != 1.")

            if d == Direction.TOP_LEFT:
                self.add_program_line(
                    f":- {{ black({r}, {c}); black({r - 1}, {c}); black({r}, {c - 1}); black({r - 1}, {c - 1}) }} != 1."
                )

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
