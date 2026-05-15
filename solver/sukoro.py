"""The Sukoro solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_num, grid, invert_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent
from noqx.rule.reachable import grid_color_connected


def num_count_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """Generate a constraint for counting the number of adjacent black cells."""
    return f":- number(R, C, N), N != #count {{ R1, C1 : adj_{adj_type}(R, C, R1, C1), {color}(R1, C1) }}."


class SukoroSolver(Solver):
    """The Sukoro solver."""

    name = "Sukoro"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VRNT8JAEL33V5g576HbXUrpDRW8IH6AMaRpmoI1ECHFQg1Z0v/u7FAtS+CAUYmJKTu8eTM7fZ39WLzmcZYwbuuf8Bj+4yO5R8PxXBp2+fQny2nin7FmvhynGQLGbtpt9hxPF4kVlFmhtVYNXzWZuvID4MDAwcEhZOrOX6trX3WZ6mEIGEeus0lyELYq+EhxjS42JLcRd0uMcIBwNMlG0yTqbJhbP1B9Bvo95zRbQ5ilbwmUOrQ/SmfDiSaG8RI/ZjGezMvIIn9KX3L4eEXBVHNHrqzkikqu+JQr9st1SrnpKmr9gNRGWBTY8nsUG/mB1v1QQa+CPX9daE1rEBynClxnWhUQAl1euQ3Dldp1Pt0aN6KubZRyHSNabxhRbntGLe6Yxbiwd3xhzhd1My5ds15t1zc/hbtyK47N4NSSAdk2WYdsHzvGlCB7SdYmWyPboZwW2UeyF2QlWZdy6rrnR63KthwoG1FtGZBauqyYH1IciM0NYD61v8eFVgDdfDZMsrNums3iKR6d3jieJ4D3U2HBCmjQ7pL/V9YJrizdfvvLR+Q0JzZQPYYnRN0wmOdRHI1S3FfYN81LuZ8/lH8sf6j+fn5woM7gYP438L++WnhhhdY7",
        },
        {"url": "https://puzz.link/p?sukoro/11/11/p2324d14e3b2b3g3b1h31c13h2b3g1b2b1e23d1434p", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_num(_range=range(0, 5), color="white"))
        self.add_program_line(invert_c(color="white", invert="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(num_count_adjacent(color="black"))
        self.add_program_line(avoid_same_number_adjacent())

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "ox_E__1":
                self.add_program_line(f"not white({r}, {c}).")
            if symbol_name in ("ox_E__4", "ox_E__7"):
                self.add_program_line(f"white({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
