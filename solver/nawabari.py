"""The Nawabari solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region


class NawabariSolver(Solver):
    """The Nawabari solver."""

    name = "Nawabari"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VXfb5swEH7nr4j8tEl+wBgI+GXKumQvGd3WTFWFUAQpW9GS0fFjPxzlf+/dwWrYIk1VpFaTJvCX7+5s8/nsc+qvbVrlXNj4yoDDLzyuCKg5gU/N7p9V0WxzNeGztrkpKyCcny8W/GO6rXMr7nsl1l6HSs+4fq1i5jBOTbCE63dqr98oHXF9ASHGBfiWwATjDtC5oZcUR3bWOYUNPOo50Cugm6LabPP1svO8VbFecYbfeUmjkbJd+S1n3TCyN+UuK9CRpQ0spr4pbvtI3V6Xn9u+r0gOXM86ufMjcqWRi7STi+yIXFzFyXLz60953WbHtIbJ4QA5fw9q1ypG4R8MDQy9UHvASO2ZtGGoAxtN28KkC6Y0pjeOhvidF6C6d7g+OPCYdKYnRuYURw/MYGQGU5xMmslC/LaJCxtnowzee8YzCIFTGHnCwcUM4u5vM7qof9DfQ/kD28fxZvXCRwXD+DAdkEBBabwiXBA6hCvIMteS8BWhTegRLqnPnPCS8IzQJfSpzxT36UE7eboc5kuHqTCAKhVQ7Hgy5F8lxrK7J8aP9+/5Eitmc6isSVRWu3QL1RW1uyyvftlwlx0s9oNRo0Pi/r/enuJ6w/zbj1wap1ZqDKm9ryquzzm7bdfpelPCOYP8YdiHP9kHBqTzR+DR1w03AGvyqiqasvo5efYl/Z5maVU8Z4l1Bw==",
        },
        {"url": "https://puzz.link/p?nawabari/10/10/b4c1d2b1c2c2j4b0b1a3b3j3b1a2b0b4j2c3c2b1d1c3b", "test": False},
    ]

    def program(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(f":- {{ upleft(R, C) }} != {len(puzzle.text)}.")

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            self.add_program_line(f"clue({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

            if isinstance(num, int):
                self.add_program_line(count_adjacent_edges(num, (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

        tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
        self.add_program_line(f":- clue(R, C), clue(R1, C1), (R, C) != (R1, C1), {tag}(R, C, R, C1), {tag}(R1, C1, R, C1).")
        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.asp_program
