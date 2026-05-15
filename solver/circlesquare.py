"""The Circles and Squares solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import all_rect, avoid_rect


class CircleSquareSolver(Solver):
    """The Circles and Squares solver."""

    name = "Circles & Squares"
    category = "shade"
    aliases = ["circlesandsquares"]
    examples = [
        {
            "data": "m=edit&p=7VU9T8MwEN3zK9DNN8R20ibeSmlZymeLEIqiqg1BVKQKtA0gV/nvnK+BDPWAkCgLsvz0/HyxX87xZf1SzVY5RtRUhD4KaiqQ3KUfc/ebNllsilwfYa/aPJYrIogXwyE+zIp17iVNVOptTaxND82pTkAAgqQuIEVzpbfmTENWLucLQDOmecCIJka7SEl00NJbnresvxOFT/y84UTviGaLVVbk09FOudSJmSDYzY75aUthWb7m0Jix450BEubF22Ojrav78qmCz8VrND12a8YOo6o1qr6MKrdR+ZtG47SuKd/XZHWqE+v6pqVRS8d6W1tHFgXjnd6CimgZgZ/WztgaBD6pck+VztjQpYbStUKoXGrHrQZONXbt1u26VOEHTlkIt+x8PSE6+zIlb8gplIwTyjAaxXjC6DOGjCOOGTDeMvYZA8YOx3TtGX3zFEGSowhBUSrk/pH+krdEdrgwtC087Dj1EhhXq4dZltM16JfL53K92ORAxab24B24J4pCg//6c+j6Y3Pv/7gK/c11Siiv9FGbC4TnajqbZmUB9O9Cq6t4Tz+4e7pzqfcB",
        },
        {
            "data": "m=edit&p=7ZRfS8MwFMXf+ynkPt+HJmm7Nm9zOl/m302GlCJzVhxuVLdVJaPf3Zu76kDuk6AoSNrD6Ul6+yNJs3qqJ8sSlcIMTYohKmpRnNBDiFnHX2HbRrP1vLR72K3X99WSDOJpv493k/mqDPJ2VBFsXGZdF92RzUEBgqZbQYHu3G7csYVptbiZAboh9QOm1DHYjtRkD3d2zP3e9bahCsmftJ7sFdnpbDmdl9eDbXJmczdC8B/b57e9hUX1XEIL45+3ABTczF/u22xV31YPNbwXb9B1mdYNBVCzAzUfoEYG1d8JmhVNQ/N9QajXNvfUlzub7uzQbhpP5FWxXtkNGENlFL6jHTMamFRKIy2mmZTGkZQm4teSWExFhjSU0kysm4lkSikx1mINpUU4pTtiLE+ciuTakVw7EQBpufq8aJp1RGuKzrAesIasMeuAxxyyjll7rBFrwmM6fld8ed98E05uNJ89n1v8t9IiyGFYL+8m05L+2F61eKxWs3UJdC42AbwC37nxh+z/UfnTR6Wf+/C3bfzfhkO/YhG8AQ==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(invert_c(color="gray", invert="white"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="gray"))
        self.add_program_line(all_rect(color="white", square=True))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__2":
                self.add_program_line(f"gray({r}, {c}).")
            if symbol_name == "circle_M__1":
                self.add_program_line(f"not gray({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
