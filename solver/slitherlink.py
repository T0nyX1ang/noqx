"""The Slitherlink solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import direction, display, fill_path, grid, shade_c
from noqx.rule.loop import separate_item_from_loop, single_loop
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def convert_direction_to_edge() -> str:
    """Convert grid direction fact to edge fact."""
    rule = 'edge_top(R, C) :- grid_direction(R, C, "r").\n'
    rule += 'edge_left(R, C) :- grid_direction(R, C, "d").\n'
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="slither"))
    solver.add_program_line(fill_path(color="slither"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="slither", adj_type="loop"))
    solver.add_program_line(single_loop(color="slither"))
    solver.add_program_line(convert_direction_to_edge())
    solver.add_program_line(adjacent(_type="edge"))

    flag = False
    for (r, c), clue in puzzle.text.items():
        if clue == "W":
            flag = True
            solver.add_program_line(f"wolf({r}, {c}).")
        elif clue == "S":
            flag = True
            solver.add_program_line(f"sheep({r}, {c}).")
        else:
            assert isinstance(clue, int), "Clue should be an integer or wolf/sheep."
            solver.add_program_line(count_adjacent_edges(int(clue), (r, c)))

    if flag:
        solver.add_program_line(separate_item_from_loop(inside_item="sheep", outside_item="wolf"))

    for r, c, d in puzzle.edge:
        solver.add_program_line(f":- not edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_top", size=2))
    solver.add_program_line(display(item="edge_left", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Slitherlink",
    "category": "loop",
    "aliases": ["slither"],
    "examples": [
        {
            "data": "m=edit&p=7VRNb9pAEL3zK6I978Efa7B9oyn0Qp22oYoiy0KGuMWKqVODq2gR/z1vxqaLVUdRRcWpMh692fdmmZ3Z8fZnnVaZHOFRnrSkjccdWvw2v+Mzz3dFFl7Jcb1blxWAlDfTqfyWFttsELeqZLDXQajHUn8IY+EKKWy8jkik/hzu9cdQR1LfghLSxtoMCAIHcGLgHfOErptF2wKOWgx4D7jKq1WRLWbNyqcw1nMp6H/ecTRBsSl/ZaIJY39VbpY5LSzTHQ6zXedPLbOtH8rHutXayUHqcZPupCdd16RLsEmXUE+6dIqz080evmfPfZkGyeGAin9BroswprS/GugbeBvuYaNwLxwPoS6ajHDs5gRwqeeN6xLrGHcIl+5E6466bDdWWR2xsjtiRbFG7HXZIW1lshq5XZdYI/bpj8xWPm1lxD7FnrCq63aPH1CsYYPT46NgNpftnu2UrcN2jqpK7bJ9z9Zi67GdsWbC9o7tNVvFdsiaEfXlrzp3fjroPc4X+Oicj8YSsF0lbYVVt8V0ARh7WIeIsDpq3jxP7EB68mCTf+0lg1hMMA5XUVlt0gJDEdWbZVYdfXyADgPxLPjlTqv/36TLf5Oo+taF7/e54xajsL8nQuobKZ7qRbpYlbhlqJ6hMSSv0s3c9NOYv34C8/jahu3w/UFfvHaYbrEt8t06q4r8x6NIBi8=",
        },
        {
            "data": "m=edit&p=7VVNb9NAEL37V1R73sPO+iO2b21JuIRASVBUWVaVpIZGJArkA1WO8t87+5zAegLlgEBIoI1Hk+eZ5zezX5vPu8m60hmPKNZGE48oNnjSyP3McYzm20WVX+jL3fZhtWZH69e9nn4/WWyqoDhGlcG+zvL6Rtcv80KFSivix6pS1zf5vn6V1wNdD/mV0sRYnz0OCNntNq5ld4z3DrxuIg27g+a9y7pldzZfzxbVXb/JeJMX9Ugr95krpDhXLVdfKtWk4f9stZzOHTCdbLmWzcP80/HNZne/+rg7xlJ50PVlo7b7vFrnPqfWaftltdX9h+rxe0Kz8nDgfr9lqXd54VS/++YO8z3bQb5XNnXxPBfkZoNJbHaq9AiE5ICh0ukJCCUQy5REABE4rAdYB4xdQ04IWP2cjgQgtZUDrZ74WCqJocSPAKtPEoPW0xaD1Q9JjAhJZD0JaL2eJGckHUnSQQ98AC1o5aAejzZFjldgGskIWXEmpysDqf+ZTM5Xhp74wFk5ZOS6ICNnjIxcXWTOiQiNMV4QgbodJJtFhLpaCLh9xIK6RWTl1JGVi4Ys+tFOO6stPFPUbIwWIuePQrlQKJQbjqJ2Q3inEvbrLWwP1sKOeDvrOoR9AWtgY9g+YrqwY9hr2Ag2QUwHNj0dDT8+Mr6GeKfHb1d2CAqb4trxR/x3IWVQqC4fwxeD1Xo5WfBhPNgtp9X69J+vvUOgHhWewmob84Xw/yr8w1eha775+YX4T282XqdFGTwB",
        },
        {
            "url": "http://pzv.jp/p.html?slither/25/15/i5di5di6bg3ad13dc13bd3cg5bi7ci7dhai6bi6ci7b02bd33cc23d8ci8ai6cibh6di6bi7dg1ca31ab10dc3dg6bi6ai6chai7ci7ci8d33dc33cc20d8bi7di7cidh8di5ci6cg3dd03cb02ad3dg6bi7ci6bg",
            "test": False,
        },
    ],
}
