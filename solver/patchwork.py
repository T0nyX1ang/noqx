"""The Patchwork solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
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
    constraint = f':- grid(R, C), grid(R - 1, C), edge(R, C, "{Direction.TOP}"), {color}(R, C), {color}(R - 1, C).\n'
    constraint += f':- grid(R, C), grid(R, C - 1), edge(R, C, "{Direction.LEFT}"), {color}(R, C), {color}(R, C - 1).\n'
    return constraint


class PatchworkSolver(Solver):
    """The Patchwork solver."""

    name = "Patchwork"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVLb9pAEL7zK6I978H78PNS0dT0QklbqKLKQsgQ06CCnBpcVYv83zs7u8QxxSGUNFWlynjm8zez3pnZ8bD+VqZFRpmjfyKgoOGSLMCbBx7ejr1Gi80yiy5ot9zc5gUASq96PTpPl+usk1ivcWerwkh1qXobJYQTijcjY6o+RFv1LlIDqoZgIjQArg+IEcoBxjW8RrtGl4ZkDuCBxQA/A5wtitkym/QN8z5K1IgSvc9rXK0hWeXfM2KW4fMsX00XmkiX86Xl1uVN/rUku5dXVHVNoPEuUFkHKupAxX2g4nCg/DkCnaYbqPr6dnF3KNxwXFVQ8I8Q8CRKdOyfahjUcBhtiXBIFFAihFEhKimN8lG5ASrPuPiG9I1nwIzyUIXGJXRRMcexmltt1jAmrfasNhswYf2E2YJJy7vMauvvWT9P71Ppym4xclNr01eYA7baPeHveei8GoTOsLHEx5eKmtB5NpZgTo01mF1CXj1kcJX7gNGZ7jH+/ntksM/oOjR3d71GgFALFm0r3WBa9lBylCM4cqoEyjcoHZQuyj76xCivUV6ilCg99PF10zy5rSBUCf0EeXIovYtPEqLl5rzOj5RIDi8PdZty1wAuQsolNJ0ALB3AzGAmKOe+wdy3/NFUE2EmX/Ny/z1u3EnIsCzm6SyDcRHffMkuBnmxSvWsG5SraVbsnmFOVx3yg+CdCD32/4/uFx/duvjOE7+05/qczv3wEzWkglF1RcldOUknsxyOA2qHPP/D/Kn7nugv3RbeO8TH9SBqM9vZ1Ga2I6rNbKfZYbPkss0gTjX4QYshPFiomHosPNFwJJujtXi0kvAP8fdq0XoQR4//zIowyl3398yPNE+r4ddv48UnE/xVjzs/AQ==",
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

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
                self.add_program_line(count_patchwork_src(num, (r, c), color="black"))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        for (r, c, _, _), color in puzzle.surface.items():
            if color == Color.GRAY:  # shaded color (DG, GR, LG, BK)
                self.add_program_line(f"gray({r}, {c}).")
            elif color == Color.BLACK:  # black color
                self.add_program_line(f"black({r}, {c}).")
                self.add_program_line(f"not gray({r}, {c}).")
            else:  # safe color (others)
                self.add_program_line(f"white({r}, {c}).")
                self.add_program_line(f"not gray({r}, {c}).")

        self.add_program_line(display(item="black", size=2))
        self.add_program_line(display(item="edge", size=3))

        return self.program
