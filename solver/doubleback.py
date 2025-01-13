"""The Double back solver."""

from typing import List

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import full_bfs
from noqx.rule.loop import count_area_pass, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="black"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("doubleback(R, C) :- grid(R, C), not black(R, C).")
    solver.add_program_line(fill_path(color="doubleback"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="doubleback", adj_type="loop"))
    solver.add_program_line(single_loop(color="doubleback"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")

            # enforce the black cells to have edges on all sides
            puzzle.edge[Point(r, c, Direction.TOP)] = True
            puzzle.edge[Point(r, c, Direction.LEFT)] = True
            puzzle.edge[Point(r + 1, c, Direction.TOP)] = True
            puzzle.edge[Point(r, c + 1, Direction.LEFT)] = True

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for ar in areas:
        arb = tuple(filter(lambda x: puzzle.surface.get(Point(*x)) is None or puzzle.surface[Point(*x)] not in Color.DARK, ar))
        if len(arb) == 0:
            continue  # drop black cells

        solver.add_program_line(count_area_pass(2, arb))

    for (r, c, _, d), draw in puzzle.line.items():
        solver.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Double Back",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VZdTxs7EH3Pr0B+9sP6a7/eKBfuSwq9N1QIraIoCUuJCDc0IRXaKP+dM+MxuVWDQEJCqlRt1j4ZOzPHczx2Vt/X42WrTUYfV2r0eLwp+bVlzm8mz/nsYd7WB/pw/XCzWAJofXZyoq/H81Xba2TWsLfpqro71N3fdaOs0vwaNdTdP/Wm+1x3A90NMKS0h60PZJS2gMc7eMHjhI6i0WTAp4IBLwGns+V03o760fKlbrpzrSjOJ/41QXW3+NGq+DP+Pl3cTWZkmIwfsJjVzexeRlbrq8XtWuaa4VZ3h5Fufw9dt6NLMNIltIcureLddOez/9rHfUyr4XaLjP8LrqO6Idpfd7DcwUG9US5TtdfKudjlsau4K2zsQuxK7krDnTFe+iL2NjoyNnoyIboyIfoyeXRmcvKG4Kf1Bq3h9pLbE24tt+dgqDvH7V/cZtwGbvs85xj0rbHaWoSy2FPGA4Ml4wCM0IwLbR1oM8YWdqBC2GbAWAZj2L3YnQEGTcIe/mkpjOGTlkM4IFYusQJKosDyGSNWIbFCBYx0EM4Rq5BYOXwW4rNArFJiFfBZis8SsSqJVRbaZeKzLIGFZ5VrZyRuhTlG5lSYY9KcCjhygA/gGAs+gCMHl3ngGBc+tLMyB7l1klv4AIbUjANw5Aabdj7GhQ1YYuHgcCFycB7nSIhrx1xg8e/hM4hPDw5BOHisK5d1WdJRckUaJU1Jo6SjQ96c5DA4aCR5Jo0kFvqdjqSXxGW9JC76/+kL7RIH0itPOmJ+0r0gTSXnpCPVC2PSV+YX4JN0L2ifSFzStxQ+fKSKvSLdxQ59oeuzvtD1Wd+0N1hT2Q+saZa0Rm4zyTnpmyXdaT/EdbG+aW+Qpmk/oEacSfqS1mJ30NoljaBp0p109ElfaOeJMwr0gsv0iFvPbc7lW9Dx88YD6v0nhfIOfJAzldMpRwCbjerb0VoTgo32QbTRznLxiHl1HY2LN+TPT/j9bMNeowbr5fV42uJW6eN2OThdLO/Gc3w7vvr2/A23+banHhW/jaM/B38u+I+/4Cn72YdV0RuL4RU6DRIr1ae7M63u16PxaLrADkPueDAW5AuDsUb3D6LK9w+g6l+OhUL/ZfDDc4YzRF0t1pN5ezAZT2/VsPcE",
        },
        {
            "url": "https://puzz.link/p?doubleback/23/9/051602u9ghhls666vh35bk1stt667e518hg0i48006800uuvnhvpge766m1oso0f3g3guvuu8e040000040000000000000000000000000000000000000",
            "test": False,
        },
    ],
}
