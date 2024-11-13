"""The Magnets solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.solution import solver


def magnet_constraint() -> str:
    """Generate the magnet constraint."""
    constraint = ":- math_G__2__0(R, C), math_G__2__0(R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__3__0(R, C), math_G__3__0(R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__2__0(R, C), area(A, R, C), not math_G__3__0(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- math_G__3__0(R, C), area(A, R, C), not math_G__2__0(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    constraint += ":- gray(R, C), area(A, R, C), not gray(R1, C1), area(A, R1, C1), adj_4(R, C, R1, C1).\n"
    return constraint.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_cc(["math_G__2__0", "math_G__3__0", "gray"]))
    solver.add_program_line(adjacent())

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        assert len(ar) == 2, "All regions must be of size 2."
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__2__0", _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "BOTTOM clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__2__0", _type="row", _id=r))

    for (r, c), num in filter(lambda x: x[0][0] == puzzle.row and x[0][1] >= 0, puzzle.text.items()):  # filter bottom number
        assert isinstance(num, int), "LEFT clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__3__0", _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == puzzle.col and x[0][0] >= 0, puzzle.text.items()):  # filter right number
        assert isinstance(num, int), "RIGHT clue should be integer."
        solver.add_program_line(count(int(num), color="math_G__3__0", _type="row", _id=r))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")

    solver.add_program_line(magnet_constraint())
    solver.add_program_line(display(item="math_G__2__0"))
    solver.add_program_line(display(item="math_G__3__0"))
    solver.add_program_line(display(item="gray"))
    solver.solve()
    return solver.solutions


__metadata__ = {
    "name": "Magnets",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7VZhj9pGEP3Or4j2a7eSd9f2rv3teuX65UraclV0shAixElRoU7hqCqf+O95M54F6nJBpGrSRBV4/fyY3Zl5s2N28/t2tq61SejrgsYdn9QEvmzI+Urkc7d4WNblM321ffilWQNo/fzmRr+eLTf1oKKZ+EwGj21Rtle6/a6slFFaWVxGTXT7Y/nYfl+2Q92O8ZPSAdxtZ2QBhwf4gn8ndN2RJgEeCQa8B5wv1vNlPb3tmB/Kqr3Tivx8w7MJqlXzR60kDnqeN6uXCyJWsze/1Q8boTfbV82vWzE0k51urzhWsT8RsDsETLALmNCJgCmPfzPgYrLbQfWfEPK0rCj6nw8wHOC4fMQ4Kh+VszQVhTFdaZRLiXBHRB7ViEToTUl5yhGROSLSA+H7XoLpESZJen5NUvQcG8uejxnn+7OyfnQm55X/wvTDMTmnsI8Y4hiW6J7HGx4tj3dQULeOx295THjMeLxlmyGEtWmibYo0LfZ9aoDhlLBFO0VMfJZ1OMu0zZEy4Rw2e1yg9SAo4eC0LZAy4QItucceGIkzDtqZbn1nzBFGX5suHuZt5xd37Vzni7FFvRnnwN36uGsnuWA9rNPFg/vehvzaQmIuCu2ooGSTkF/IG+0Fcy4h4hRYdAjQIa7joU/kCdM+YmzpdST2iFN8sYaZ8Bn08cJ71CL6Ij6TmDPo5mONEE/kU6yfiubE0w4n7KimglPETJuN10HuEhvygyYdjzt0E56wjTpDHyf6YE0nazJ2orNDjag7eU2qi8wlbKRGBrkbqZFBjeLchOou9SX9k8iT/mJPOBG/CdU06ok4E9E5QJ8gOQLHdcjGBqlRoFqLVlQXHzHVV/T0qEu0J+zFF9l40dNDTy+1zqFz5DPsf2rhqHMW+wI2ucSTY29QU3NdaA+IDTTEs/DIJdo7qmmsNexTiSfF3mAeTfyCW/max5THnFvc0yv0opfsP3+bnA2nQhbytysf/3GfJ4NKjbfr17N5jT+m4as39bNRs17NlngabVcv6/Xh+bpZvW02i4da4YiwG6g/FV+VoxPH/6eGT3NqoAok/7VtfSacqr3XaNn2uVZvt9PZdN5ge0G4y/nxhfwX7NdfyJ9cZ0R8pb7C5pUj1t8NPAy+fr/BUyt/3hV5Kq9wTpDwnonTD534QR6LcxOLL7T7TtbuKf7SbvokeX30dzpOK5PBOw==",
        },
    ],
}
