"""The Binario solver."""

from typing import List

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import count, display, grid, invert_c, shade_c
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.shape import avoid_rect


def unique_linecolor(colors: List[str], _type: str = "row") -> str:
    """
    Generates a constraint for unique row / column in a grid.
    At least one pair of cells in the same row / column should have different colors.
    """
    if _type == "row":
        colors_row = ", ".join(
            f"#count {{ C : grid(R1, C), grid(R2, C), {color}(R1, C), not {color}(R2, C) }} = 0" for color in colors
        ).replace("not not ", "")
        return f":- grid(R1, _), grid(R2, _), R1 < R2, {colors_row}."

    if _type == "col":
        colors_col = ", ".join(
            f"#count {{ R : grid(R, C1), grid(R, C2), {color}(R, C1), not {color}(R, C2) }} = 0" for color in colors
        ).replace("not not ", "")
        return f":- grid(_, C1), grid(_, C2), C1 < C2, {colors_col}."

    raise ValueError("Invalid line type, must be one of 'row', 'col'.")


class BinairoSolver(Solver):
    """The Binairo solver."""

    name = "Binairo"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VfbbtNAEH3PV6B93ofdmVnv2m8hNLy03JqqqqyoaoNRIxIMuQBylH9nvTEEVSeqVAGqROR4NBmfzJ65bdbLL+ubRaXJtB8O2mgbL5+HdAdn0226azRdzarime6vV3f1Iipavx4O9Yeb2bLqlR1q3Ns0edH0dfOyKJVVWlG8rRrr5m2xac4KNannt1Olm/P4XGkbH5zukBTVk716mZ632mBntCbqrzo9qldRXVWfVsvd1zdF2Yy0ald6nn7aqmpef61Ux6T9vls9Gm5n3+4623L9vv64Vj89b3XTf4Aq76nyL6qMqVJHdTJdTGbV9dkfZZuPt9uY8XeR73VRttQv9mrYq+fFZtsyaqVN8qrYqMxHN6R/oxbJqiyPVnvf6h3C+gCx0EMg5CEIxHpkzXPkwRqLzYLNMGhrIGdrLTYzNmPfRBDNBqIZxm4ZExS8pARodnhJh1PlMmzGvjNYX5th3z6D4Xhc4hw7yR1yQgYWjcwBNOxhwg1BuPJEMLFEB9CwaEQwscQ4HIGTQwLbhwSHgxuCHCwDeQOdeJxYj5kEvGTATnIYPBuYWDZwSbaw2RgXjfG4MmHfuGiMi8YME8sCZ4cFtj3jWjIeV/Zwe2SP0eGAGQ4JB8wkh07EwMQKrqXgcRU8gIJrKQSDF4INIQxrKbg6IozN2DeeS8GbqWSwfQRvpuIxQY9ThcdVcEMI/tuWgIPH7SM5LIPDW6+zMFXOwmZzBFPlCBJ0BIKPx6FhOhRRkqN4ZtINJ/kiSZOkS/I0YU6SvExykKQkmSWMb09djz6X/SU6pdud7x++3BF3xP1/uHGvVIN6/rleTleVim+y2576rtJdcgTI8eX237/cttk3T20rfWp04uY+7v0A",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row % 2 == 0 and puzzle.col % 2 == 0, "total rows and columns must both be even!")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="circle_M__1"))
        self.add_program_line(invert_c(color="circle_M__1", invert="circle_M__2"))
        self.add_program_line(count(puzzle.row // 2, color="circle_M__1", _type="row"))
        self.add_program_line(count(puzzle.col // 2, color="circle_M__1", _type="col"))
        self.add_program_line(unique_linecolor(colors=["circle_M__1", "circle_M__2"], _type="row"))
        self.add_program_line(unique_linecolor(colors=["circle_M__1", "circle_M__2"], _type="col"))
        self.add_program_line(avoid_rect(1, 3, color="circle_M__1"))
        self.add_program_line(avoid_rect(1, 3, color="circle_M__2"))
        self.add_program_line(avoid_rect(3, 1, color="circle_M__1"))
        self.add_program_line(avoid_rect(3, 1, color="circle_M__2"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__1":
                self.add_program_line(f":- circle_M__2({r}, {c}).")
            else:
                self.add_program_line(f":- circle_M__1({r}, {c}).")

        self.add_program_line(display(item="circle_M__1"))
        self.add_program_line(display(item="circle_M__2"))

        return self.program
