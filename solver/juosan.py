"""The Juosan solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.solution import solver


def jousan_constraint():
    """Constrain consecutive lines."""
    # black for horizontal, not black for vertical
    rule = ":- grid(R, C), grid(R + 2, C), black(R, C), black(R + 1, C), black(R + 2, C).\n"
    rule += ":- grid(R, C), grid(R, C + 2), not black(R, C), not black(R, C + 1), not black(R, C + 2).\n"
    rule += 'content(R, C, "——") :- grid(R, C), black(R, C).\n'
    rule += 'content(R, C, "|") :- grid(R, C), not black(R, C).'
    return rule


def count_lines(area_id: int, num1: int, num2: int = 0):
    """Limit the number of horizontal or vertical lines."""
    rule = f"count_area({area_id}, N) :- #count{{ R, C: area({area_id}, R, C), black(R, C) }} = N.\n"
    rule += f":- not count_area({area_id}, {num1}), not count_area({area_id}, {num2})."
    return rule


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(jousan_constraint())

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.sudoku)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.sudoku[rc][0]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count_lines(i, data, len(ar) - data))

    solver.add_program_line(display(item="content", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Juosan",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7VZdbxM5FH3Pr6j87Ifxx4zH81ZKy0sJLC2qqiiq0jbQLAlhk2aFJsp/77n2MekioZVAiCKhZDzH9v04c8/1JOt/NpPVVJtKvq7VuOPjTZsu2zbpqvg5n93Pp92BPtzc3y1XAFq/OjnR7ybz9XQwotV4sO1j1x/q/kU3UlbpdBk11v1f3bZ/2fVD3Z9hS2mDtVMgo7QFPN7Di7Qv6Cgvmgp4COyy2yXgzWx1M59eneaV192oP9dK8jxL3gLVYvnvVOUQaX6zXFzPZOF6co+HWd/NPnFnvbldftjQ1ox3uj/8Nl23pysw0xX0NV0+z0+mG8e7Hcr+BoSvupFwf7uH7R6edVuMwzSabqti5RHBCyEVjQVuMrYVsHRFmohR3jCVaTBxnDiZlB0vZpaT8GjH1DLhjmkkdE5pTCs+jGZ9u/exj81cYlAmtfDkxCcGEgBPdJme6ySNNo3neGzduzQ+T2OVxjqNp8nmGHWwxmlrg+osutXUwJEYB8CBiWBbAYNIwkFbb4gjsMvYwUbqkLAHxiMJ9livue4NcE2MvDXzetjXxR55pQKCa6w3XK/BrSG3GhwCOdQ4rAF1EdwgV2CuRg4x1wPytswbrBxsYsRvGT8gfsv4ARwiObSwj7RvYRNpg5eDq4pNC8xcbQRmTSJsDG1iACbnCBuTbRADOHN2lQHOPF3lgTM3+GlnuQ69HPWCH3CxQS7qBT/gzAd+wJkz/LSjdvADpg20c9QOfsD5eeGnXU2e0M5RO/gB0wY6OuqIGMCsp/SAY80RB32w74fSP6K7L/2A2jJv6gFfekP6rfSA9AntReuGcRro25QegF4N698gb2DeIL1Be9E9lH5AXjmyRffAvK30DGNG+MaiHfhE8onoMfZD0rFibUVH9gPuX/oBd2DWWX512A/QHJj1FB1N0Vd6pugLvUzRUXqAcaz0wCNdeB6TFqwt7tQUh/4iHf2jNPo0NumVEOQ9+R1v0h95+/wvnRE6U36W//upf7+18WCkjm/fTw+Gy9ViMscv2XCzuJ6uyhx/HXYD9VmlS97q2v/5N/GL/k2IBNVTOwlPjQ7Opvp7s1xPPqrx4AE=",
        },
        {
            "url": "https://puzz.link/p?juosan/21/12/4ql08qtg9qt59ul5bunltnn9tntd72ta72h636h5b641bm04vmcvjo0fu1vo3s6fhuv1u0gf7fvpjo0fvjro0fs3vu0tvvgg33g42554342h553444g2g24211g121g2221341225h121g252442224465g25g1g2425g273",
            "test": False,
        },
    ],
}
