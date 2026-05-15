"""The Choco Banana solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_cc
from noqx.rule.helper import tag_encode, target_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import all_rect, no_rect


def grid_src_same_color_connected(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """Generate a constraint to check the reachability of same color cells starting from a source."""

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    tag_ls = tag_encode("reachable", "Lshape", "adj", adj_type, color)

    r, c = src_cell
    initial = f"{tag}({r}, {c}, {r}, {c}).\n"
    propagation = f"{tag}({r}, {c}, R, C) :- {tag_ls}({r}, {c}), {tag}({r}, {c}, R1, C1), grid(R, C), {tag_ls}(R, C), adj_{adj_type}(R, C, R1, C1).\n"
    return initial + propagation


def bulb_src_same_color_connected(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """Generate a constraint to check the reachability of {color} cells starting from a bulb."""

    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    r, c = src_cell
    initial = f"{tag}({r}, {c}, {r}, {c})."
    bulb_constraint = f"{color}(R, C), adj_{adj_type}(R, C, R1, C1), (R - {r}) * (C - {c}) == 0"
    propagation = f"{tag}({r}, {c}, R, C) :- {color}({r}, {c}), {tag}({r}, {c}, R1, C1), {bulb_constraint}."
    return initial + "\n" + propagation


def count_same_color_reachable_src(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4):
    """Generate a constraint to count the reachable cells starting from a source."""
    src_r, src_c = src_cell

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    rop, num = target_encode(target)

    return f":- {color}({src_r}, {src_c}), {{ {tag}({src_r}, {src_c}, R, C) }} {rop} {num}."


def count_same_color_rect_src(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """Generate a cell-relevant constraint for choco banana."""
    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {color}({src_r}, {src_c}), {count_r}, {count_c}, CR * CC != {target}."


class CBananaSolver(Solver):
    """The Choco Banana solver."""

    name = "Choco Banana"
    category = "shade"
    aliases = ["chocobanana"]
    examples = [
        {
            "data": "m=edit&p=7VVNb9swDL37VxQ862B9+esyZF2zS5ZuS4aiMIzA8Vw0mAN3TjwMCvzfR9FuHLU9rIe2l0LWAx9Jxc+ixOx+t3lTMi7sIyPmM45DxYqmDDVNfxjLzb4qkzM2afe3dYMGY5fTKbvJq13ppUNW5h1MnJgJM5+TFDgwEDg5ZMx8Sw7mS2LmzCwwBCxC36xPEmhejOYVxa113ju5j/Z8sNG8RrPYNEVVrma952uSmiUD+56PtNqasK3/lDDosLyot+uNdazzPX7M7nZzN0R27c/6Vwv3r+iYmfRyF0/IlaNceZQrn5YrXl5unHUdbvt3FLxKUqv9x2hGo7lIDp3VdQAZ41KFtabKgPKR8pFypOFIpZOsXRr4Lo2QyiMNQ4dGdi18gKOD+1ZJNHKunAVcaDcuXamctOoTHrj5oXDk8dDVxyMrUIw81k5c+MLl3PLghCvn9wXXD+LBSRx3n1MNrgmnhIJwiSViRhJ+IvQJNeGMci4IrwjPCRVhQDmhLfJ/HgOQKDtiIFGt6M/EK2hLpaIG83jod78dmZfCom1u8qLEez5vt+uyOZvXzTavABtr58FfoEknUr332jfqtbYE/rM67tvf/BR3F++fuWRw167yVVFXgH/XjPz6kf/V1WN7yLx/",
        },
        {
            "url": "https://puzz.link/p?cbanana/15/15/w29l8q4k4j65l5g6h6m7g7m35i3zh8o7zh9i36m1g5m6h3g6l63j5k6q6l76w",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(["gray", "white"]))
        self.add_program_line(adjacent())
        self.add_program_line(all_rect(color="gray"))
        self.add_program_line(no_rect(color="white"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(grid_src_same_color_connected(src_cell=(r, c), color="white"))
                self.add_program_line(count_same_color_reachable_src(num, src_cell=(r, c), color="white"))
                self.add_program_line(bulb_src_same_color_connected(src_cell=(r, c), color="gray"))
                self.add_program_line(count_same_color_rect_src(num, src_cell=(r, c), color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
