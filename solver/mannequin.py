"""The Mannequin Gate solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def dist(grid_size: Tuple[int, int]) -> str:
    """
    Generate a rule to calculate the distance between grids.
    """
    r, c = grid_size
    rule = "dist(R, C, R, C, -1) :- grid(R, C).\n"
    rule += "dist(R, C, R0, C0, N) :- grid(R, C), grid(R0, C0), dist(R0, C0, R, C, N).\n"
    # The following r + c upper bound is not rigorous.
    # Actually it's better to pre-calculate the distance in python for this puzzle.
    rule += f"dist(R, C, R0, C0, N) :- grid(R, C), grid(R0, C0), N < {r + c}, (R0, C0) != (R, C), area(A, R, C), area(A, R0, C0), N - 1 = #min{{ N1 : adj_4(R0, C0, R1, C1), area(A, R1, C1), dist(R, C, R1, C1, N1) }}.\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(dist(grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(
        "area_num(A, N) :- area(A, R0, C0), area(A, R1, C1), gray(R0, C0), gray(R1, C1), (R0, C0) < (R1, C1), dist(R0, C0, R1, C1, N)."
    )
    solver.add_program_line(":- area(A, _, _), area_num(A, N0), area_num(A, N1), N0 < N1.")

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    area_id = [[None for c in range(puzzle.col)] for r in range(puzzle.row)]
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(target=2, color="gray", _type="area", _id=i))
        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(f"area_num({i}, {data}).")

        for r, c in ar:
            area_id[r][c] = i

    area_adj = set()
    for r in range(puzzle.row):
        for c in range(puzzle.col):
            if c < puzzle.col - 1 and area_id[r][c] != area_id[r][c + 1]:
                area_adj.add((area_id[r][c], area_id[r][c + 1]))
            if r < puzzle.row - 1 and area_id[r][c] != area_id[r + 1][c]:
                area_adj.add((area_id[r][c], area_id[r + 1][c]))
    for a1, a2 in area_adj:
        solver.add_program_line(f"area_adj({a1}, {a2}).")
    solver.add_program_line(f":- area_adj(A1, A2), area_num(A1, N), area_num(A2, N).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Mannequin Gate",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVBb9pMEL37V1R7nsPu2rTgW0qhF0qaQhVFloWM6yhWzWdq46paxH/Pm/Fa9ECVfo0U9VAtHj1m3sy+Ge9C+63LmoJGWOGYNBksa8fyRJo/w1qXh6qIX9FVd3ioGwCi6/mc7rOqLYLEs9Lg6CaxuyH3Pk6UUaQsHqNScjfx0X2I3ZLcCiFFBr5FT7KAszO8lTijae80GnjpMeAdYF42eVVsFr3nY5y4NSne561kM1S7+nuhvA7+nte7bcmObXZAM+1DufeRtvtSf+0816Qncle93NkFueFZLsNeLqMLcrmL58ut9vUloZP0dMLAP0HqJk5Y9eczHJ/hKj7CLuOjsppTQ6jo34qy4dC0d4yEoQcH8oxk34mdi7Vi1yhOLhT7TqwWOxK7EM4Me04iTATbWBTUIRlje2wssPcb9keeMwGGCsE4jz9j7XM15xqfy5yh5hh44jHqcL+MLU629XwLvvV8izo8gsEfen4Ifsh10MOtdDIVG4l9LR2+4eH+r/E/f5hPykm4U79Gv4fSIFGrrrnP8gKHbFrv9nVbHgqFu3wK1A8lT4IXRNG/6/3i15uHr/+2U/aEnARzHa49uWtS+26TbfK6UviHIIkOvwS/CP9h8ovPARdO/dc15bbuVBo8Ag==",
        },
    ],
}
