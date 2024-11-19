"""The Yin-Yang solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def exclude_checkboard_shape() -> str:
    """Exclude checkboard shape."""
    rule = ":- circle_M__1(R, C), circle_M__2(R, C + 1), circle_M__2(R + 1, C), circle_M__1(R + 1, C + 1).\n"
    rule += ":- circle_M__2(R, C), circle_M__1(R, C + 1), circle_M__1(R + 1, C), circle_M__2(R + 1, C + 1)."
    return rule


def exclude_border_color_changes(rows: int, cols: int) -> str:
    """Exclude border color changes more than twice."""
    rule = ""
    for r in range(rows - 1):
        rev_r = rows - 1 - r
        rule += f"changed({r}, 0) :- circle_M__1({r}, 0), circle_M__2({r + 1}, 0).\n"
        rule += f"changed({r}, 0) :- circle_M__2({r}, 0), circle_M__1({r + 1}, 0).\n"
        rule += f"changed({rev_r}, {cols - 1}) :- circle_M__1({rev_r}, {cols - 1}), circle_M__2({rev_r - 1}, {cols - 1}).\n"
        rule += f"changed({rev_r}, {cols - 1}) :- circle_M__2({rev_r}, {cols - 1}), circle_M__1({rev_r - 1}, {cols - 1}).\n"

    for c in range(cols - 1):
        rev_c = cols - 1 - c
        rule += f"changed(0, {c}) :- circle_M__1(0, {c}), circle_M__2(0, {c + 1}).\n"
        rule += f"changed(0, {c}) :- circle_M__2(0, {c}), circle_M__1(0, {c + 1}).\n"
        rule += f"changed({rows - 1}, {rev_c}) :- circle_M__1({rows - 1}, {rev_c}), circle_M__2({rows - 1}, {rev_c - 1}).\n"
        rule += f"changed({rows - 1}, {rev_c}) :- circle_M__2({rows - 1}, {rev_c}), circle_M__1({rows - 1}, {rev_c - 1}).\n"

    rule += ":- { changed(R, C) } > 2.\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="circle_M__1"))
    solver.add_program_line(invert_c(color="circle_M__1", invert="circle_M__2"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_rect(2, 2, color="circle_M__1"))
    solver.add_program_line(avoid_rect(2, 2, color="circle_M__2"))

    # exclude checkerboard shape
    solver.add_program_line(exclude_checkboard_shape())

    # exclude border color changes more than twice
    solver.add_program_line(exclude_border_color_changes(puzzle.row, puzzle.col))

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.CENTER, "The symbol should be placed in the center."
        if symbol_name == "circle_M__1":
            solver.add_program_line(f"circle_M__1({r}, {c}).")
        else:
            solver.add_program_line(f"not circle_M__1({r}, {c}).")

    solver.add_program_line(grid_color_connected(color="circle_M__1", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(grid_color_connected(color="circle_M__2", grid_size=(puzzle.row, puzzle.col)))

    solver.add_program_line(display(item="circle_M__1"))
    solver.add_program_line(display(item="circle_M__2"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Yin-Yang",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VXva9tADP3uv2LoswaWz+c4963Lmn5Ju3XNKMWYkmbeapbUW35s6wX/79HJhhQiGIyNlTEcPV7eKdKzo/Otv25nqwqJwsfkGCMzTG0mQZRIxP01rTeLyr3Ak+3mvlkxQXwzHuPH2WJdRUWfVUY7P3T+Ev2ZK4AAIeEgKNFfup0/dzBvlnc1oL/idUDihUmXmTA9PdBrWQ9s1IkUM7/oOdMbpvN6NV9Ut5NOeesKP0UIzV7JrwOFZfOtgt5M+N4ZYOFu8f2+19bbD83nbZ9FZYv+5CduzcFtoJ3bwBS34SaeuD3/rW6HZdvyQ3/Hfm9dEay/P9D8QK/cjvFCkARv3A7MgMsk3OapNbCJqmaamqWqqtbNhpqax6qqdhuqFShW21Gc67JehEiX1YdBZHVZtU2kG0xCNh3JRjeYGjU71Vta3aDVndjQ8rj2QL/5Qah9nJ0rtXnQxjJuieCUpxG9EXwtGAtawYnknApeC44EU8FMcgZhnn954v+QncLwy1K57L+rllEBo2b5pVnXmwr4xd9G8AMkChPOkf9nwV85C8IfED+3/fHc7PCOhcf64eXj7OETlNEe",
        },
        {
            "url": "https://puzz.link/p?yinyang/22/18/00000000000000030190030000900003000000900130020006000l0000090000i0020009400030200060000002empf01900001009901030130900031009a00009000",
            "test": False,
        },
    ],
}
