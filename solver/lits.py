"""The Lits solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, avoid_rect, count_shape, general_shape
from noqx.solution import solver


def avoid_adjacent_same_omino(num: int = 4, color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An area adjacent rule, an omino rule should be defined first.
    """
    tag = tag_encode("belong_to_shape", "omino", num, color)
    return f":- area_adj_{adj_type}_{color}(A, A1), A < A1, {tag}(A, _, _, T, _), {tag}(A1, _, _, T, _)."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for i, o_type in enumerate(["L", "I", "T", "S"]):
        o_shape = OMINOES[4][o_type]
        solver.add_program_line(general_shape("omino_4", i, o_shape, color="gray", _type="area", simple=True))

    solver.add_program_line(all_shapes("omino_4", color="gray", _type="area"))
    solver.add_program_line(count_shape(1, "omino_4", _id=None, color="gray", _type="area"))
    solver.add_program_line(area_adjacent(color="gray"))
    solver.add_program_line(avoid_adjacent_same_omino(4, color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "LITS",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VXfa9s8FH3PX1H0rAdLV7Jlv2X90r103beloxQTSpq6a1hKuvwYwyH/e8+VrjCDwh4GpYOR+Ork5ujeIx3L3n7fzzedNgV/KWiM+DgT4mVDGa9CPpfL3aprTvR4v3tYbwC0/nh2pu/nq203aoU1Gx36uunHun/ftMoorSwuo2a6/9Qc+g9NP9H9FH8pbZA7TyQLOBngVfyf0WlKmgL4QjDgNeBiuVmsupvzlPm/aftLrbjPuziboXpc/+iU6ODfi/Xj7ZITt/MdFrN9WD7JP9v93frbXrhmdtT9OMmdviCXBrkMk1xGL8jlVfy53NXT+iWh9ex4xIZ/htSbpmXVXwYYBjhtDogXMZoYr2M8i9HGeAmq7inG/2IsYvQxnkfOpDkoa6y2tlSNhbfGA9eCK23JJGyBnWAqgJ1gzHUylxxwSNgZbb0XDI4XjgPHZw56eenlUL+U+g63amkT9uCUwvHgVMLx4FTCKaGnEj0l+lbSt+RbPnNqYEq4Aj8IvyLgSjB6BekVkK8lH6C5Fs0haCqkZqiBpWaN81ZIzbrSZERnDY5JHCoMcNKGecCpPvFZtWkuwQsSL8g44NSXTKmJioQt8iR564GTZnA1uaSN4AuJL+RQ30t97D/l/bd4HFhZo8X+SH14DixrZH9J1kjYE5I1sqdO8g75fD+wvy77jvpO6rOP+R5gH7MGj76l9C1Rs5Sa7F32nf3KvlfgVNlH9MpeB2jOXrN32d+AXmHwbvAXfWvpWyNfyx6yR+Iv/AQWv9gj8RQjsHAM+5i9Az/7y35lf9mj7Cn2nGTPMQ7+sndy7jAOXuOskZxBjMDZX8zN9wCB74QPX0h8wQicfUff6AUO/VU8+qcxuhjL+Eio+Nnyyk+f38ppsQP8Evv14/++3GzUqul+cz9fdHjyT+6+dicX683jfKXwij2O1E8Vr5b4jf3vrfvqb13e/OKt3f1vTQ7Oo1otd1s1Gz0D",
        },
        {
            "url": "https://puzz.link/p?lits/24/24/0000000o01lnmg5dvc0dntsq94ia94i814i914i976i94i294i294i8t4i90ci94ki94s294j094ia14i9pki944i94o1mregamtm0rddc00010002002dhm02i14080044vvvk6001os0001vvvq1g00a4000sfvvvsc003p80073fvvq700080000g3vvu100021g0087vvv8114102295g296oo",
            "test": False,
        },
    ],
}
