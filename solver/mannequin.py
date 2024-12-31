"""The Mannequin Gate solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def distance_in_area(grid_size: Tuple[int, int]) -> str:
    """Generate a rule to calculate the distance between grids in an area."""
    r, c = grid_size
    rule = "dist(R, C, R, C, -1) :- grid(R, C).\n"
    rule += "dist(R, C, R0, C0, N) :- grid(R, C), grid(R0, C0), dist(R0, C0, R, C, N).\n"
    # The following r + c upper bound is not rigorous.
    # TODO Actually it's better to pre-calculate the distance in python for this puzzle.
    rule += f"dist(R, C, R0, C0, N) :- grid(R, C), grid(R0, C0), N < {r + c}, (R0, C0) != (R, C), area(A, R, C), area(A, R0, C0), N - 1 = #min{{ N1 : adj_4(R0, C0, R1, C1), area(A, R1, C1), dist(R, C, R1, C1, N1) }}.\n"
    return rule.strip()


def mannequin_constraint(color: str = "black") -> str:
    """
    Generate a rule to enforce the Mannequin Gate constraint.

    An area_adjacent rule and a dist rule are required.
    """
    rule = f"area_num(A, N) :- area(A, R0, C0), area(A, R1, C1), {color}(R0, C0), {color}(R1, C1), (R0, C0) < (R1, C1), dist(R0, C0, R1, C1, N).\n"
    rule += ":- area(A, _, _), area_num(A, N0), area_num(A, N1), N0 < N1.\n"
    rule += ":- area_adj_4(A1, A2), area_num(A1, N), area_num(A2, N).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(area_adjacent())
    solver.add_program_line(distance_in_area(grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(mannequin_constraint(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(target=2, color="gray", _type="area", _id=i))
        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(f"area_num({i}, {data}).")

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
    "aliases": ["mannequingate", "manekingeto"],
    "examples": [
        {
            "data": "m=edit&p=7VTBbtpAEL3zFdGe57C7Nq3tG02hF0raQhVFloWM4zSoUFODq2oR/54347WoVKKkjcQpWnv0PPtm/GY86+3PJq9L6mMFEWkyWNZGcoear27NlrtVmVzQoNndVzUA0dVoRHf5alv2Us/KensXJ25A7kOSKqNIWdxGZeQ+J3v3MXFDclNsKYrgG7ckCzg8wmvZZ3TZOo0GnngMeANYLOtiVc7HredTkroZKX7PO4lmqNbVr1J5HfxcVOvFkh2LfIditvfLjd/ZNrfV98ZzTXYgN2jlTk/IDY5yGbZyGZ2Qy1W8XO5qU50SGmeHAxr+BVLnScqqvx5hdITTZA87SfbKag4NoKL9KsoGXdHe0ReG7hyIMxJ9I3Yk1oqdITm5QOx7sVpsX+xYOEO8Mw7REbzGIqEOyBjbYmOBvd+wP/ScGBgqBGMe/8Tax2qONT6WOV3OCDj2GHm4XsYWk20934JvPd8iD7eg8weeH4AfcB7UcC2VXIoNxb6RCt9yc5/Zfmk8ElvkjNpv8fLOPqkt5bL96j8PZb1UTZv6Li9KTNzw9lt5Manqdb7C06RZL8q6e8ZRP/TUbyV3iu9H4evpP/vp5+brf/oHnGHunpCTYgy6vwK5K1KbZp7Piwozht7JbvejeGT7/4OnZONH/Pov/9n7hiOrfjT1clE1Kus9AA==",
        },
    ],
}
