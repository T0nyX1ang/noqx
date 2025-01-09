"""The Fillmat solver."""

from typing import List

from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, avoid_region_border_crossover, general_shape
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(general_shape("fillmat", 1, OMINOES[1]["."], color="grid", adj_type="edge"))
    solver.add_program_line(general_shape("fillmat", 2, OMINOES[2]["I"], color="grid", adj_type="edge"))
    solver.add_program_line(general_shape("fillmat", 3, OMINOES[3]["I"], color="grid", adj_type="edge"))
    solver.add_program_line(general_shape("fillmat", 4, OMINOES[4]["I"], color="grid", adj_type="edge"))
    solver.add_program_line(all_shapes("fillmat", color="grid"))
    solver.add_program_line(avoid_region_border_crossover())

    tag_be = tag_encode("belong_to_shape", "fillmat", "grid")
    solver.add_program_line(
        f":- grid(R, C), grid(R1, C1), adj_4(R, C, R1, C1), not adj_edge(R, C, R1, C1), {tag_be}(R, C, N, _), {tag_be}(R1, C1, N, _)."
    )
    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        if isinstance(num, int):
            solver.add_program_line(f":- not {tag_be}({r}, {c}, {num}, _).")

    for (r, c, d, _), draw in puzzle.edge.items():
        assert d is not None, f"Direction in ({r}, {c}) is not defined."
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Fillmat",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7VRRb5swEH7nV1T3fA/YJoT4Zcq6ZC8Z3dZMVYVQRFK6ooHoIEyTo/z3ng+WFClptEXqNGkiPr677y7+fNiuvzdJlaJw7U8FSG96PBHwkIHPw+2eebbOU32B42b9UFYEEK+mU7xP8jp1oi4rdjZmpM0YzXsdgQTkISBG80lvzAdtQjTXRAEKis0ICUBJcLKHN8xbdNkGhUs47DDBW4KrrFrl6WLWRj7qyMwR7DxvudpCKMofKbRl7K/KYpnZwDJZ02Lqh+yxY+rmrvzWdLki3qIZt3InB+SqvVwLW7kWHZBrV3G23PTua1o3y0NaR/F2Sz3/TGoXOrLCv+xhsIfXekM21BtQri19Q0LaDwNKUMB++c4dkSt3ru+Rq3aukLKXLWTQ571+uRgM+75vZ3uW7w+e8SRRsNBbtlO2ku2c1oFGsX3H1mU7YDvjnAnbG7aXbD22PucMbSd+q1fnywHP9msU0DkQEqX0QauTEiPVnsT+M/j3YrETwYT27kVYVkWS0/4Nm2KZVr98ui22DvwEHrwpvP8XyN+4QGz/3Vc+Guee1IhauztVaK4QHptFsliVtM+of5amw3eYAKqhuuGROqKHRAdHaeG9TCuklD+tPjU3/fkLyk/QJ9Z9TPmrf3u6BeE+y/MiWUPsPAE=",
        },
        {
            "url": "https://puzz.link/p?fillmat/21/12/1b3e2d4d2h1i2d21p12b4z3b3e4j2m3e4b2e2d3c3c2b4h2b1g2d4n3h3b2o3b4d3c1e1a2f",
            "test": False,
        },
    ],
}
