"""The Hitori solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c, unique_num
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected


class HitoriSolver(Solver):
    """The Hitori solver."""

    name = "Hitori"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZLb9swDL7nVwQ666CH9fIt65pdsnRbWhSFEQRO5qLBErhz4mFwkP8+SU4rkNlhOyy9DIIIkqLJzyRNefe9LZuKWr+kpYxyv2Qm4hbMxc1O63a931T5kI7a/VPdeIbSm/GYPpabXTUoTlbzwaFzeTei3Ye8IJxQIvzmZE67z/mh+5h3U9rN/BGhmddNeiPh2evE3sfzwF31Ss48Pz3xnn3w7GrdrDbVYtJrPuVFd0tJiPMuPh1Ysq1/VOSEI8irertcB8Wy3PuX2T2tn08nu/Zr/a0lLyGOtBv1cGcvcEWCKxNc+QpX/h6u+Pdw3fx49Gn/4gEv8iJgv0usTewsPxwDrgMR2j8aah0rQ4QJnoYkKSxWOKSQzCt0Ejk+F14hkyjxuQUIZPAvXsWMIfOMA3dZ8K6SGLxnSczw0wp4VwzEVhi7Ct5NEjF2hf0rhRUaesD51QIr4BvoEMEmEeLX0Ls2oBQa1047YG4weqNAMAN7wxgQ28C6GdwXlgFnFufWalA5izNjLSi0xf4d7DsH+8LhvDoJwjmcG+dA3jnDjccZfgPOYPNxJpGPDGDiDHcH52dR+FkULkAiOZfQK8dl5FyB1HCuzyxgtv0w4HEkPEQ6jlREeusnBu1kpO8jZZGqSCfR5jrS+0ivIs0i1dHGhJnzh1MpzqOsn0OiH1EXwFYIHe+7tNRl5fmgILO2eSxXlR/r03a7rJrhtG625Yb4e/Q4ID9J3LHu2f+r9Y2u1lAC9lcX7Nt/WYXPru/v7oaS53ZRLlb1hvi/Mxr15kx/cfT+85sPfgE=",
        },
        {
            "url": "https://puzz.link/p?hitori/10/10/1174453399113445756a2345678aa82513328aa85417a698323227a9411566517a43236688115329986a115274aa99886611",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(unique_num(color="not black", _type="row"))
        self.add_program_line(unique_num(color="not black", _type="col"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent())
        self.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(f"number({r}, {c}, {num}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
