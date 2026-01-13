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
            "data": "m=edit&p=7VZdb9s2FH33rwj4tKEcJlKS9QHswUmdrm2iOm2CLDaMQHYUW6lkdbKUdAry33suRdmW7XQbhg15GARRh+dekfceklda/l6GecRdXKbLDS5wmZZUtzQ8dRv6Oo+LJPIPeK8s5lkOwPmHgN+GyTLi767mJ0dZ7+F177d7txgOxRujfGtc3h3fvfqYvn8bm7k4DtzB6eA0lrPer0eHZ93+q+6gXF4U0f1ZKg7vLobnt4PLmSf/6AdDqxp+MOx3w9uf73sXv3RGOoRx57Hy/KrHqzf+iAnGmcQt2JhXZ/5jdepXfV59golxMeYsLZMinmZJlrOGq07qFyVgfw0vlZ3QUU0KAzjQGPAKcBrn0yS6PqmZgT+qzjmjuQ/V2wRZmt1HNBnFRv1plk5iIiZhAfWW8/gL4yYMy/Im+1xqVzF+4lWvziD4ixlgkCYDgnUGhPZkQIn9uxl446cnLM5H5HDtjyidizV01/CT/4g28B+ZaeJV2m5q/ZjpUVeu+jaZzVXXsdtmx22ZhWGRfYMQAoSl+5hSqImvVHusWqnac8TFK1O1r1VrqNZW7Yny6SNcYbtcOAbzJUa0PWBMQLiLHBwEqzACdBCJwgiGoibs4GC5UmP4uNrHQYBuV+MuMLIi7MLH0z4ufDzt48LHa3wcYIhG2OvioGrec+jQKiwN8KLmpTC4lHUMUgjgOmYpcMjNOhcp4WNqHwkfWiOFUQzMOh5pwsfSPiZ4q+Et4DpOaWJeS89LhcTWPhZ8bO1jwcdufBCzrXMhrRptHdKw0coGbnSA5o2eLnwaPUkrV2tOWrmO1oQ01LyHcRo9oRv0Wum20tajwlevNZ7AWh/S06j98VxpjueG5nhX6HdJc9qICsN/tRbwF9pfmlgLrY+EPrKOE2uyXgvSuVkLC3yjP2lrNTzGV5pjw16qbXukWku1XbWdHTqEf+uY/vOT86fhjCRWoXVhhf7L/rgzYv2bWXQQZHkaJqh7QZlOorzp46vDlllyvSzz23AaXUdfw2nB/PrDt2lpcQs1RotKsuxLEi/2jdCYWmQ8W2R5tNdEZISYnxmKTHuGmmT5zVZMD2GStHNRfwQtqv5stKgixzdhox/mefbQYtKwmLeIje9Ha6RosSVmEbZDDD+HW7OlazmeOuwrUzc+Byib//8ivOhfBFoo46VVoJcWjtrjWf6dgrM2btN7yg7Y71SeDes+/pkis2Hd5ncqCgW7W1TA7qkrYLdLC6jd6gJyp8CAe6bG0KjbZYai2q40NNVOsaGpNuvNiOXRYhIuDn6onz+l4U02K6fz+Ec27nwD",
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
