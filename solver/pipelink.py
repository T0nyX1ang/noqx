"""The Pipe Link solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import display, fill_line, grid
from noqx.rule.helper import fail_false
from noqx.rule.neighbor import adjacent
from noqx.rule.route import crossing_route_connected, single_route


class PipeLinkSolver(Solver):
    """The Pipe Link solver."""

    name = "Pipe Link"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7Zbfb6M4EMff81dUfl1La4OxAWkf0iZdqUpzzW16vRZVEU1IQ0vCLpC2our/vuMfiB+hq3u5U09aESaffG2PZwZrSP5jH2YRpkR+bBfDN1yMuuq2XK5uYq55XCSRf4SH+2KTZgAY/3F6itdhkkf47PrhePQ4fB4P//7s3Nj25XT96WE0u3xYXf1FZyT+nJFp4u7OL0bHyaev5c35ZvgUjSN+kafLTRKFq7C8uTp7SXan7v1mTU/ONifuOtyR/Ic7956OZ1++DAITyO3gtfT8cojLr36ALITVTdEtLmf+a3nulxNcfoMhhCloEyAHYQtwDEg1XqlxSSdapAR4ahjwGnAZZ8skWky0cuEH5Rwjuc+xWi0RbdOnCOll6vcy3d7FUrgLC6hXvom/m5F8v0of92YuOETbfVLEyzRJMylK7Q2Xw/dTsOsUJOoUJPWkIDP7l1Pw+lN4g8fzJySx8AOZz2WNbo3f/FewU2WpstfKniprKTuHqbi0lR0pS5R1lJ34r8h2MLds5FtYIrOEQua1kNEKuc1rNBM4oPagkCl0KKBXIWN6AueAegIgd4xqYc70XIkOUSgY5tyqkHG9sSswF9qDQqdCxmsU2hklBNit2dPuqOVhQbU/zToTyQ5psKXzpoxhYTfZ+AF2rAab4lBOsGDGD7BjmxigPk0WplaUCtjXxAwsiE6FEsjbMz6BuYnfg4JyPR2Qm2yFC/XSCwGZo9d58FCFLrNE10RFYLJX7SK52gVWujU7RD8LasGWnokQWBCThW1jYZk5iqsqQVXN+ZDsqBMEB3KsjuWVsifKMmW5OpBCnuz/7Oz/w3ACW/f09uX8/7TbQYAm8S46mqbZNkwQvARQniaLfJ+tw2W0iF7CZYF8/TJqjrS03X57F0GrakhJmn5PwHGPh2qoJcb3uzSLeoekGK3u33Mlh3pc3aXZqhPTc5gk7VzUi7ol6cbekooMunbjd5hl6XNL2YbFpiU0OnzLU7TrFLMI2yGGj2Fnt21djrcBekHqDmz5h+L3G/uDv7HloyIfrXd9tHDUKU+zX7ScerAr9zQeUH/Rexqjffo7baYx2tUPeooM9rCtgNrTWUDtNheQDvsLiActBrR3uoz02m00Mqpur5FbHbQbuVWz4wS3g58=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(single_route(color="grid", crossing=True))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(crossing_route_connected(color="grid"))

        for (r, c, d, _), draw in puzzle.line.items():
            fail_false(draw, f"Line must be drawn at ({r}, {c}).")
            for d in (Direction.TOP, Direction.LEFT, Direction.BOTTOM, Direction.RIGHT):
                if Point(r, c, d) in puzzle.line:
                    self.add_program_line(f'line_io({r}, {c}, "{d}").')
                else:
                    self.add_program_line(f'not line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
