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
            "data": "m=edit&p=7Vbdb9pADH/nr0B52qSTdl/5uLx1XbsXRre1U1VFCAHNVlRYOijbFMT/Xtuhyt2NVKWl7KWKYtn52b6fnYtz81+LwSxnImRSMJUwzgRcEU9YoiImVUw3X19n49tJnrbZweL2qpiBwtjJ8TH7PpjM81a29uq1lqVJywNWfkyzQAUskHT3WPklXZaf0rLLylOAAibgWQc0ETAJ6lGtnhOO2mH1UHDQu5UegXoB6mg8G03yfqdK9DnNyjMW4DrvKRrVYFr8zoMqjOxRMR2O8cFwcAvFzK/GN2tkvrgsrhdrX9FbsfKgotvZQFet6epKreii9lJ0rwZAdRNT01utoONfgWs/zZD2t1pNavU0XYLspstAcwxtAzEGCSCflvBA1aYGU9Zm5KKJY4aYrHYO3VQhpqrNBJ0tU3lEktjBjesupHDWEhLjbTx0bYXpdG1rjLdw7a8vNEZYKxB/28biLTvCjE6GyK1YRBjheMTGf5J4dRmXheQuLoVbtxRunVL4K0jqlJVBuXXBN+5H0Cax1gg9DiH22okIPdbUG4tV7HGIPX/jvw1pcI3aQ3HcibaHEi5LRZ1xPTDGyiHd/aqky0Ipl7VS/2SkXllrauw2zMx72+uUCt23pRK394o2vWUbf08p432QXg1aet+vRP+6Bi2xB7bt7mKtMJ+FK8xn45ivZgRjRNAwuSB5TFKSPINZw0pF8gNJTjIk2SGfI5LnJA9JapIR+cQ4rbaaZ8+hA7OQ4VRQUKVgOAdRixjOAcVBjRnOO8UfyTuDfPgDbbrCV/QV3T3aa2VBZ/wzb3eL2XQwgWNCdzEd5rN7G45kq1bwN6AbJgVs9ddT2v5Padh9vrfZtptRm0Fj17ORlScsuFn0B/1RAXsMeleBNEI3g0InelvkwYTPAR8s4oXAfRJ6NEz/t6bU9Mfb3dsUOor2gZhYbgk8cf1wW8QYsSUA3Wyq0qgtgeZcgDTW0oQY09Tl/wccPQEQXGzs/W6RfbWFN7xGzs0uQnZ42q7O2OXJY/9NcKKu/ql/iuvBdT4r2m/IfDecjS9/5PO3Qa91Bw==",
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
