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
            "data": "m=edit&p=7VVNT4NAEL3zK8yc5wC7gLq3qtWL39SYhpCG4moba6ilGLMN/93ZoUqikGjjx8Vs9uXx9gGPWRiKxzJdaAxpyB100aMhwpCn5/s83fUYTJczrbawVy4n+YII4tkp3qazQjvx2pQ4K7OrTA/NkYpBAPL0IEFzoVbmRJkhmoiWAH3Sjol5gIJov6HXvG7Zfi16LvHTNSc6JJpNF9lMj6Kols5VbAYI9kZ7fLql8JA/aajP4+MsfxhPrTBOl/QwxWQ6X68U5U1+X8LrPSo0vTpv9JpXNHllk1e+5ZXtecW35NU3d7oox21hd5OqoqpfUtyRim3yq4buNDRSq8qmsugxDtUKQp8u4+G7eOD5QYcetutBhz/o8IftfiHa/SIQHbps1aXo0GX7daRs81ONDrlSgnFAhUQjGQ8YXcaA8Zg9fcZrxn1GnzFkz7bdik9uFtUClLDRQPkfd+6HssVCcBOoR7A5T5wYonJxm2aa3tpoks41UHeoHHgGnrEkm//fMP6mYdgdcDduG3/zYcRUWynRnCHMy1E6yvIZ0C8HWRdf08VH/deflr62xHkB",
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
