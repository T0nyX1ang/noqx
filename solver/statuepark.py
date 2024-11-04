"""The Statue Park solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    shapeset = puzzle.param["shapeset"]
    if shapeset == "tetro":
        omino_num, omino_count_type = 4, 1
    elif shapeset == "pento":
        omino_num, omino_count_type = 5, 1
    elif shapeset == "double_tetro":
        omino_num, omino_count_type = 4, 2
    else:
        raise AssertionError("Shape set not supported.")

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))

    solver.add_program_line(all_shapes(f"omino_{omino_num}", color="gray"))
    for i, o_shape in enumerate(OMINOES[omino_num].values()):
        solver.add_program_line(general_shape(f"omino_{omino_num}", i, o_shape, color="gray", adj_type=4))
        solver.add_program_line(count_shape(omino_count_type, name=f"omino_{omino_num}", _id=i, color="gray"))

    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == "circle_M__2__0":
            solver.add_program_line(f"gray({r}, {c}).")
        elif symbol_name == "circle_M__1__0":
            solver.add_program_line(f"not gray({r}, {c}).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Statue Park",
    "category": "var",
    "examples": [
        {
            "url": "https://puzz.link/p?statuepark/12/12/3g3g6000515100003ala0i003g3a0060515160003g3g0000//p",
            "config": {"shapeset": "pento"},
        },
        {
            "data": "m=edit&p=7VVNa9tAEL3rV5Q5T2Fn17Llvblu3IuTftglBCGC4yqNqB21ttXWa/zfMzsSGJI5FVJCKWIfz2/Hs2+W0Wj7o1lsSiRCMugyNMgMe2kfe5RhSgNZpnvm1W5V+lc4anZ39YYJ4vvJBG8Xq22Z5F1UkRzC0IcRhnc+BwIEy4ugwPDRH8K5h2W9vqkAw4z3AYk3pm2kZXp2opeyH9m4Fckwv+g40yumy2qzXJXX01b54PMwR4iHvZF/Rwrr+mcJnZn4uzXAws3q112nbZsv9bemi6LiiGEkbsNMMepORiNtjUamGI3+n83osDge+b4/sdVrn0fXn080O9GZPzBeCJLglT9A6jgN8TGttXOxBmlfUwcDTc1IVdW8Waqq8TT7WB1aVdVjVWfDTIslY3Q5nvckBxk1NZFaNZFaNpFaN1HM/dSJVSsnq+e2PT1avSiy+p04/U6cXqXeNKR1DbfZRJrNCs65FzE4wbeCRjAVnErMmeCl4FiwJ9iXmEHs5j/u92eykzsrU/Pxk/4LapHkMGs2t4tlyfNnXK+/19tqVwJP+WMCv0FW7uJH4//g/9uDP969eWmvw0uzwy8o7Kv71/vF/Vcokgc=",
            "config": {"shapeset": "double_tetro"},
        },
    ],
    "parameters": {
        "shapeset": {
            "name": "Shape Set",
            "type": "select",
            "default": {"tetro": "Tetrominoes", "pento": "Pentominoes", "double_tetro": "Double Tetrominoes"},
        }
    },
}
