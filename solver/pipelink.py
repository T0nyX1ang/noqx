"""The Pipe Link solver."""

from noqx.manager import Solver
from noqx.puzzle import Point, Puzzle
from noqx.rule.common import direction, display, fill_path, grid
from noqx.rule.helper import fail_false, tag_encode
from noqx.rule.loop import intersect_loop


def adjacent_loop_intersect() -> str:
    """
    Generate a constraint to check adjacent loop intersection.

    An intersect_loop rule should be defined first.
    """
    adj = 'direction_type("H"; "V").\n'
    adj += 'adj_loop_intersect(R, C, "H", R, C, "V") :- grid(R, C), not intersection(R, C).\n'
    adj += 'adj_loop_intersect(R, C, "H", R, C + 1, "H") :- grid(R, C), grid(R, C+1), grid_direction(R, C, "r").\n'
    adj += 'adj_loop_intersect(R, C, "V", R + 1, C, "V") :- grid(R, C), grid(R+1, C), grid_direction(R, C, "d").\n'
    adj += "adj_loop_intersect(R0, C0, T0, R, C, T) :- adj_loop_intersect(R, C, T, R0, C0, T0)."
    return adj


def loop_intersect_connected(color: str = "black") -> str:
    """Generate a constraint to check the reachability of {color} cells connected to loops."""
    tag = tag_encode("reachable", "grid", "adj", "loop", "intersection", color)
    rule = f'{tag}(R, C, "H") :- (R, C) = #min{{ (R1, C1): grid(R1, C1), {color}(R1, C1) }}.\n'
    rule += f"{tag}(R, C, T) :- {tag}(R1, C1, T1), grid(R, C), {color}(R, C), adj_loop_intersect(R, C, T, R1, C1, T1).\n"
    rule += f":- grid(R, C), {color}(R, C), direction_type(T), not {tag}(R, C, T).\n"
    return rule


class PipeLinkSolver(Solver):
    """The Pipe Link solver."""

    name = "Pipe Link"
    category = "loop"
    examples = [
        {
            "data": "m=edit&p=7Zbfb6M4EMff81dUfl1La4OxAWkf0iZdqUpzzW16vRZVEU1IQ0vCLpC2our/vuMfiB+hq3u5U09aESaffG2PZwZrSP5jH2YRpkR+bBfDN1yMuuq2XK5uYq55XCSRf4SH+2KTZgAY/3F6itdhkkf47PrhePQ4fB4P//7s3Nj25XT96WE0u3xYXf1FZyT+nJFp4u7OL0bHyaev5c35ZvgUjSN+kafLTRKFq7C8uTp7SXan7v1mTU/ONifuOtyR/Ic7956OZ1++DAITyO3gtfT8cojLr36ALITVTdEtLmf+a3nulxNcfoMhhCloEyAHYQtwDEg1XqlxSSdapAR4ahjwGnAZZ8skWky0cuEH5Rwjuc+xWi0RbdOnCOll6vcy3d7FUrgLC6hXvom/m5F8v0of92YuOETbfVLEyzRJMylK7Q2Xw/dTsOsUJOoUJPWkIDP7l1Pw+lN4g8fzJySx8AOZz2WNbo3f/FewU2WpstfKniprKTuHqbi0lR0pS5R1lJ34r8h2MLds5FtYIrOEQua1kNEKuc1rNBM4oPagkCl0KKBXIWN6AueAegIgd4xqYc70XIkOUSgY5tyqkHG9sSswF9qDQqdCxmsU2hklBNit2dPuqOVhQbU/zToTyQ5psKXzpoxhYTfZ+AF2rAab4lBOsGDGD7BjmxigPk0WplaUCtjXxAwsiE6FEsjbMz6BuYnfg4JyPR2Qm2yFC/XSCwGZo9d58FCFLrNE10RFYLJX7SK52gVWujU7RD8LasGWnokQWBCThW1jYZk5iqsqQVXN+ZDsqBMEB3KsjuWVsifKMmW5OpBCnuz/7Oz/w3ACW/f09uX8/7TbQYAm8S46mqbZNkwQvARQniaLfJ+tw2W0iF7CZYF8/TJqjrS03X57F0GrakhJmn5PwHGPh2qoJcb3uzSLeoekGK3u33Mlh3pc3aXZqhPTc5gk7VzUi7ol6cbekooMunbjd5hl6XNL2YbFpiU0OnzLU7TrFLMI2yGGj2Fnt21djrcBekHqDmz5h+L3G/uDv7HloyIfrXd9tHDUKU+zX7ScerAr9zQeUH/Rexqjffo7baYx2tUPeooM9rCtgNrTWUDtNheQDvsLiActBrR3uoz02m00Mqpur5FbHbQbuVWz4wS3g58=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line("pipelink(R, C) :- grid(R, C).")
        self.add_program_line(fill_path(color="pipelink"))
        self.add_program_line(intersect_loop(color="pipelink"))
        self.add_program_line(adjacent_loop_intersect())
        self.add_program_line(loop_intersect_connected(color="pipelink"))

        for (r, c, _, d), draw in puzzle.line.items():
            fail_false(draw, f"Line must be drawn at ({r}, {c}).")
            for d in "lurd":
                if Point(r, c, label=d) in puzzle.line:
                    self.add_program_line(f'grid_direction({r}, {c}, "{d}").')
                else:
                    self.add_program_line(f'not grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
