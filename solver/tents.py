"""The Tents solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent


def identical_adjacent_map(known_cells: List[Tuple[int, int]], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate n * (n - 1) / 2 constraints and n rules to enforce identical adjacent cell maps.
    n is the number of known source cells.
    """
    rules = "\n".join(
        f"{{ map_{r}_{c}(R, C): adj_{adj_type}(R, C, {r}, {c}), {color}(R, C) }} = 1 :- grid({r}, {c})."
        for r, c in known_cells
    )  # n rules are generated

    constraints = ""
    for i, (r1, c1) in enumerate(known_cells):
        for j in range(i + 1, len(known_cells)):
            r2, c2 = known_cells[j]
            constraints += f":- map_{r1}_{c1}(R, C), map_{r2}_{c2}(R, C).\n"

    return rules + "\n" + constraints


class TentsSolver(Solver):
    """The Tents solver."""

    name = "Tents"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VZNb9swDL3nVxQ66yDRH7J9GbKu2SVLtyVDERhG4GQeEiyZMyceBgX576Not64rXRag7aVwRJCPlPlISVYOv+u8KrgMzM+LuOASn1BENGQkaNw/s81xWyRXfFgf12WFCue3oxH/kW8PxSCVNFdmg5OOEz3k+mOSMsk4AxySZVx/SU76U6InXE/RxTCW63ETBKjedOod+Y123YBSoD5pdVTnqK421WpbLMYN8jlJ9Ywzk+c9zTYq25V/CtbyMPaq3C03BljmRyzmsN7sW8+h/l7+rNl9ijPXw4bu3EHX6+h6D3Q9N11o6R6LX8fDRVzbmTbNODufsd1fkegiSQ3nb50adeo0OZ0NnxPzJU4FXCdaEeYDml5neubF71gH+H1/iKZ8MAPR8wayb/bfHcS9zCp6kkoGfi9AxtCzIVKP3oflSCpqjkWFkmg96jALPRuKLUjZE6PAguLIgqQQDswRJx1xAA7MtzFP2ZjvwAK7MOloiXT0RCpH3ii0sdiF2XlB2LWBZ+cFR23g25xB2f0Dx6qBcuR11AbKXl5Qdm2g7LUE5ag3esoPt+SINiaQnOEB5Noj+YGkIBmQHFPMDck7ktckfZIhxShzhP/rkPfOBhGE5yeYhs3d4XrUm+cSTzZI2aTeLYvqalJWu3yLV8B0ne8LhnfsecD+Mhr0TfTfrt0XvnZN68XF5/J1PhMpdhX/z+lbzvb1Il+sStxTIntxlvi5yAb/AA==",
        },
        {"url": "https://puzz.link/p?tents/13/13/h3g03h1g2j3h32g24g2g55233hi11131331f78625243a872550", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="tents__2"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(avoid_same_color_adjacent(color="tents__2", adj_type=8))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int) and isinstance(num, int):
                self.add_program_line(count(num, color="tents__2", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int) and isinstance(num, int):
                self.add_program_line(count(num, color="tents__2", _type="row", _id=r))

        all_trees: List[Tuple[int, int]] = []
        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "tents__1":
                all_trees.append((r, c))
                self.add_program_line(f"not tents__2({r}, {c}).")
            if symbol_name == "tents__2":
                self.add_program_line(f"tents__2({r}, {c}).")

        self.add_program_line(identical_adjacent_map(all_trees, color="tents__2", adj_type=4))
        self.add_program_line(count(len(all_trees), color="tents__2", _type="grid"))
        self.add_program_line(display(item="tents__2"))

        return self.program
