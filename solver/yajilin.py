"""The Yajilin solver."""

from typing import List

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.rule.variety import yaji_count
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="gray"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
    solver.add_program_line(fill_path(color="white"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
    solver.add_program_line(grid_color_connected(color="white", adj_type="loop"))
    solver.add_program_line(single_loop(color="white"))

    for (r, c, d, pos), clue in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        solver.add_program_line(f"gray({r}, {c}).")

        # empty clue or space or question mark clue (for compatibility)
        if isinstance(clue, str) and (len(clue) == 0 or clue.isspace() or clue == "?"):
            continue

        fail_false(isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows.")
        num, d = clue.split("_")
        fail_false(num.isdigit() and d.isdigit(), f"Invalid arrow or number clue at ({r}, {c}).")
        solver.add_program_line(yaji_count(int(num), (r, c), int(d), color="black"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Yajilin",
    "category": "loop",
    "aliases": ["yajirin"],
    "examples": [
        {
            "data": "m=edit&p=7VRRb5swEH7nV1T37AeMCSV+mbKu2Quj25KpqhBChFGVjYyOhKlzxH/v3ZmMTG2nVZMyTZqIv3z+uDOfz3Cbr13elkK69FOhwH+8fBny8MKAhztcy2pbl/pEzLrtTdMiEeJiPhfXeb0pnWSISp2dmWozE+a1TkCCAA+HhFSYd3pn3mgTC7PAWyBC1CIb5CE9H+kl3yd2ZkXpIo+R42IS6RXSomqLuswiq7zViVkKoOe85GyisG6+lTD4oHnRrFcVCat8i5vZ3FS3w51N97H53A2xMu2FmVm70d6uP9pVo12i1i6xR+zSLv7Ybl19Ke8eczpN+x4r/h69Zjoh2x9GGo50oXeIsd6Bcin1Bdqgo8H1JpLXysj3IAWKJJWpUQo5TR5KU89GHSRKlzO9jM5pr8nJQ00Nue6B5vs27lALOPeHW9yD5J1cMc4ZPcYlblQYxfiK0WWcMEYcc854yXjG6DMGHHNKpfrNYoIfgPZtSY9gKlH20/z5mvx7WuoksOja67wo8XWO8LU+iZt2ndc4i7v1qmz3c2wkvQN3wCNR1Jf+95bj9xaqvvusDvP3v9HELIQfCHMh4LbL8qxo8PXCsv1SP31CD5+pP7XOw+cevWrYR+B7/qnCE4fUuQc=",
        },
        {
            "url": "https://puzz.link/p?yajilin/19/13/g24g33f45o23d30g32z43k41y11a11a42zo33a14a12b11d31a32c21e11t36g31e21y",
            "test": False,
        },
    ],
}
