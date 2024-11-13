"""The Yajilin-Kazusan solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def yajikazu_count(target: int, src_cell: Tuple[int, int], arrow_direction: int, color: str = "black") -> str:
    """
    Generates a constraint for counting the number of {color} cells in a row / col.

    A grid fact should be defined first.
    """
    src_r, src_c = src_cell
    op = "<" if arrow_direction in [0, 1] else ">"

    if arrow_direction in [1, 2]:  # left, right
        return f":- not {color}({src_r}, {src_c}), #count {{ C1 : {color}({src_r}, C1), C1 {op} {src_c} }} != {target}."

    if arrow_direction in [0, 3]:  # up, down
        return f":- not {color}({src_r}, {src_c}), #count {{ R1 : {color}(R1, {src_c}), R1 {op} {src_r} }} != {target}."

    raise AssertionError("Invalid direction.")


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="gray"))
    solver.add_program_line(grid_color_connected(color="not gray"))
    solver.add_program_line(count(("gt", 0), color="gray", _type="grid"))

    for (r, c), clue in puzzle.text.items():
        assert isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows."
        num, direction = clue.split("_")
        assert num.isdigit() and direction.isdigit(), "Invalid arrow or number clue."
        solver.add_program_line(yajikazu_count(int(num), (r, c), int(direction), color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Yajisan-Kazusan",
    "category": "shade",
    "aliases": ["yk", "yajisan-kazusan"],
    "examples": [
        {
            "data": "m=edit&p=7VZNb9NAEL3nV0R7AmmQdv0Rr30LpeESUiBBVWVZlhNcNTTBxakRbJT/3pnxoqwbH+BAKyFkefL8PDP7ZjxeZ/etKeoSVAAx+BokKDzCSOKFBK00n9Iei/X9pkyGMG7ub6oaAcDFZALXxWZXDlLrlQ32Jk7MGMzbJBWeAD6VyMB8SPbmXWJmYOZ4S4BGbopICfAQnh/hJd8ndNaSSiKetQkVwiuEq3W92pT5tGXeJ6lZgKB1XnM0QbGtvpeiTcHXq2q7XBOxLO6xmN3N+s7e2TWfq9vG+qrsAGbcyp33yPWPcgm2cgn1yKUq/rLcODscsO0fUXCepKT90xHqI5wne7SzZC8Cj0KD3Ec19IQwYxAS5eXU4V9UzAvkVJGlQkmUdL1GwUngiHP5bvooar2cXBGnD9xA7Z8ExhzYpawuJ1BJdSJMSc7muaFKsZ+XS5cb9fjZZd18nj7181hLl/O5SarL9Wjxe9b1e9YION8jztbR4Ti201A1sn13642sFtdP80R0/TTX5vQAp0fxDF2xnbD12C5wxMD4bN+wlWxDtlP2OWd7yfaMbcB2xD4RDelvjrGgNnk4jlidbmf6CbSluEXSBtl/hP/2vWyQinlTXxerEvegWbNdlvVwVtXbYiNw0z8MxA/BZ+qje/D/O/BM3wF6BPKPvgbP/1an2N0wAnMB4q7Ji3xVbQT+lQDi8Z17zD+5enz1xc/iy/q2MM3wBaFd8fUVXeHvS5ENHgA=",
        },
        {
            "url": "https://puzz.link/p?yajikazu/9/9/301040104010103040201030101030103040301030101020304010203030401040404040301010304010401030402030402020203040203040302020204040304020402040201010402020102020402040",
            "test": False,
        },
    ],
}
