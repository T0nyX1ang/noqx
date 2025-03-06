"""The Statue Park solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape


class StatueParkSolver(Solver):
    """The Statue Park solver."""

    name = "Statue Park"
    category = "var"
    examples = [
        {
            "url": "https://puzz.link/p?statuepark/12/12/3g3g6000515100003ala0i003g3a0060515160003g3g0000//p",
            "config": {"shapeset": "pento"},
            "test": False,
        },
        {
            "data": "m=edit&p=7VZNa9tAEL37V5Q5T0Gz+rCsm+vGvThJW7uEIIRRVKURlaPUjtpmjf97ZkcqgngOpZAUShH7eH4az74ZxrvefWvzbYlESB76MXrIDIMwwoBiDGksy+ufVXVfl8krnLb3N82WCeL5fI7Xeb0rR2kflY32dpLYKdp3SQoECIYXQYb2Q7K3pwkUzeaqArRLfg9I/GLRRRqmJwO9kPeOzTqRPOZnPWd6ybSotkVdrhed8j5J7QrBbfZGvu0obJrvJfRm3OfOAAtX9Y+bXtu1n5uvbR9F2QHtVNza5S+j8WDUH4w62hl1TDHq/D+b0Ul2OHC/P7LVdZI6158GGg90mewZzwRJ8DLZQ+hzGuJtOmunYg3CSFPHY02NSVXVvHGoqm4381SdGFXVY1Vnk1iLJc/TZbffUQ7y1NREatVEatlEat1ELvexE6NWTkbPbQI9Wm0UGb0nvt4TX69SHxrSpobHbC7DZgRXPItofcG3gp5gKLiQmBPBC8GZYCAYSczYTfNvzjsE3GCuKmK/8fHwP5O31DdyhD59wn9BzUYpLNvtdV6UfBjNms1ds6vuS+Aj/zCCnyAr9d0N8v8WeOlbwPXe++O74O/8VFPuazBGe45w167zddHUwP8g0OmRf6S/uHv+PcNDdfv6Ib/9AtnoEQ==",
            "config": {"shapeset": "double_tetro"},
        },
    ]
    parameters = {
        "shapeset": {
            "name": "Shape Set",
            "type": "select",
            "default": {"tetro": "Tetrominoes", "pento": "Pentominoes", "double_tetro": "Double Tetrominoes"},
        }
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        shapeset = puzzle.param["shapeset"]
        if shapeset == "tetro":
            omino_num, omino_count_type = 4, 1
        elif shapeset == "pento":
            omino_num, omino_count_type = 5, 1
        elif shapeset == "double_tetro":
            omino_num, omino_count_type = 4, 2
        else:
            raise ValueError("Shape set not supported.")

        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))

        self.add_program_line(all_shapes(f"omino_{omino_num}", color="gray"))
        for i, o_shape in enumerate(OMINOES[omino_num].values()):
            self.add_program_line(general_shape(f"omino_{omino_num}", i, o_shape, color="gray", adj_type=4))
            self.add_program_line(count_shape(omino_count_type, name=f"omino_{omino_num}", _id=i, color="gray"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__2":
                self.add_program_line(f"gray({r}, {c}).")
            if symbol_name == "circle_M__1":
                self.add_program_line(f"not gray({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"gray({r}, {c}).")
            else:
                self.add_program_line(f"not gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
