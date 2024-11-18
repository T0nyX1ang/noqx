"""The Statue Park solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    shapeset = puzzle.param["shapeset"]
    if shapeset == "tetro":
        omino_num, omino_count_type = 4, 1
    elif shapeset == "pento":
        omino_num, omino_count_type = 5, 1
    elif shapeset == "double_tetro":
        omino_num, omino_count_type = 4, 2
    else:
        raise AssertionError("Shape set not supported.")

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))

    solver.add_program_line(all_shapes(f"omino_{omino_num}", color="gray"))
    for i, o_shape in enumerate(OMINOES[omino_num].values()):
        solver.add_program_line(general_shape(f"omino_{omino_num}", i, o_shape, color="gray", adj_type=4))
        solver.add_program_line(count_shape(omino_count_type, name=f"omino_{omino_num}", _id=i, color="gray"))

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.CENTER, "The symbol should be placed in the center."
        if symbol_name == "circle_M__2":
            solver.add_program_line(f"gray({r}, {c}).")
        if symbol_name == "circle_M__1":
            solver.add_program_line(f"not gray({r}, {c}).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Statue Park",
    "category": "var",
    "examples": [
        {
            "url": "https://puzz.link/p?statuepark/12/12/3g3g6000515100003ala0i003g3a0060515160003g3g0000//p",
            "config": {"shapeset": "pento"},
            "test": False,
        },
        {
            "data": "m=edit&p=7VZNa9tAEL37V5Q5T0Gz+rCsm+vGvThJW7uEIIRRVKURlaPUjtpmjf97ZkcqgngOpZAUShH7eH4az74ZxrvefWvzbYlESB76MXrIDIMwwoBiDGksy+ufVXVfl8krnLb3N82WCeL5fI7Xeb0rR2kflY32dpLYKdp3SQoECIYXQYb2Q7K3pwkUzeaqArRLfg9I/GLRRRqmJwO9kPeOzTqRPOZnPWd6ybSotkVdrhed8j5J7QrBbfZGvu0obJrvJfRm3OfOAAtX9Y+bXtu1n5uvbR9F2QHtVNza5S+j8WDUH4w62hl1TDHq/D+b0Ul2OHC/P7LVdZI6158GGg90mewZzwRJ8DLZQ+hzGuJtOmunYg3CSFPHY02NSVXVvHGoqm4381SdGFXVY1Vnk1iLJc/TZbffUQ7y1NREatVEatlEat1ELvexE6NWTkbPbQI9Wm0UGb0nvt4TX69SHxrSpobHbC7DZgRXPItofcG3gp5gKLiQmBPBC8GZYCAYSczYTfNvzjsE3GCuKmK/8fHwP5O31DdyhD59wn9BzUYpLNvtdV6UfBjNms1ds6vuS+Aj/zCCnyAr9d0N8v8WeOlbwPXe++O74O/8VFPuazBGe45w167zddHUwP8g0OmRf6S/uHv+PcNDdfv6Ib/9AtnoEQ==",
            "config": {"shapeset": "double_tetro"},
        },
    ],
    "parameters": {
        "shapeset": {
            "name": "Shape Set",
            "type": "select",
            "default": {"tetro": "Tetrominoes", "pento": "Pentominoes", "double_tetro": "Double Tetrominoes"},
        }
    },
}
