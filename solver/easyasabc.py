"""The Easy As ABC solver."""

from noqx.manager import Solver
from noqx.puzzle import Point, Puzzle
from noqx.rule.common import count, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, validate_direction, validate_type


class EasyAsABCSolver(Solver):
    """The Easy As ABC solver."""

    name = "Easy As ABC"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7ZTBTttAEIbvfgq05zl4do299i0FwiUN0AQhZFmRk7oiqiNTJ0ZoI797ZyemhjUS6qHAoXJ29OfbHfv3znq2v5q8LgDR/pQGH0hBcBzyQJQ8/O6ar3dlkRzBqNndVTUJgIvxGH7k5bbwUuRczLy9iRMzAnOepAIFCEkDRQbmKtmbr4mZgpnRlICA2OSwSJI86+UNz1t1coDok552muQtydW6XpXFYnIgl0lq5iDsc75wtpViUz0UovNh/6+qzXJtwTLf0cts79b33cy2+V79bMTTI1owI8eu7O2q3q76Y1e9blf+e7tx1ra07d/I8CJJrffrXupezpJ9a33thQps6oi8HGojVGjB9TMQuUBbMOtB4FswfwbQBZELtAMid4WOHGOxtOC8B+i7OYiuV5SDLOXeGINBVjggOhiQ0NkGHFhGrQckdv3EvnvnGF9kUaWQ63XLccxRcpxTOcEojqccfY7HHCe85ozjDccTjgHHkNdE9kD81ZF5BztpoAGdK/pcJPNSMW02y6I+mlb1Ji8F9bvWE4+CR6ps+/zfAj+oBdoS+J/tVL9hJ6XdpXPPDU12reC+WeSLVVUKoE3sFpiLl/zdX4O+z8z7DQ==",
            "config": {"letters": "AUGST"},
        },
    ]
    parameters = {"letters": {"name": "Letters", "type": "text", "default": "ABC"}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")
        n = puzzle.row
        letters: str = puzzle.param["letters"]
        rev_letters = {v: k + 1 for k, v in enumerate(letters)}
        self.add_program_line(grid(n, n))
        self.add_program_line(fill_num(_range=range(1, len(letters) + 1), color="white"))
        self.add_program_line(unique_num(_type="row", color="grid"))
        self.add_program_line(count(n - len(letters), _type="row", color="white"))
        self.add_program_line(unique_num(_type="col", color="grid"))
        self.add_program_line(count(n - len(letters), _type="col", color="white"))

        for (r, c, d, label), letter in puzzle.text.items():
            letter = str(letter)
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(len(letter) == 1, f"Clue at ({r}, {c}) should be a letter.")

            if r == -1 and 0 <= c < puzzle.col:
                self.add_program_line(
                    f":- Rm = #min {{ R: grid(R, {c}), not white(R, {c}) }}, not number(Rm, {c}, {rev_letters[letter]})."
                )

            if r == puzzle.row and 0 <= c < puzzle.col:
                self.add_program_line(
                    f":- Rm = #max {{ R: grid(R, {c}), not white(R, {c}) }}, not number(Rm, {c}, {rev_letters[letter]})."
                )

            if c == -1 and 0 <= r < puzzle.row:
                self.add_program_line(
                    f":- Cm = #min {{ C: grid({r}, C), not white({r}, C) }}, not number({r}, Cm, {rev_letters[letter]})."
                )

            if c == puzzle.col and 0 <= r < puzzle.row:
                self.add_program_line(
                    f":- Cm = #max {{ C: grid({r}, C), not white({r}, C) }}, not number({r}, Cm, {rev_letters[letter]})."
                )

            if 0 <= r < puzzle.row and 0 <= c < puzzle.col:
                self.add_program_line(f"number({r}, {c}, {rev_letters[letter]}).")

        self.add_program_line(display(item="number", size=3))

        return self.program

    def refine(self, solution: Puzzle) -> None:
        """Refine the solution."""
        letters: str = solution.param["letters"]
        for (r, c, d, label), letter in solution.text.items():
            solution.text[Point(r, c, d, label)] = letters[int(letter) - 1]
