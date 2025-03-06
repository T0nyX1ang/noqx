"""The Mochinyoro solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_rect_src, grid_color_connected
from noqx.rule.shape import all_rect, avoid_rect, no_rect


class MochinyoroSolver(Solver):
    """The Mochinyoro solver."""

    name = "Mochinyoro"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVRj5pAEH73V1zmeR5YFhB5aez17Iv12mpzuRBikHKRFItFaa5r/O83M9AA3jWpaWKTptH98s3szO7HjIy7b1VcpqgUf7WPFhJDx/VkKWXLsprPItvnaXCF42q/LkoiiLeTCT7E+S4dhE1UNDiYUWDGaN4GIShAsGkpiNB8CA7mXWBmaOa0BajIN62DbKI3Lb2TfWbXtVNZxGcNJ3pPNMnKJE+X09rzPgjNAoHveS3ZTGFTfE+h0cF2UmxWGTtW8Z4eZrfOts3OrvpcfKmaWBUd0YxrufOfcllOI1e3cpnWcpm9IJfT/lxuvi1eEjqKjkcq+EeSugxCVv2ppX5L58GBcBYcQHuc+opU1F0BxyYHt70xh2RS3xvT1SfhnnPiGFq9fF/18v3+cSO+rGP6vVxljXrbSrl922bxnXjdP07p/m3KYfUd22XxHdtj7d2HUUOW3/ecnOnznU7H5mdoM6jMSop9LzgRtAUX1As0WvCNoCXoCk4l5kbwTvBa0BH0JGbI3fzNfgMXx0bQVAOnbv4FtIWaS/X84/673mgQwrwqH+IkpVd0Vm1WaXk1K8pNnANNw+MAHkFWqHm4/h+QFx+QXHzrrDH599/ikOpK75K5RdhWy3iZFDnQvyuKX//Cf278uf7n51+8ajRi6FeQrLOvP4qygGjwBA==",
        },
        {
            "url": "https://puzz.link/p?mochinyoro/17/17/hdzmenajfzh71zw4zu6i5zu3zw-108zh2jcn9zmbh",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(invert_c(color="black", invert="green"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="not black", adj_type=8, grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(all_rect(color="green"))
        self.add_program_line(no_rect(color="black"))

        fail_false(len(puzzle.text) > 0, "No clues found.")
        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            self.add_program_line(f"clue({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="not black"))
            if isinstance(num, int):
                self.add_program_line(count_rect_src(num, (r, c), color="not black"))

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        tag = tag_encode("reachable", "bulb", "src", "adj", 4, "not black")
        self.add_program_line(f":- clue(R, C), clue(R1, C1), (R, C) != (R1, C1), {tag}(R, C, R, C1), {tag}(R1, C1, R, C1).")
        self.add_program_line(display(item="black"))

        return self.program
