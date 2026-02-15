"""The Oasis solver."""

from typing import Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, invert_c, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected, grid_src_color_connected
from noqx.rule.shape import avoid_rect


def count_reachable_oasis(
    target: int,
    src_cell: Tuple[int, int],
    color: str = "black",
    adj_type: Union[int, str] = 4,
):
    """A rule to compare the number of reachable oasis cells to the source cell with a specified target."""

    src_r, src_c = src_cell
    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)

    return f":- #count {{ R0, C0: {tag}({src_r}, {src_c}, R, C), adj_{adj_type}(R, C, R0, C0), clue(R0, C0) }} != {target}."


class OasisSolver(Solver):
    """The Oasis solver."""

    name = "Oasis"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VXdb9owEH/nr6j8WkuL80WItAdKoWtHKS0gVqIIBRogbYJZPmgXxP/es0MXHNKqe1i3SVPwcfc753wf8HP0PXFCFxOJfRQDwzc8KjH4kg2dL2n39L3Yd80jXE/iBQ1Bwfiq1cIzx49cfHG7aDdo/fG0/m1txKMROZOSc2l437o/vgm+nntKSFodo3vZvfTkef1L4+Rabx7r3SQaxO76OiAn94NRf9Ydzmvyj2ZnpKajK0m7GM0+reuDzxVrl4Nd2aQ1M63j9My0EEEYybAIsnF6bW7SSzPt4LQHLoRVG6Mg8WNvSn0aIo4R2NfOXpRBbebqkPuZ1shAIoHeyXQd1FtQp1449d1xOwvUNa20jxE7+4S/zVQU0LXLDmO5MXtKg4nHgIkTQ/uihbdCWAFHlNzRh2S3ldhbnNazCnrvrACCvFTA1KwCpv22CvwVLcm9Zm+3MJYbyH5sWqyQQa4audozNyA75gYpMryqYj2bHFKqgqlqYJLcNNg5R1DDDtDVAlBl4QRALwCGJIQ0WEjtp0kkMQFCWAb7dg3sam7LSiE+UUgRUQsxNZaCsENjWei5rbOo8s6GThHer1suW1zKXPahnThVuDzlUuJS47LN9zS5HHLZ4FLlUud7qmwg7xwZUiBxGYYEFarZ/D4gN0vJqEh8tH8PsysW6iXhzJm68HfqJMHEDY86NAwcHwGZoYj64yjzj90nZxojM+PTfY+ALXkMAfIpXfnesizCi0sAvfmShm6pi4Hu3fy1UMxVEmpCw7tCTo+O74u18LtGgDI2EqA4BKrZs50wpI8CEjjxQgD2iFWI5C4LzYwdMUXnwSmcFuTt2FbQE+LLUrDMBvn/5vkrbx42IumX7p8/z60WtFohOL3CaJWMnTG0mf8EOC4VcCib4apawGFIpbhmf3i1/M9DwzeYLHcW4RI+A/QNStvzluGvsNeet4gfUBVL9pCtAC0hLECLnAXQIW0BeMBcgL1CXixqkb9YVkUKY0cdsBg7ap/ILLRMQi/wIufBQ3blGQ=="
        },
        {
            "url": "https://pzplus.tck.mn/p.html?oasis/17/17/.h6o3h.m.g.o.h.h4h.h.h2u4y.i6i.i.m.k4l.l1l.i4j1g1j4i.l1l.l3k.m.i.i2i.y4u3h.h.h3h.h.o.g.m.h5o2h./",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(defined("clue"))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(invert_c(color="black", invert="white"))
        self.add_program_line(invert_c(color="clue", invert="oasis", _from="white"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent(color="black"))
        self.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="not black"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"clue({r}, {c}).")
            self.add_program_line(f"not black({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color="oasis"))
                self.add_program_line(count_reachable_oasis(num + 1, (r, c), color="oasis"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
