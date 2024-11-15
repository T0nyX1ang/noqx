"""The Snake solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def exclude_checkboard_shape(color: str = "black") -> str:
    """Exclude checkboard-shape shading."""
    rule = f":- {color}(R, C), not {color}(R, C + 1), not {color}(R + 1, C), {color}(R + 1, C + 1).\n"
    rule += f":- not {color}(R, C), {color}(R, C + 1), {color}(R + 1, C), not {color}(R + 1, C + 1)."
    return rule


def simple_shade_path(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a rule to ensure the shaded path is a simple path.

    An adjacent rule should be defined first.
    """
    adj_count = f"#count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }}"

    constraint = f"pass_by_loop(R, C) :- grid(R, C), {color}(R, C), {adj_count} = 2.\n"
    constraint += f"dead_end(R, C) :- grid(R, C), {color}(R, C), {adj_count} = 1.\n"
    constraint += ":- { dead_end(R, C) } != 2.\n"
    constraint += f":- grid(R, C), {color}(R, C), not pass_by_loop(R, C), not dead_end(R, C).\n"
    return constraint


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP clue must be an integer."
        solver.add_program_line(count(num, color="gray", _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "LEFT clue must be an integer."
        solver.add_program_line(count(num, color="gray", _type="row", _id=r))

    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(grid_color_connected(color="gray"))
    solver.add_program_line(exclude_checkboard_shape(color="gray"))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))
    solver.add_program_line(simple_shade_path(color="gray"))

    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == "circle_L__1__0":
            solver.add_program_line(f"gray({r}, {c}).")
            solver.add_program_line(f":- dead_end({r}, {c}).")
        if symbol_name == "circle_L__2__0":
            solver.add_program_line(f"gray({r}, {c}).")
            solver.add_program_line(f":- not dead_end({r}, {c}).")

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Snake",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VRRb5swEH7Pr6j87AfbQCC8ZV2zlyzdlkxVhKKIMKpEJSODME2O8t/73UFHO5C2aVqeKuPTd9/Z+ON8XPmtiotUapceJ5BKagzPVzxdf8hTNWOxO2ZpeCXH1XGbFwBS3k4m8j7OynQQ0U6M1eBkR6EdS/sujIQWUhhMLVbSfgxP9n1ol9LOERIyADetFxnAmxbecZzQdU1qBTxrMOASMNkVSZaupzXzIYzsQgo65w3vJij2+fdUNDrIT/L9ZkfEJj7iY8rt7tBEyupL/lA1a/XqLO24ljvvkeu0cgnWcgn1yKWv+He52SHvEzpanc9I+CdIXYcRqf7cwqCF8/AEOwtPwtXY6uGm+E6E68ANWteFa1p3CBfF8eQGcJ2frqdeuD7tpRqoXa0p3L5aDynevswoij/zHTrs6Wyo1ax5Cc2ez5GXKRQjkt5htR6xjF9pFttD00u6dEAndmijTC9t+lc7vUcat3+153VpfP+Es2DYLnCZ0jps37JVbD22U15zw/aO7TVbl+2Q1/hUDn9YMJz2APcKYaaunue38p+0RZ5fN5LOeOWbBhuJeVXcx0mKjjCr9pu0uJrlxT7O4M+38SEVaMLngfghePIv6r725Yv3ZUq++qvufIH/6zdyIuQVf6C9leJQreN1kqOqkDXifa/DX1w9GoQov8YPVOOP",
        },
        {"url": "https://puzz.link/p?snake/11/11/00000000000000000000000000000000000000000957664857598o9", "test": False},
        {
            "url": "https://puzz.link/p?snake/15/15/13a3b00000a3d3a00000a3a4a00030a3a3a10000d3aca03001a3a3a10039a3d3a00100j3a39zp",
            "test": False,
        },
    ],
}
