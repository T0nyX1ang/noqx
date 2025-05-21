"""The Mukkonn Enn solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.loop import loop_turning, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected


def mukkonn_constraint(r: int, c: int, pos: str, num: int) -> str:
    """
    Generate a mukkonn constraint.

    A loop_straight rule, a loop_turning rule, and an adjacent rule should be defined first.
    """

    rule = ""
    if pos == "sudoku_4":
        max_u = f"#max {{ R0: grid(R0, {c}), turning(R0, {c}), R0 < {r} }}"
        rule += f':- grid_direction({r}, {c}, "u"), R = {max_u}, grid(R, _), {r} - R != {num}.\n'

    if pos == "sudoku_5":
        min_r = f"#min {{ C0: grid({r}, C0), turning({r}, C0), C0 > {c} }}"
        rule += f':- grid_direction({r}, {c}, "r"), C = {min_r}, grid(_, C), C - {c} != {num}.\n'

    if pos == "sudoku_6":
        max_l = f"#max {{ C0: grid({r}, C0), turning({r}, C0), C0 < {c} }}"
        rule += f':- grid_direction({r}, {c}, "l"), C = {max_l}, grid(_, C), {c} - C != {num}.\n'

    if pos == "sudoku_7":
        min_d = f"#min {{ R0: grid(R0, {c}), turning(R0, {c}), R0 > {r} }}"
        rule += f':- grid_direction({r}, {c}, "d"), R = {min_d}, grid(R, _), R - {r} != {num}.\n'

    return rule.strip()


class MukkonnSolver(Solver):
    """The Mukkonn Enn solver."""

    name = "Mukkonn Enn"
    category = "loop"
    aliases = ["mukkonnenn"]
    examples = [
        {
            "data": "m=edit&p=7VVNj9owEL3zK5DPPthxPpzcttulF0q7hWqFoqgKu9mCCoWSTVUF8d93ZvLFQA6VqlYcqsDovfmIn8exnf8o0n0mQ3iMlUpqeIxV9Lcu/lT9zFYv6ywaypviZbndA5Dyw2gkn9N1ng3iOisZHMowKu9l+S6KhRZSOPDXIpHlfXQo30flXJZTCAnpgm9cJTkA7zr4QHFEt5VTK8ATwCFggHOAj9vNLs3zyvExisuZFDjMGypGKDbbn5moZSCHksUKHYv0BeaSL1e7OpIXT9tvRZ2rk6Msbyq14x61plOLsFKLqEctTuJP1WZPX7O8WPRJDZPjETr+CcR+iWLU/bmDtoPT6CCsKyIX8CQ6gNXg0a5V+KIhyUKqOXWAOg0xHfECjLSJXoAx0xAY5zTmMRr6nAacWk7DbkzfsErfYGUbw7qWYFWXSFqbGCk9iTGtPtfqY8faSnsW42rsqRrLBYSsyX5IvYNtUVN6b0MDxZYgUKzRgWLyA0Xy21reoYD3IXDpzW2yy2RYh3XeGqbZGqbKGpJhGuoxVdZjTbUea5z1SKTb0JDXhry2ak5HqZbGhU94Dp+wwVlo2izt/hI04rnTxymcO4M+J22KCyfqvHD2DWSxk+dO+s7PndrpG0k7OMsLLy0u90IPRrSZHbIz2OuyNGTfklVkPbJjyrkj+0D2lqxL1qecAE+L3zxPTk+SajH+kpzYsXQrnT7edXmSQSymxf45fczglB6vvmfDyXa/SdfAJsVmke07Pl2mu0zAPXkciF+C/nh0Su//1fnvr07svrq2D/7a5MAWbBchGbwC",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line("mukkonn(R, C) :- grid(R, C), not black(R, C).")

        self.add_program_line(fill_path(color="mukkonn"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="mukkonn", adj_type="loop"))
        self.add_program_line(single_loop(color="mukkonn"))
        self.add_program_line(loop_turning(color="mukkonn"))

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, ("sudoku_4", "sudoku_5", "sudoku_6", "sudoku_7"))
            if pos and isinstance(num, int) and num > 0:
                self.add_program_line(mukkonn_constraint(r, c, pos, num))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"black({r}, {c}).")

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
