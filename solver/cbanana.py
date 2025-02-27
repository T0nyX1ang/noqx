"""The Choco Banana solver."""

from typing import Tuple

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


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_cc(["gray", "white"]))
    solver.add_program_line(adjacent())
    solver.add_program_line(all_rect(color="gray"))
    solver.add_program_line(no_rect(color="white"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        if isinstance(num, int):
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

    return solver.program


__metadata__ = {
    "name": "Choco Banana",
    "category": "shade",
    "aliases": ["chocobanana"],
    "examples": [
        {
            "data": "m=edit&p=7VVNb5tAEL3zK6w5z4FlwXxcKjeNe3FJW7uKIoQsTIlsFZcUm6pay/89MwMpoPrQHppcovWO3psP89jZXQ4/mqwuUDn80wHaqGi4oStT+55Muxur3bEsognOmuO2qgkg3szneJ+Vh8JKuqzUOpkwMjM076MEFCA4NBWkaD5FJ/MhMjGaJYUAA/It2iSH4HUPbyXO6Kp1Kptw3GGCdwTzXZ2XxXrRej5GiVkh8HPeSjVD2Fc/C+h0MM+r/WbHjk12pJc5bHcPXeTQfK2+NV2uSs9oZq3c5QW5upfLsJXL6IJcfov/LDdMz2da9s8keB0lrP1LD4MeLqMT2Tg6gQ6p1KVeS2fAtYly6zuqiPo91aNkb0ynXDugAVH9m/r+iAZcC29oDTqHsllJ0HPljgqU443jeixViVZvwKfjfN8ZyVP+WJ8KWCDt/yce8vP6uGNz/YAr5tMBZ739/zuK64dx1vMUp9VX0oM7sXOxjtgVtQiNFvtOrC3WE7uQnGuxt2KvxLpip5Ljc5P/chuAJtkBgia1TrsnnkFbonkhLg1u4KtfpVYCy6a+z/KCznnc7DdFPYmrep+VQBfr2YJfIFN2pPt6177QXcstsP/pxn35k5/Q6tL5MzcID806W+dVCfS5RvF7f/ifXT1dD5Bvq7yabLLvNCC1HgE=",
        },
        {
            "url": "https://puzz.link/p?cbanana/15/15/w29l8q4k4j65l5g6h6m7g7m35i3zh8o7zh9i36m1g5m6h3g6l63j5k6q6l76w",
            "test": False,
        },
    ],
}
