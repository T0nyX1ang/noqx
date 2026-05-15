"""The Hashi solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.reachable import grid_color_connected


def hashi_bridge(color: str = "white") -> str:
    """Generate a rule for hashi constraints."""
    rule = "num(1..2)."
    rule += f'direction("{Direction.LEFT}"; "{Direction.RIGHT}"; "{Direction.TOP}"; "{Direction.BOTTOM}").\n'
    rule += f"{{ line_io(R, C, D, N) : direction(D), num(N) }} :- grid(R, C), {color}(R, C).\n"
    rule += ":- N != -1, number(R, C, N), #sum{ N1, D: line_io(R, C, D, N1) } != N.\n"

    rule += "pass_by_route(R, C) :- grid(R, C), #count { D: line_io(R, C, D, _) } = 2.\n"
    rule += f'pass_by_straight(R, C) :- grid(R, C), num(N), line_io(R, C, "{Direction.LEFT}", N), line_io(R, C, "{Direction.RIGHT}", N).\n'
    rule += f'pass_by_straight(R, C) :- grid(R, C), num(N), line_io(R, C, "{Direction.TOP}", N), line_io(R, C, "{Direction.BOTTOM}", N).\n'
    rule += f":- grid(R, C), {color}(R, C), not number(R, C, _), not pass_by_straight(R, C).\n"
    rule += f":- grid(R, C), {color}(R, C), not number(R, C, _), not pass_by_route(R, C).\n"

    # path along the edges should be connected
    rule += f':- grid(R, C), line_io(R, C, "{Direction.LEFT}", _), not line_io(R, C - 1, "{Direction.RIGHT}", _).\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.TOP}", _), not line_io(R - 1, C, "{Direction.BOTTOM}", _).\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.RIGHT}", _), not line_io(R, C + 1, "{Direction.LEFT}", _).\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.BOTTOM}", _), not line_io(R + 1, C, "{Direction.TOP}", _).\n'

    # path along the edges should have the same bridges
    rule += f':- grid(R, C), line_io(R, C, "{Direction.LEFT}", N1), line_io(R, C - 1, "{Direction.RIGHT}", N2), N1 != N2.\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.TOP}", N1), line_io(R - 1, C, "{Direction.BOTTOM}", N2), N1 != N2.\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.RIGHT}", N1), line_io(R, C + 1, "{Direction.LEFT}", N2), N1 != N2.\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.BOTTOM}", N1), line_io(R + 1, C, "{Direction.TOP}", N2), N1 != N2.\n'

    # path inside the cell (not number) should have the same bridges, not sure if this is necessary
    rule += f':- grid(R, C), num(N), not number(R, C, _), line_io(R, C, "{Direction.LEFT}", N), not line_io(R, C, "{Direction.RIGHT}", N).\n'
    rule += f':- grid(R, C), num(N), not number(R, C, _), line_io(R, C, "{Direction.TOP}", N), not line_io(R, C, "{Direction.BOTTOM}", N).'

    return rule


def hashi_adjacent() -> str:
    """Generate a rule to constrain adjacent connectivity."""
    adj = f'adj_line(R0, C0, R, C) :- R = R0, C = C0 + 1, grid(R, C), grid(R0, C0), line_io(R, C, "{Direction.LEFT}", _).\n'
    adj += f'adj_line(R0, C0, R, C) :- R = R0 + 1, C = C0, grid(R, C), grid(R0, C0), line_io(R, C, "{Direction.TOP}", _).\n'
    adj += "adj_line(R0, C0, R, C) :- adj_line(R, C, R0, C0)."
    return adj


class HashiSolver(Solver):
    """The Hashi solver."""

    name = "Hashi"
    category = "route"
    aliases = ["bridges", "hashikake", "hashiwokakero"]
    examples = [
        {
            "data": "m=edit&p=7VZNb9swDL3nVxQ+6yCJkmz51nXtLlm6jw5FYQRBmnlosGTpkmYYHOS/j5IzuOTiomnT7FIYJkg9inqkZUqLn8vhvBTKCq0EZEIKhY+TmcjACQ1pfOXmuRjfTcr8SBwv725mc1SEOD87E9+Gk0XZKTZe/c6q8nl1LKp3eZFAIhId376oPuar6n1e9UT1GaFEKBzroqYSoVE9bdTLiAftpB5UEvVerTtUr1AdjeejSTno1oE+5EV1IZKwzps4O6jJdParTOpp0R7NptfjMHA9vMNkFjfj2w2yWH6dfV9ufFV/Larjmm53C13Y0DW1WtOFF6R7M0Sq25j6/nqNFf+EXAd5EWh/adSsUT/nq3WgtEqMDFOPkJjAABjPaByAxjRo6sZ0FM2IaSVxtjSUNcTMJDWBEclSgnvqrrQiaykNDLfUhhDONLZRFDd8fWVSuoI1zM6o7RSP4GjGymXcI/V8JGN5ecpCS4prRfPWiuapFV9Bx0rdiwCG2SmfYWjttWUcrOUzLGMda3OPVco4pMzf86+hvSUeIB3zAEVZguIxQDkaQ0tmUxYAlDXAPxGBblIwodqqsVmlwNKvBRmtPWSMged7Cjz7IVkORrP/VxuSg9GO2XQXG5AUB81wQxhhG1GxmVxFeRaljvICe42oIMq3UcoobZTd6HMa5WWUJ1GaKF30SUO32qmfPYcO9kIRugJglkqEPhg0J0IfAIlqKkK/A/lI3oWpD9C2x76ir+j+0X6nSLrjH+VRbzafDid4Tegtp9fl/K+NV7J1J/mdxBc7BW7111va4W9pofryYL1tP622wMJueqOozkVyuxwMB6MZ7jGsXQ3GFrodVCYzuyIPBnwO+GASLwQektCj4Xi+tYWOJ97+vqYyzh0C8aneEXji+nZXxHu1I4DVbMvSw45AeyxEWnNpQ7xvq/L/A06fACipttZ+v8ihyiJbPqOUfh9T9njbru/Y1fljzya8Ufc7fwA=",
        },
        {
            "url": "https://puzz.link/p?hashi/19/14/2g2g3g3g2i2g3g2q2g2g1h3g2g3h2v2i3g2h1g2h1g2g3p2g23g2g2g2j2g2i2h2g3g3g33zh2h3g1h2g32h1g2g2h2j4g3h1h2l2g1j23g2h4g2g1h2h3g2o1g2h2p2g2i2k1g2g3g4j3h22g3h2",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="number", size=3))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(hashi_bridge(color="white"))
        self.add_program_line(hashi_adjacent())
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"white({r}, {c}).")
            self.add_program_line(f"number({r}, {c}, {num if isinstance(num, int) else -1}).")

        for (r, c, d, label), draw in puzzle.line.items():
            if label == "double" and draw:
                self.add_program_line(f':- not line_io({r}, {c}, "{d}", 2).')

            if label == "normal" and draw:
                self.add_program_line(f':- not line_io({r}, {c}, "{d}", 1).')

        self.add_program_line(display(item="line_io", size=4))

        return self.program
