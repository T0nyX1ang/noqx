"""The City Space solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import border_color_connected, bulb_src_color_connected, count_reachable_src, grid_color_connected
from noqx.rule.shape import all_rect, avoid_rect


def constrain_rect_shape():
    """Constrain rectangle shapes for City Space."""
    rule = f':- rect(R, C, "{Direction.BOTTOM_RIGHT}").\n'  # the shapes should be 1xn
    rule += f':- rect(R, C, "{Direction.TOP_LEFT}"), not rect(R, C + 1, "{Direction.TOP}"), not rect(R + 1, C, "{Direction.LEFT}").'  # the shapes cannot be 1x1
    return rule


class CitySpaceSolver(Solver):
    """The City Space solver."""

    name = "City Space"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VPBjpswEL3zFas5z8HYJiS+VOl200uabZtUqxVCEaGsFhVESkJVOeLfOx5CUKpN1UqrbQ+Vw9Ob53GYN3h2X5ukzjCkpcYo0KelhOZnJNyvX6t8X2TmCqfN/rGqiSDezmb4kBS7DL3omBZ7Bzsxdor2rYlAAh6fGO0Hc7DvjF2gXdIWoB8jlE2xz9OqqGroNTsn5gNKojcDveN9x6470RfEF0dO9J5omtdpka3nnfLeRHaF4N79mk87CmX1LYPuGMdpVW5yJ2ySPTncPeZbQEUbu+Zz9aWB/g0t2mnnYNk70L92oAYH6uRAPe1APouDYls9Ufskblv6LB+p+rWJnJFPAx0PdGkOrSvoAFLTUUVXgY7TvylxFmoX6iEMKQxP4cjt+uIUh+oseyzOsicuhFcwCKMzgQryuax7xhmjZFxR1WgV4xtGwRgwzjnnhvGO8ZpRM444J3S+f7Mz3BNJvQjA6K5NL1BbJDWPZL+C549iL4JlUz8kaUb3adGUm6y+WlR1mRRA09x68B34oRsgXfr/Af8nB9x9IvFHY/73ZyuiVtMNt7cI22adrKnN3Cmnq+AnXV3Q9QU9uKDL+MW7QIMcez8A"
        },
        {"url": "https://pzplus.tck.mn/p.html?cityspace/9/9/g2h4h2l6r6g5k6oakbg9r6l2h2h4g", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="not black", adj_type=4))
        self.add_program_line(border_color_connected(puzzle.row, puzzle.col, color="black", adj_type=8))
        self.add_program_line(avoid_rect(2, 2, color="not black"))
        self.add_program_line(all_rect(color="black"))
        self.add_program_line(constrain_rect_shape())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="not black", adj_type=4))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num, (r, c), main_type="bulb", color="not black", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
