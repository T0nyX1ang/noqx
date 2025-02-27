"""The Number Rope solver."""

from noqx.puzzle import Color, Point, Puzzle
from noqx.rule.common import defined, display, fill_num, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_num_adjacent
from noqx.solution import solver


def numrope_constraint() -> str:
    """
    Generate a constraint for the number rope.

    An adj_loop rule should be defined first.
    """
    rule = "adj_count(R, C, N) :- grid(R, C), N = #count { R1, C1 : adj_loop(R, C, R1, C1) }.\n"
    rule += ":- adj_count(R, C, N), N > 2.\n"
    rule += ":- adj_count(R, C, 1), number(R, C, N), number(R1, C1, N1), adj_loop(R, C, R1, C1), |N - N1| != 1.\n"
    rule += (
        ":- adj_count(R, C, 2), number(R, C, N), N * 2 != #sum { N1, R1, C1 : number(R1, C1, N1), adj_loop(R, C, R1, C1) }.\n"
    )
    return rule.strip()


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(defined(item="hole"))
    solver.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
    solver.add_program_line(fill_num(_range=range(1, 10)))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(avoid_num_adjacent(adj_type=4))
    solver.add_program_line(numrope_constraint())

    for (r, c, _, d), draw in puzzle.line.items():
        fail_false(draw, f"Line must be drawn at ({r}, {c}).")
        solver.add_program_line(f'grid_direction({r}, {c}, "{d}").')

    for (r, c, _, _), color in puzzle.surface.items():
        fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
        solver.add_program_line(f"hole({r}, {c}).")

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")

        if Point(r, c) in puzzle.surface:
            solver.add_program_line(f":- #sum {{ N, R, C: number(R, C, N), |{r} - R| + |{c} - C| = 1 }} != {num}.")
        else:
            solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display(item="number", size=3))

    return solver.program


__metadata__ = {
    "name": "Number Rope",
    "category": "num",
    "aliases": ["numberrope"],
    "examples": [
        {
            "data": "m=edit&p=7ZRNb9NAEIbv+RXVnudgr3dtr2+hNFxC+GhRVVlW5ARXjUhwSWIEjvLf+86OkxgJQRFQLsjx7LOT2dnXsx+bT025rijBE6UUUIgnCox/44B/h+dqsV1W2RkNm+1dvQYQvRqN6LZcbqpB3kUVg13rsnZI7YssV6EipfGGqqD2TbZrX2btmNpL/KXIwDeWIAu8ENTAa/8/07k4wwA8EeZhN8DFxwrSl4vtVwl9neXtFSme6Zkfz6hW9edKdUq4P69XswU7ZuUWn7O5W9x3/2ya9/WHposNiz21QxE8+bHg6CiY6TuCWdxfF+yK/R6lfwvJ0yxn9e9OmJ7wMtspbVRmSEWJNM43RnpWmjiQJvJNIk0aSiM9F6NBxkmXETIMaiSL7ZPnSgc9D+b5NobngofXtPPwfLlKTw6eEml6ITw7BvViWEhvECSF2Q72xtuRt9rbK9SA2sjb594G3lpvx/iQyJJBOgu5liIh3SctZFIy+B6OO5LmE3Qg3ZEjg1LyiIAMPoZHHCkOKdaebJ+sUJxSLJltn6xQ4shJZlAqlAbkJLPT5FAo9h0pCSmVzKBEyBlyVuL6lAolHaF0F76A196ee2u8jX3pEt5cj9x+hy2DxH7V9G+v2iPl5dr42+3w2D/fKwa5umzWt+W8wiEd48SfTer1qlyiN2lWs2p96OOe3A/UF+XfPMJg8//q/IdXJy9D8Es7+Al27E/k5KgvrqTeKSJ130zL6bzGhguKJ5eLM1YMHgA=",
        },
    ],
}
