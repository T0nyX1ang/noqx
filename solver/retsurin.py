"""The Retsurin solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route


def count_row_col_xor(target: int, src_cell: Tuple[int, int], color: str = "black") -> str:
    """A rule to ensure the only the number of the shaded color equals to the target, but not both."""
    src_r, src_c = src_cell
    rule = f":- N1 = #count {{ C : {color}({src_r}, C) }}, N2 = #count {{ R : {color}(R, {src_c}) }}, N1 = N2.\n"
    rule += f":- N1 = #count {{ C : {color}({src_r}, C) }}, N2 = #count {{ R : {color}(R, {src_c}) }}, (N1 - {target}) * (N2 - {target}) != 0."

    return rule


class RetsurinSolver(Solver):
    """The Retsurin solver."""

    name = "Retsurin"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VXvb9o8EP7OX1H5ay29cRwgRJomSqFrRyktIFYihAINkDbBzCS0C+J/79kOIgm0qtRX06RNUc7n587n+6E8Wf2MHO5iomFCMTUxrPAYxMRFqmMzebXk6Xqh71onuBqFc8ZBwfim0cBTx1+5+Op+3qyx6vN59cfaDAcDcqFFl1r/sfF4ehd8v/QoJ42W2b5uX3v6rPqtdnZbqp+W2tGqF7rr24CcPfYG3Wm7P6vov+qtgREPbrTi1WD637ra+1KwkxyGhU1cseIqji8sG+kIy5egIY5vrU18bcUtHHfAhLA5xCiI/NCbMJ9xJDECfk3QCMI6qPW92pd2odUUSDTQW4kO6j2oE49PfHfUVEjbsuMuRuLuM3laqChga1dcBsfkfsKCsSeAsRNC+1Zzb4kwBcMqemBPUeJKhlscV1UFzV0FxvsVQJBdBUJVFQjtSAWisM9X4C/Zkdwrw+0WxnIH2Y8sWxTS26vmXu1YG0S0IrJMmBilai1qai0RtZZNWMG5Bc4UbHLIRI0YUXCykZYC9LwHhLVRKQVUckcMI3ekJIHUEVPeIhqYADJpG31NIeqeNCIKySKipCwiissgupYtAAon1gbkvZQNKXUpu9BEHFMpz6XUpCxK2ZQ+dSn7UtakNKQsSZ+yGMNHB0WhKwZ0qwyLGsdnckPlMjSsAgM2itgoIYt+MFubKkrKPsW/CxsWbNSJ+NSZuPBJNr2Fe9JiPHB82LWiYOzy3R7oEa2YP1op75H74kxCZCmGTluQFfIogRYyRMbLZ2zpwz1HAuxM6QjebMG4u7fk3N2H2VuRhCkDqlBjxh9yKT07vp+tRP67MpBitwwUcqCu1N7hnD1nkMAJ5xkgRdSZSO4i18rQyaboPDm524J9O7YF9ILka1Osi6H++5P9kX8yMSLtgzT5eWb8f1jbjjuYGji+wWgZjZwRtFl2SuBGOYdD2TaMJqHinBE6LYzA1weG316z/IQYf4fN9sY8fITUAH2H11LWY/gbHJay5vEDwhLJHnIWoEdoC9A8cwF0SF4AHvAXYG9QmIiaZzGRVZ7IxFUHXCauStOZjRYR956csYuGhVc=",
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
        self.add_program_line(grid_color_connected(color="not black", adj_type="line"))
        self.add_program_line(single_route(color="not black"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"hole({r}, {c}).")

            if isinstance(clue, int):
                self.add_program_line(count_row_col_xor(clue, (r, c), color="black"))

            # empty clue or space or question mark clue (for compatibility)
            if isinstance(clue, str) and (len(clue) == 0 or clue.isspace() or clue == "?"):
                continue

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            if color == Color.BLACK:
                self.add_program_line(f"black({r}, {c}).")

            if color == Color.GRAY:
                self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
