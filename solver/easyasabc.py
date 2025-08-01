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
            "data": "m=edit&p=7VTBbtpAEL37K6I9z8FjO2DvjaYhF+q0hSiKLAsZ6iqoRk4NrqpF/HtmZq16MZGqHprmUC379Hg7s7ydXWb3vS2aEhD5E8bgAzGILkcyEQOZfjcWm31V6guYtPvHuiECcDudwtei2pVexpk0cu9gEm0mYG50plCBCmiiysF80gfzQZsUzJyWFESkzWxQQPS6p/eyzuzKiugTTztO9IHoetOsq3I5s8pHnZkFKP6dd5LNVG3rH6XqfPD3db1dbVhYFXs6zO5x89St7Nov9be2i8X8CGYysMt2Orthb5eptcvsBbuc9pftJvnxSGX/TIaXOmPvdz2NezrXB8JUH1QYceqEvNi7UeGIhTtHGA+FmIV5L0Q+CwtHwKEge7iC7OEI42FELIJjLAlYuOkF9Ic5iEOvGJxl2fM4G6N152aNzpRY6nSiSKGcMuCZZYzlmCdKMvSTSPXcnRMp368suimU+3oQnAoGggu6TjCh4HtBX/BScCYx14L3gleCkeBIYsb8IP7oybyCnSyKbQ9xxvhtKbmXqbTdrsrmIq2bbVEp6ndHT/1UMrOQ2+f/FviPWiBfgf/WXvVv7GRUXXr30tCCrhU8tctiua4rBVTELsDcnuqvfgz6f+beMw==",
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
