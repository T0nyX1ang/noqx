"""The Renban-Madoguchi solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type


def consecutive_in_room(_id: int, size: int) -> str:
    """Generate a rule to ensure the numbers in each room are consecutive."""
    return f":- area({_id}, R0, C0), area({_id}, R1, C1), number(R0, C0, N0), number(R1, C1, N1), |N0 - N1| >= {size}.\n"


def calc_edge_length(r: int, c: int, d: str, puzzle: Puzzle) -> int:
    """Calculate the edge length based on the direction."""
    length = -1
    if r > 0 and d == Direction.TOP:
        lc = c
        while lc >= 0 and puzzle.edge.get(Point(r, lc, Direction.TOP)) is True:
            lc -= 1
            length += 1

        rc = c
        while rc < puzzle.col and puzzle.edge.get(Point(r, rc, Direction.TOP)) is True:
            rc += 1
            length += 1

    if c > 0 and d == Direction.LEFT:
        tr = r
        while tr >= 0 and puzzle.edge.get(Point(tr, c, Direction.LEFT)) is True:
            tr -= 1
            length += 1

        br = r
        while br < puzzle.row and puzzle.edge.get(Point(br, c, Direction.LEFT)) is True:
            br += 1
            length += 1

    return length


class RenbanMadoguchiSolver(Solver):
    """The Renban-Madoguchi solver."""

    name = "Renban-Madoguchi"
    category = "num"
    aliases = ["renbanmadoguchi", "renban-madoguchi"]
    examples = [
        {
            "data": "m=edit&p=7VVNbxMxEL3nV1Q+++CP9dreWymBSwgfTYWqKKrSdKERiRbygdBG+e+88c7GrYQECIF6QNZOnsfP8cyzx95+2c83tQxoNkglNZotTPqMiulT3CbL3aquzuT5fnffbACkfD2WH+arbS0HU2bNBoc2Vu25bF9WU6GFFAafFjPZvq0O7auqHcr2EkNC6pkU6/1qt1w0q2Yjel876iYawGGG79M4oYvOqRXwmDHgNeBiuVms6ptR53lTTduJFLT2szSboFg3X2vBsVF/0axvl+S4ne+Q4PZ++VlIi4Ht/q75tBf9CkfZnncZjH8xA5szsKcM7I8zMH89gzg7HrE575DDTTWldK4yDBleVocjhXUQ1mIqnYi0f8JG6ppT39GwPXW9ezzsw6NhrQoaf+DQGo6C+1hSp4Wvk32RrEl2grhka5N9nqxK1iU7SpwhwtUuSO2VqAz+0UVg3eESOXjLGAH6gjGCoagJe5z9YBiDE5jjEWAoGZfAocMBnMicAE5kTgAn9hwPHDscS9QS+6OnukrYKPh15zdaSWMMYw1sGaMObZeLMeBY5hhwLHMM6tV28RgLTsEcC3/R+wvgkjHWLXhdqnXHnAIcx5wCHNdzELOLWateW2+znt4B9zrorGewWU/SKrisVfCsCWnI/uiynpH09CfdTtpGupsUa4h8lc56Ks/YnzTH7wPNMVerrLnmudo/2AvwNfONxV6wPgb6GMca6rwXpHO/F4XO+pO2hc0aJs2PdBnQsb1Itki2TMfZUxH+Vpn+eeX8NJypKdPLkJv7t/3ZYCqGdx/rs3GzWc9XuPfG+/Vtven7eHWOA/FNpA+XjqEp/x+iJ/wQ0Uapp3bOn1o4qLzZ4Ds=",
        },
        {"url": "https://puzz.link/p?renban/6/6/6a6cqqo6uqo1h4n7q1i5g81k", "test": False},
    ]
    parameters = {"max_number": {"name": "Max number", "type": "number", "default": 20}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        lmt_num = int(puzzle.param["max_number"])
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_num(_range=range(1, lmt_num + 1)))
        self.add_program_line(unique_num(color="grid", _type="area"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(consecutive_in_room(_id=i, size=len(ar)))

        for (r, c, d, _), draw in puzzle.edge.items():
            if d == Direction.TOP and r > 0 and draw:
                self.add_program_line(
                    f":- number({r}, {c}, N), number({r - 1}, {c}, M), |N - M| != {calc_edge_length(r, c, d, puzzle)}."
                )

            if d == Direction.LEFT and c > 0 and draw:
                self.add_program_line(
                    f":- number({r}, {c}, N), number({r}, {c - 1}, M), |N - M| != {calc_edge_length(r, c, d, puzzle)}."
                )

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
