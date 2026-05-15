"""The Sumiwake solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent, count_covering
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect


class SumiwakeSolver(Solver):
    """The Sumiwake solver."""

    name = "Sumiwake"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VddT9tIFH3nV1R+7UjrmbET29I+BBq67UIIBcSSKIpMMBDqYNZJoGvEf++51+NiO0NbVdvVrrRKMnNyPLn33Pk4dpZ/ruM8EdKltw4Eerw8GfBHBR3+uOZ1PF+lSfRK9Nar6ywHEOJgIC7jdJmI92fXeztZ7+FN74/7YDUaybfu+p17erN78/rD4vd3c53L3UEw3B/uz9VV77ed7cNO/3VnuF6erJL7w4XcvjkZHV8OT69C9Vd/MPKK0YHrvx9d/nLfO/l1a2wkTLYeizAqeqJ4G40d6QhH4SOdiSgOo8diPyr6ojjCJUcEE+Es1ulqPsvSLHeYkxi3V/5QAfaf4SlfJ7RTktIFHhgMeAY4m+ezNJnul8wwGhfHwqHc2/xrgs4iu08oGWmj77NscT4n4jxeYfaW1/M7R2hcWK4vso9rM1ROnkTRKys4+s4KEKSqgGBZASFLBVRYrYK9v7+CcPL0hMX5gBqm0ZjKOXmGwTM8ih7RDriV3J5Fj45SHcSRSFafYtBdOx1Yaa3stLbTnpX2XDttj+2RbrVJk8BN2ren9H07bZ+Tjl1gR9ppu+6unQ7sSgLrMmjXqkTLF2gSuDEnWlqVaGktXku7EmndEFpZ51vbN5vWpHtToH1XaW1dYq1D62j7rtKeXaBHy7AZmzdbazQO0C4fI8XtMU6ZKDS3b7h1ufW53eMxfTpwna5QHZSALOiBoZtwVwreHIwVMA4PYw0MtYw9YEhk7ANDF2PcLrpYII4ZAqNo5l1grD7hEONDMz7E+NCMD6EnNHpC6AmNnjAUvM+A0QOXcdADlzrRA5c60QOXOtEDG50SeZWJqaDNM3V5qMs3GnxoqHTSPNBpIByQ5poeaXJJ5CKHIqy6QntGmwdtdKY5L2JqE1MjJi0t50VM38T0aa5q80zHjfMiZr1eWf4WPfKWv0WPvEYPatFVLQpzS5uOc2H+yXo4F9au0uaTBrMWHta6wgrzT37HGPrJbquYpl6OaepF3xxf56tcGvFp/zKPOORivE8Qh6yLMcaTX/EY2pMGa2gmR2WM+SHnrmKSuVcxvUobaaiNr/MmF0wKc2j2icI+oeNMGA9BfIYZ09yavYfav2CJ/UYewpjWxexDikkuV8VUZr0UrVdtfJ2vcknEJwPivIhDzsBrijhmz6AHNnFQ+xeMRzV2KcbYM+SGVUwyzCqm2Yfom+PrPOeCSZyyVexw63HbYQvp0m38O2/02LVOFFCSMmbrrv9j1vVNbWOUSk+xzZf/3+MmW2PnaJ1fxrMEj2L9i6vk1SDLF3GKb0fX8V3i4HHYWWbpdFmOmiaf4tnKicon8vqVBne7XpwneJ6sUWmW3aXzW1uE6lKDnF/dZnlivURkAq0vhKJLllDnWX7R0vQQp2mzFv6z0qDKO2GDWuV4WK19j/M8e2gwi3h13SBqD7aNSMltazJXcVNi/DFuZVs8T8fTlvPJ4c8YHkTL+f9/l3/xfxdaKPeH/8H8JC/7hpwxJhxuVxwI5249jaeYbJ4v5mWL15N/XD0fiSz/ij89X2zTFpcC+xWjql218S94Uu1qm98wIBK76UFgLTYEtu1EoDbNCOSGH4F7wZIoatuVSFXbmCjVhjdRqro9jSdbnwE=",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent(color="gray"))
        self.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            if d == Direction.TOP_LEFT and symbol_name == "circle_M__1":
                self.add_program_line(count_covering(1, (r, c), d, color="gray"))

            if d == Direction.TOP_LEFT and symbol_name == "circle_M__2":
                self.add_program_line(count_covering(2, (r, c), d, color="gray"))

        for r in range(puzzle.row):
            borders_in_row = [c for c in range(1, puzzle.col) if Point(r, c, Direction.LEFT) in puzzle.edge]
            for i in range(len(borders_in_row) - 1):
                b1, b2 = borders_in_row[i], borders_in_row[i + 1]
                self.add_program_line(avoid_rect(1, b2 - b1 + 2, color="not gray", corner=(r, b1 - 1)))

        for c in range(puzzle.col):
            borders_in_col = [r for r in range(1, puzzle.row) if Point(r, c, Direction.TOP) in puzzle.edge]
            for i in range(len(borders_in_col) - 1):
                b1, b2 = borders_in_col[i], borders_in_col[i + 1]
                self.add_program_line(avoid_rect(b2 - b1 + 2, 1, color="not gray", corner=(b1 - 1, c)))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
