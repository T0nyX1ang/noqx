"""The Pipe Link solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.route import crossing_route_connected, route_crossing, single_route


def straight_at_ice(color: str = "white") -> str:
    """A rule to make a route go straight at ice cells."""
    rule = ""
    for d1, d2 in ((Direction.TOP, Direction.BOTTOM), (Direction.LEFT, Direction.RIGHT)):
        rule += f':- ice(R, C), {color}(R, C), line_io(R, C, "{d1}"), not line_io(R, C, "{d2}").\n'
        rule += f':- ice(R, C), {color}(R, C), line_io(R, C, "{d2}"), not line_io(R, C, "{d1}").\n'

    return rule


class PipeLinkSolver(Solver):
    """The Pipe Link solver."""

    name = "Pipe Link"
    category = "route"
    aliases = ["pipelinkr", "pipelinkreturns"]
    examples = [
        {
            "data": "m=edit&p=7Zbfb6M4EMff81dUfl1La4OxAWkf0iZdqUpzzW16vRZVEU1IQ0vCLpC2our/vuMfiB+hq3u5U09aESaffG2PZwZrSP5jH2YRpkR+bBfDN1yMuuq2XK5uYq55XCSRf4SH+2KTZgAY/3F6itdhkkf47PrhePQ4fB4P//7s3Nj25XT96WE0u3xYXf1FZyT+nJFp4u7OL0bHyaev5c35ZvgUjSN+kafLTRKFq7C8uTp7SXan7v1mTU/ONifuOtyR/Ic7956OZ1++DAITyO3gtfT8cojLr36ALITVTdEtLmf+a3nulxNcfoMhhCloEyAHYQtwDEg1XqlxSSdapAR4ahjwGnAZZ8skWky0cuEH5Rwjuc+xWi0RbdOnCOll6vcy3d7FUrgLC6hXvom/m5F8v0of92YuOETbfVLEyzRJMylK7Q2Xw/dTsOsUJOoUJPWkIDP7l1Pw+lN4g8fzJySx8AOZz2WNbo3f/FewU2WpstfKniprKTuHqbi0lR0pS5R1lJ34r8h2MLds5FtYIrOEQua1kNEKuc1rNBM4oPagkCl0KKBXIWN6AueAegIgd4xqYc70XIkOUSgY5tyqkHG9sSswF9qDQqdCxmsU2hklBNit2dPuqOVhQbU/zToTyQ5psKXzpoxhYTfZ+AF2rAab4lBOsGDGD7BjmxigPk0WplaUCtjXxAwsiE6FEsjbMz6BuYnfg4JyPR2Qm2yFC/XSCwGZo9d58FCFLrNE10RFYLJX7SK52gVWujU7RD8LasGWnokQWBCThW1jYZk5iqsqQVXN+ZDsqBMEB3KsjuWVsifKMmW5OpBCnuz/7Oz/w3ACW/f09uX8/7TbQYAm8S46mqbZNkwQvARQniaLfJ+tw2W0iF7CZYF8/TJqjrS03X57F0GrakhJmn5PwHGPh2qoJcb3uzSLeoekGK3u33Mlh3pc3aXZqhPTc5gk7VzUi7ol6cbekooMunbjd5hl6XNL2YbFpiU0OnzLU7TrFLMI2yGGj2Fnt21djrcBekHqDmz5h+L3G/uDv7HloyIfrXd9tHDUKU+zX7ScerAr9zQeUH/Rexqjffo7baYx2tUPeooM9rCtgNrTWUDtNheQDvsLiActBrR3uoz02m00Mqpur5FbHbQbuVWz4wS3g58=",
        },
        {
            "data": "m=edit&p=7Zbfb6NGEMff/Vec9vVWKgvL8kPqg5OLr3d1fE7iyI1RFBGHxOQgpBicK1b+95vZhRrw+tRWqpRKlc364+8OszOz68Hr38swjygz8G25FD7hxZkrL9MV8jLq1ywuksh/R4dlscpyAEq/jEb0PkzWEf18tRofZ8OXD8PfNm6xWLCPRvnJmD+OHt+fp79+iq2cjSbu9HR6GpsPw1+Oj87EyXsxLdeXRbQ5S9nR4+Vidj+dP3jmHyeTBa8WXwz78+L+p83w8udBUMdwPdhWnl8NafXRD4hJqLwYuabVmb+tTv1qTKsLmCKUgTYGsgk1AU8AmcK5nEc6ViIzgCc1A14BLuN8mUQ3Y6VM/aCaUYLrHMm7EUmabSKibpPfl1l6G6NwGxZQqvUqfq5n1uVd9rWsbcEhScukiJdZkuUoovZKq+HhFKxdCogqBSRNCpjZv5yCp0/hFbbnHJK48QPM53KH7g4v/C2MEzkyOV75W+Jw8MIggHbQxLG1qqtVPZ3qOjrVY1pVGwMztMbMOGCtDY4xoZe14THT0MuaSKB+I1lFU44zKDKtLDl+kKMhR1uOY6g0t6mwLOKbFJFbEAGiAypk1CAUHlAwKjgkpJDb6jbHAoRQFAqhkBkmFS5sQsMeJIFsMeow5URxbQNsGy02lXfGLeDaJ7BjNSyAGxtkFS7jLrCKF9k2odTSJ9g0PiXX9oYHsdU2wDbur2TIG4/An1z7BOZui70mRwE2tX/Jzb0C7Fvsqdw9k3JHlQSxtnCxrMohoqP82VA+S6mAnCtbG3bDUs4k1gZwm7lDrjwI2COuEgMUNi4Mx+NEHpK5HI/lyOUo5PFw8Bf6j3/Df/ck/sVwAks9lrov+7+nXQ8CMo6foneTLE/DBPrqxSp8jgg81Mg6S27WZX4fLqOb6Fu4LIivnqvtmY72VKa3EbTelpRk2XMCC2g8NFMdMX54yvJIO4VidPdwyBVOaVzdZvldL6aXMEm6ucj/HB1JtbOOVOTwFGp9D/M8e+koaVisOkLridXxFD31ilmE3RDDr2FvtXRXjtcB+UbkFVjUxE38/x/Im/4HgltlvLUe9tbCkac8y3/QcnaTfVnTeED9Qe9pzer0A22mNdvX93oKBrvfVkDVdBZQ+80FpP3+AuJeiwHtQJdBr/1Gg1H1ew0utdducKl2xwmuB98B",
            "config": {"pipelinkr": True},
        },
    ]
    parameters = {
        "pipelinkr": {"name": "Pipelink Returns", "type": "checkbox", "default": False},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="grid", crossing=True))
        self.add_program_line(crossing_route_connected(color="grid"))

        if puzzle.param["pipelinkr"]:
            for (r, c, d, label), symbol_name in puzzle.symbol.items():
                validate_direction(r, c, d)
                validate_type(label, "normal")
                validate_type(symbol_name, "circle_L__1")
                self.add_program_line(f"ice({r}, {c}).")

            self.add_program_line(shade_c(color="crossing", _from="ice"))
            self.add_program_line(straight_at_ice(color="grid"))
        else:
            self.add_program_line(route_crossing(color="grid"))

        crossing_points = set()
        for (r, c, d, _), draw in puzzle.line.items():
            fail_false(draw, f"Line must be drawn at ({r}, {c}).")

            cnt = 0
            for d in (Direction.TOP, Direction.LEFT, Direction.BOTTOM, Direction.RIGHT):
                if Point(r, c, d) in puzzle.line:
                    self.add_program_line(f'line_io({r}, {c}, "{d}").')
                    cnt += 1
                else:
                    self.add_program_line(f'not line_io({r}, {c}, "{d}").')

            if cnt == 4 and (r, c) not in crossing_points and puzzle.param["pipelinkr"]:
                self.add_program_line(f"crossing({r}, {c}).")
                crossing_points.add((r, c))

        self.add_program_line(display(item="line_io", size=3))

        return self.program
