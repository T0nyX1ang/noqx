"""The Shimaguni solver."""

from typing import List

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent, avoid_area_adjacent
from noqx.rule.reachable import area_color_connected
from noqx.solution import solver


def adjacent_area_different_size(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to enforce that adjacent areas have different sizes.

    An adjacent area rule and an area rule should be defined first.
    """
    size_count = f"#count {{R, C: area(A, R, C), {color}(R, C) }} = N"
    size1_count = f"#count {{R, C: area(A1, R, C), {color}(R, C) }} = N1"
    return f":- area_adj_{adj_type}(A, A1), A < A1, {size_count}, {size1_count}, N = N1."


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(area_color_connected(color="gray"))
    solver.add_program_line(avoid_area_adjacent(color="gray"))
    solver.add_program_line(area_adjacent())
    solver.add_program_line(adjacent_area_different_size(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            num = puzzle.text[Point(*rc, Direction.CENTER, "normal")]
            assert isinstance(num, int), "Clue must be an integer."
            solver.add_program_line(count(num, color="gray", _type="area", _id=i))
        else:
            solver.add_program_line(count(("ge", 1), color="gray", _type="area", _id=i))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Shimaguni",
    "category": "shade",
    "aliases": ["islands"],
    "examples": [
        {
            "data": "m=edit&p=7VVbT9tMEH3Pr0D71Er74L359kZp6AsN/Ro+IWRFkQkGoiaEJriqHOW/c2Z3FhcViVZVqSpVSdbHk9mZ4zkz683ntl43UiX0NbnEFR+rcv/Teep/CX9O5neLptyT++3d9WoNIOXx4aG8rBebZlCx12Sw7Yqy25fdu7ISSkih8VNiIrv/ym33vuyGshvjLyFz2I6CkwYc9vDU/0/oIBhVAjxiDHgGOJuvZ4tmehQsH8qqO5GC8rzxuwmK5epLI5gH3c9Wy/M5Gc7rOzzM5np+y/9s2ovVp5Z91WQnu/1Ad/wEXdPTJRjoEnqCLj3Fb6ZbTHY7lP0jCE/Lirj/38O8h+Nyi3VUboVJsFVDa6+MMObRrdLF43ub4Z5ag+4RQvlAZ3499Kv26wnyyM749a1fE786vx55nyHSa2Wk1giq0R7KAueM0XHEzeMMWDFGNxodsIbdsl3DbtluEmDLWAE7xho4ZYxclnNZYBexA8ZDewwOKXOwiJ9yfAf/lP0dfDL2cfDJ2CdFroxzpTRBbM/ALWduGXxy9skQp+A4OewF23PkKjgXJtAk0acAhliEC9gV24scOOSCL3DIBV/gUGf4SqPZrhRwqA/2AYe82Acc8mKfNFx/7ANmu3bAoVbYJ40NHLAPmDngLDEuYnB2gTN8gZmDBTfHPUAaURN6jN4wUUfUwUQdC2gXdSGtuQcsac11tqQ1x0H8h35wwJzX6+g4piPdueakaeTj0GOxN0jf2BsOHGJvpOCQMocUHGKfpNgb+8SfoBwzhz2PduoNjglNH3qgQMyCa56gbqyv106xnbSLWlPNaVg9hj/PDq69dpgFw7ODK/A3WnANce21Qw2hTa8R1xBXYO4ZzIvhmcIVmJ4Rw33qR/zAr9avqR/9jA6gHzyi/OGU04OGmDivfv3IeZZbhZLRCff44/4+22RQiXG7vqxnDd4Vw4urZm+0Wi/rBe5G7fK8Wcd7vKp3A/FV+F9l6M3/7+39h97eJEHyU+/wF5iJZ+hUqC6mpjuW4rad1tPZCj2G2nm7+s7+4uwx1AJFX9ZX7c1879V8s6hvLjavxWRwDw==",
        },
        {
            "url": "https://puzz.link/p?shimaguni/15/12/55a19a6l11nhcnqlddnqkr5cmajmaoeahc3gqv3nftavvke414681sk3e7cekml25fok2o43g1s",
            "test": False,
        },
    ],
}
