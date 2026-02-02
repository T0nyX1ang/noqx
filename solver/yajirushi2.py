"""The Yajirushi 2 solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, invert_c, shade_cc
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected


def yajirushi_pair(color: str) -> str:
    """Generate a rule to create Yajirushi pairs and constraints."""
    rule = "{ pair(R, C1, R, C2) } :- arrow_N_W__5(R, C1), arrow_N_W__1(R, C2), C2 > C1 + 1.\n"
    rule += f":- pair(R, C1, R, C2), grid_all(R, C), C1 < C, C < C2, not {color}(R, C).\n"
    rule += "{ pair(R1, C, R2, C) } :- arrow_N_W__7(R1, C), arrow_N_W__3(R2, C), R2 > R1 + 1.\n"
    rule += f":- pair(R1, C, R2, C), grid_all(R, C), R1 < R, R < R2, not {color}(R, C).\n"

    # every arrow symbol should belong to a pair
    rule += ":- arrow_N_W__1(R, C), not pair(_, _, R, C).\n"
    rule += ":- arrow_N_W__3(R, C), not pair(_, _, R, C).\n"
    rule += ":- arrow_N_W__5(R, C), not pair(R, C, _, _).\n"
    rule += ":- arrow_N_W__7(R, C), not pair(R, C, _, _).\n"

    return rule


class Yajirushi2Solver(Solver):
    """The Yajirushi 2 solver."""

    name = "Yajirushi 2"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7Vbfb6JKFH73r2jmtZNcfqlIsg9qtdveltqq8SoxBC0qLTgugu3F+L/3nBmNgLRpNnd3+3CDnjl858z5xfjh+kfshC6twaXqVKIyXKou8a+u4UfaXz0v8l3jjNbjaMFCUCi9a7fpzPHXLr0eLm6arP5yUf9no0ejkXwpxVfS4Kn9dP4Q/H3lqaHcNvXObefWU+b1783GfaV1XunE637kbu4DufHUH/VmncG8pvzbMkdaMrqTytej2V+bev9bydrXMC5tk5qR1GlyaVhEJpQo8JXJmCb3xja5NRKTJl0wEaqNKQliP/KmzGch4ZgMfjdiowJq66gOuB21pgBlCXRT6FVQh6A6YchebNNuiEgdw0p6lGDyBt+OKgnYxsVsWBzeT1kw8RCYOBHMb73wVoSqYFjHj+w53rvK4x1N6qKF4aEF/eMWIMihBVRFC6gVtICdpVsY/Pct1Ma7HTyeB2jCNizsp39U9aPaNbZEU4ihUaJpYqmIRedLRSxVSSzCsyo8a/tFbKgJT1kSrrJyWMUeWRHesoLukNncZ8ZGq+LY8KS8fHREANNbRDsCWEEWgLCZLViVhSfxAPBKLCKlEe6jHhCoRja2IIdctrlUuOzBmGiicnnBpcRlmcsb7tPicsBlk0uNywr3qeKgP/koxFjS5RC1DKXKNHdWYMxVwHVK2Kvd2p/YX1G3peichNJX+Wsh45JFunE4c6Yu/ETMOJi44ZnJwsDx4b67cFYuAaoia+bba+Fnu6/ONCKGYMu0JYMteawM5DO28r1lUYSDKQN68yUL3UITgu7j/L1QaCoINWHhY66mF8f3s73wt0gGmnrh1M9CUQg0krrnJyyDBE60yAApyslEcpe5YUZOtkTn2cllC47j2JXIK+FfS6UKPtD/3ytf+r2Cj0r6aUr7MwxrwcSBNGlyR8kqth0bxk3gPwxFg1ouxjXl0/hvb5f/ilj4AaUdjXm4gNgA/YDbUtYi/B0aS1nz+AlnYbGntAVoAXMBmicvgE75C8ATCgPsHRbDqHkiw6ryXIapTugMU6UZzRqX3gA=",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_cc(colors=["ox_E__8", "arrow_N_W__1", "arrow_N_W__3", "arrow_N_W__5", "arrow_N_W__7"]))
        self.add_program_line(yajirushi_pair(color="ox_E__8"))
        self.add_program_line(adjacent())
        self.add_program_line(invert_c(color="ox_E__8", invert="arrow_all"))
        self.add_program_line(grid_color_connected(color="ox_E__8"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="arrow_all"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name.startswith("arrow_N") and symbol_name.split("__")[1] in ["1", "3", "5", "7"]:
                self.add_program_line(f"{symbol_name.replace('B', 'W')}({r}, {c}).")

            if symbol_name == "ox_E__8":
                self.add_program_line(f"ox_E__8({r}, {c}).")

        self.add_program_line(display(item="arrow_N_W__1", size=2))
        self.add_program_line(display(item="arrow_N_W__3", size=2))
        self.add_program_line(display(item="arrow_N_W__5", size=2))
        self.add_program_line(display(item="arrow_N_W__7", size=2))
        self.add_program_line(display(item="ox_E__8", size=2))

        return self.program
