"""The Norinori solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.solution import solver


def nori_adjacent(color: str = "gray", adj_type: int = 4) -> str:
    """
    Generates a constraint for Norinori puzzles.

    A grid rule and an adjacent rule should be defined first.
    """
    return f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} != 1."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))

    solver.add_program_line(adjacent())
    solver.add_program_line(nori_adjacent(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(2, color="gray", _type="area", _id=i))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Norinori",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7ZRNa9tMFIX3/hVh1rPQfEia0c5N7W5c98MuIQgRHEdpTO0qlePyIuP/nnNnrhAFQxcvmCyKmMvjqzP20dH17H8dVm0tHS7jZCIVLmN1WDrxYSV8LTcv27q4kuPDy1PTAqT8NJ3Kx9V2X49KVlWjY+eLbiy7D0UplJBCYylRye5Lcew+Ft1EdgvcEtKhN4siDZwMeBPuE13HpkrAc2bgLXC9adfb+m4WO5+LsltKQb/zLuwmFLvmdy3YB31eN7v7DTXuVy94mP3T5pnv7A8PzY8Da1V1kt042l2csWsGu4TRLtEZu/QU/9/u9rk5Z9RXpxMC/wqrd0VJrr8N6AZcFEfUeagq1NtQp6HqUJeQys6E+j7UJNQ01FnQTIqjUJmWKrei0HivuZXKZcwZ2EV2RiqfMkPjWeNysGd2GK8kss/AvNejr2If98GaGRoVNdBKrVmjoNGsUQpsmDHCOvrUGn3DfY2+6fsGHH1CC44+tYHGssZAY1ljUnDODD+W/VjsTXmvhSZljc3B8XmhlTrj56Ws8qgJWTnOk7JyfW7pkK2jbHs9Muxz9pQz7/WUM+9Fnsqz3lPmQ7Z9/jqBz4Q9U259zoryZ43CEdDnrClnNWTY56yhMawx0BjWGMqcv5My7DO36Fvu0zFj+Xss5UwaDNpNGLfrUG2oWRjDnOb5whP/VzulRtp/XHhzl/xcjUqxOLSPq3WNU2Ly8L2+mjftbrUVOI5PI/GfCKvEsEj774S++AlN4SdvbWrfmh38j8TPpt3QEtXoFQ==",
        },
        {
            "url": "http://pzv.jp/p.html?norinori/20/10/ahkcfeorctdhkqdffmk9jprqnqd57ea6us16ok4jboec2oku7ck43rbqseje3kc16cvv8f7i7f",
            "test": False,
        },
    ],
}
