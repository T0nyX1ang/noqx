"""The Stostone solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, avoid_area_adjacent
from noqx.rule.reachable import area_color_connected
from noqx.solution import solver


def valid_stostone(color: str = "black") -> str:
    """
    Generate a constraint to enforce a valid stostone dropping.

    A grid rule should be defined first.
    """
    below_C = f"grid(R, C), {color}(R, C), #count {{ R1: grid(R1, C), {color}(R1, C), R1 < R }} = BC"
    below_C1 = f"grid(R, C + 1), {color}(R, C + 1), #count {{ R1: grid(R1, C + 1), {color}(R1, C + 1), R1 < R }} = BC1"
    return f":- {below_C}, {below_C1}, BC != BC1."


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row % 2 == 0, "The stostone grid must have an even # rows."

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(count(puzzle.row // 2, color="gray", _type="col"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.text[rc]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="gray", _type="area", _id=i))
        else:
            solver.add_program_line(count(("ge", 1), color="gray", _type="area", _id=i))

    solver.add_program_line(area_color_connected(color="gray"))
    solver.add_program_line(avoid_area_adjacent(color="gray"))
    solver.add_program_line(valid_stostone(color="gray"))
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Stostone",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7Vbfa9tIGHz3XxH0vA/S/tCu9JbmnL6kbnvOEYIxwXGUi6ldt/5RDhn/75lvdxaXo3CUozSFYns9/jT77UgzWmv7eT/bdKqqVFUqE1SpgJR1tbJVUK7y8VPydb3YLbv2TJ3vd0/rDYBSby8v1eNsue0GE7Kmg0PftP256l+3k6IqVKHxqYqp6t+3h/5N2w9VP8ahQlWoXSWSBhye4E08LugiFasSeEQMeAs4X2zmy+7uKlXetZP+WhWyzqs4W2CxWn/pCuqQ3/P16n4hhfvZDiezfVp84pHt/mH9YU9uNT2q/jzJHWe54STXnOQKTHIFfUOunMUPlttMj0dc9j8h+K6diPa/TjCc4Lg9YBy1h6K2mOrgtTiDWhWP3MbxMo46jteYqHoTxz/iWMbRxfEqcobop3WjtEVTDb+NAQ7EFrhJ2AK7jGul64o4ABti9BFxgl0FXBOD48mpNbAnRk/PnjV6Bvb04ARyPPQE6vHgB/I9+E3me2BNDA0NNQRoaKgheGVKckIApp7QAJPfVMDkNxqYGhoLzHWbWpkqrYt+wImDfsBJJ/oBJ74pnTK6JMZcnedCj0560Bs4aUA/ZQzruI2NSTrRD5gcjfvdOGJoNkmz0VjLci0DbZba4Kmhp+gBTG0GazmuZdDfsb9FvWYd/hr6i3nA5MBfQ3/RA5hrOWjw1ACvDb0GF3sUz71G/8D+XvaudC4xYzZjB5zzAx+pM2Yp59BJ3tJa+D5lspbskS95y/n0qPucE8lhriNjnhmQjHlq8NDgT3nQDfkN+MxY9LqkF+I184OMIANf+ZjzoHFNNK+nhi/Zd40+OnsqmcmeSmayj5ib82DAyb4bcEzmSH6y15Kf7DW8y9mwuOaWXljotNlryQA5DhxHjoM2R23ir8u+Y12X/ZUMUFuN84o5wQZzE7eZizjaONZx+/Gyq33Xvvf/d7r/lDPBFZY/0X+/ZLP95avTwaQY7zePs3mH/6Hhw9/d2Wi9Wc2W+DXar+67Tf6Nx4DjoPiniJ+JkaeK308GP+nJQCwoX9p98tLk4M4ttrs13h+7Yjp4Bg==",
        }
    ],
}
