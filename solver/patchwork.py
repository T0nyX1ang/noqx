"""The Patchwork solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_src_color_connected
from noqx.rule.shape import all_rect_region


def count_patchwork_src(target: int, src_cell: Tuple[int, int], color: str = "black") -> str:
    """Generate a constraint to count the reachable patchwork cells starting from a source."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    src_r, src_c = src_cell
    return f":- #count{{ R, C: {tag}({src_r}, {src_c}, R, C), {color}(R, C) }} != {target}."


def avoid_area_adjacent(color: str = "black") -> str:
    """Generate a constraint to avoid the same color in adjacent edges."""
    constraint = f":- grid(R, C), grid(R - 1, C), edge_top(R, C), {color}(R, C), {color}(R - 1, C).\n"
    constraint += f":- grid(R, C), grid(R, C - 1), edge_left(R, C), {color}(R, C), {color}(R, C - 1).\n"
    return constraint.strip()


class PatchworkSolver(Solver):
    """The Patchwork solver."""

    name = "Patchwork"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZNb9s8DL7nVxQ662B9+PMyZJ27S5duS4eiMIzATd01WAJ3Tj0MCvLfS1LqHL+Lm+bN1mHA4Jh8/JCSSEqms/zaFHXJhYc/FXHQcGkR0S2jgG7PXeez+3mZHPFhc39b1QA4Pzs54TfFfFkOMueVD1YmTsyQm7dJxiTjdAuWc/MhWZl3iRlxMwYT4xFwp4AE4xJg2sILsiM6tqTwAI8cBngJcDqrp/NycmqZ90lmzjnDdV7TaIRsUX0rmR1Gz9NqcTVDopjfzB23bK6rL43zEvmam6ENNH0MVLeBqjZQhDZQRFsCxfgPDvSquIeqL29nd9vCjfP1Ggr+EQKeJBnG/qmFUQvHyYopjyURZ0pZFZPS2qqQlB+RCqxLaMnQekbCqoBUbF1in5Tw7NzCk07bMULY6YWwo4SwCwjl/JRdQmjH+3YR4Tv/wPkFuA7kMcI8YG5ba3uuKAc6aj8ImLXjgXl1CMywMwSTzJhqCcyzM4Ry6oyh7DL2apOhUf4Gg5n+h6HoNufB7LsM1qG7OlZkI0CohUhWIC9JnpCUJM9hy7lRJN+Q9Ej6JE/JJyV5QfKYpCYZkE+Ih+bZxwpC1XCeIE8JpYeNgicN0Uq7X4dHyrSEyWM8phKmRyBVzKWGQ6cAaw8wRIFYKC4lFBixDB2/M9VM2c7Xvfy/j8sHGRs39U0xLaFdpNefy6NRVS8K7HWjZnFV1o/P0KfXA/ad0Z0pbPv/WveLt24svvfMN+1XvU6HvviZGXMluDnj7K6ZFJNpBdsBtSNe/mZ+33X39Nd+Dx9s49O2EfWZXW/qM7sW1Wd23Wy7WUvdZ1D7GsKoxxBvLVTKAxHvadiRzc5aPFlJ+EL8uVr0bsTO7T+wIoJLH/5Z/B/zE4en1/Dzu/HinQk+1fngAQ==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region(square=True))
        self.add_program_line(avoid_area_adjacent(color="black"))
        self.add_program_line(avoid_area_adjacent(color="white"))

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
                self.add_program_line(count_patchwork_src(num, (r, c), color="black"))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            if color == Color.GRAY:  # shaded color (DG, GR, LG, BK)
                self.add_program_line(f"gray({r}, {c}).")
            elif color == Color.BLACK:  # black color
                self.add_program_line(f"black({r}, {c}).")
                self.add_program_line(f"not gray({r}, {c}).")
            else:  # safe color (others)
                self.add_program_line(f"white({r}, {c}).")
                self.add_program_line(f"not gray({r}, {c}).")

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="edge_left"))
        self.add_program_line(display(item="edge_top"))

        return self.program
