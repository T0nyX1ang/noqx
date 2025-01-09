"""The Choco Banana solver."""

from typing import List, Tuple

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_cc
from noqx.rule.helper import tag_encode, target_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import all_rect, no_rect
from noqx.solution import solver


def grid_src_same_color_connected(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to check the reachability of same color cells starting from a source.

    An adjacent rule and a grid fact should be defined first.
    """

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    tag_ls = tag_encode("reachable", "Lshape", "adj", adj_type, color)

    r, c = src_cell
    initial = f"{tag}({r}, {c}, {r}, {c}).\n"
    propagation = f"{tag}({r}, {c}, R, C) :- {tag_ls}({r}, {c}), {tag}({r}, {c}, R1, C1), grid(R, C), {tag_ls}(R, C), adj_{adj_type}(R, C, R1, C1).\n"
    return initial + propagation.strip()


def bulb_src_same_color_connected(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells starting from a bulb.

    An adjacent rule and a grid fact should be defined first.
    """

    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    r, c = src_cell
    initial = f"{tag}({r}, {c}, {r}, {c})."
    bulb_constraint = f"{color}(R, C), adj_{adj_type}(R, C, R1, C1), (R - {r}) * (C - {c}) == 0"
    propagation = f"{tag}({r}, {c}, R, C) :- {color}({r}, {c}), {tag}({r}, {c}, R1, C1), {bulb_constraint}."
    return initial + "\n" + propagation


def count_reachable_src(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4):
    """
    Generate a constraint to count the reachable cells starting from a source.

    A grid_src_same_color_connected should be defined first.
    """
    src_r, src_c = src_cell

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    rop, num = target_encode(target)

    return f":- {color}({src_r}, {src_c}), {{ {tag}({src_r}, {src_c}, R, C) }} {rop} {num}."


def count_rect_src(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a cell-relevant constraint for shikaku.

    A bulb_src_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "bulb", "src", "adj", adj_type, color)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {color}({src_r}, {src_c}), {count_r}, {count_c}, CR * CC != {target}."


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_cc(["gray", "white"]))
    solver.add_program_line(adjacent())
    solver.add_program_line(all_rect(color="gray"))
    solver.add_program_line(no_rect(color="white"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        assert isinstance(num, int), f"Clue at ({r}, {c}) must be an integer."
        solver.add_program_line(grid_src_same_color_connected(src_cell=(r, c), color="white"))
        solver.add_program_line(count_reachable_src(num, src_cell=(r, c), color="white"))
        solver.add_program_line(bulb_src_same_color_connected(src_cell=(r, c), color="gray"))
        solver.add_program_line(count_rect_src(num, src_cell=(r, c), color="gray"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Choco Banana",
    "category": "shade",
    "aliases": ["chocobanana"],
    "examples": [
        {
            "data": "m=edit&p=7VXBbtpAEL37K6o5z8HrNWbZG01DL5S0hSqKVhYC6iioRE4BV9Ui/j0zs1a9oWnVHJqoUmX28Xg7O37M4GH3tVlsK1Qpv7RBeqcrV0ZWZgpZaXvN1vtNZV/hsNnf1FsiiBejEV4vNrsqcW1UmRz8wPoh+rfWgQKEjJaCEv0He/DvrJ+gn9IWoCFtHIIyoucdvZR9ZmdBVCnxScuJXhFdrberTTUfB+W9dX6GwPd5LaeZwm39rYLWB39e1bfLNQvLxZ6+zO5mfdfu7JrP9ZemjVXlEf0w2J0+Yld3dpkGu8wescvf4i/bHZTHI5X9IxmeW8feP3XUdHRqD4QTewCt+GhOXkJvQBcsFJEwYMF0Qt5nod8JRXYSUUiOKGlfckSCOb2LSiVkEClKYuhH80PJJCY+pTUrvUjJzYkZ1ZM8OlYkT5y5yB8oVBwlJboSHAlmgjOqIHot+EYwFewJjiXmXPBS8EwwFywkps89+MMugU7BGmoClTgLLXsGb06H5//h1fv3tDJxNIaOCXwHWU7zVPs/mV5oMnEL0ifNp5d/EB1Vlx4Hf4Fw18wX81W9Afpzw9/q6hd69sT4n/M/e3VoGpTJPQ==",
        },
        {"url": "https://puzz.link/p?cbanana/12/12/k417g4k4l4i3n3g4zg83p81p58zg4g3n2i3l3k6g464k", "test": False},
    ],
}
