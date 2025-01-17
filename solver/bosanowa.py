"""Solve Bosanowa puzzles."""

from typing import List

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_num, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.solution import solver


def bosanowa_constraint(adj_type: int = 4) -> str:
    """Generate bosanowa constraints."""
    return f":- number(R, C, N), N != #sum {{ |N - N1|, R1, C1: number(R1, C1, N1), adj_{adj_type}(R, C, R1, C1) }}."


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)

    lmt_num = int(puzzle.param["max_number"])
    solver.add_program_line(defined(item="hole"))
    solver.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
    solver.add_program_line(fill_num(_range=range(1, lmt_num + 1)))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(bosanowa_constraint())

    for (r, c, _, _), color in puzzle.surface.items():
        fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
        solver.add_program_line(f"hole({r}, {c}).")

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be an integer.")
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Bosanowa",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VXBbptAEL37K6I5zwHYhQVubhr34jpt7SqKVsjCLlGs2iLFpqrW8r9ndgYFLCVqL0l7qBAzj8eb5e3ueL3/0ZZNhSkaVCkGGNKldIQq0KiTkO+guxabw7bKL3DcHu7rhgDi9WSCd+V2X41spypGR5flbozuQ24hBISI7hAKdJ/zo/uYuxm6Ob0C1MRNRRQRvOrhDb/36FLIMCA86zDBW4LrTbPeVsupMJ9y6xYI/jvvuNpD2NU/K+h8+Od1vVttPLEqDzSZ/f3moXuzb7/V39tOGxYndOOX7arerodi16Nn7PpZvLLdrDidaNm/kOFlbr33rz1MezjPjxAlkGvaFCMplZRxUoGkSJKSJBIlEi0SrSXFnGIhYyFj+UIsX0ikPJFyIxIjdUYkaShJ6jJ5yqQuk7owEE9h4E3RVGY0FUVKC4oWVBoMNIks6AFBagtJT8RcQh35RHDJgEjI2tkYCdk6G8MwMSgx5NGC6YmU1uNsjJQmc1aScsmAyNjpYC5hwFZ9Mz0xtHgDDa1CmB8p3nKccIw4Lmi/0SmO7zkGHGOOU9ZccbzheMlRc0xYY3zH/GFPyXa8gR0bJXxA9Vf8us/FyMK8be7KdUW/u1m7W1XNxaxuduUW6KA7jeAX8G0VyfX/s+8vnX1+C4J/rVt/Y8e6ORqD7hrhoV2Wy3W9Bfr7xBf4N3dPP7di9Ag=",
            "config": {"max_number": 10},
        },
        {
            "data": "m=edit&p=7VRNb9swDL3nVxQ66yBKsiP7lnXNLln2kQ5FYRhFkrlosATZnHgYFOS/lyIZOCt22GVbDoNh8ol8Ep8o2btv3bxtdNBgtAvaaMDHeas9BG19Rq+R53a1XzfllR51+6dti0Drd+Oxfpyvd82gElY9OMSijCMd35SVAqWVxRdUreOH8hDflnGq4wxTSnuMTZhkEd708I7yCV1zEAziqWCE9wiXq3a5bh4mHHlfVvFWq1TnFc1OUG223xslOtJ4ud0sVimwmO9xM7un1VfJ7LrP2y+dcKE+6jh6ITdVEbmul5sgy03oF3LTLv6w3KI+HrHtH1HwQ1kl7Z96GHo4Kw/K5qr0eChDdoFdQc4ZdpadY8cUx5SMKRmwy9jxmjkzh56djHhe4HmB5wXOFTwquF7B9cAwFcxpzOuB4WIATAeQPEgeTnlWA8BbBCs8KzwrPOkESCtAegHSDHDCc8JzwpOGgHQEvOj1aTfY5Sl2OcXwaAweNl9+lbIYcX0kR10Yyc8iqPAFB2v/vE6OVSt1Rgkoq1KhD4ChUmfrguOFTxEUCeUB7T3ZMVlL9hZvio6O7GuyhmxGdkKcG7J3ZK/JerI5cYbprv3mbeRu/QU5lc3p19Y/2WWN60GlZl37OF82+IVPu82iaa+m23YzXyv8pR4H6oeit3JI9///sv/oL5uOwFza7b40Ofi91YNn",
            "config": {"max_number": 25},
            "test": False,  # very slow
        },
    ],
    "parameters": {"max_number": {"name": "Max number", "type": "number", "default": 10}},
}
