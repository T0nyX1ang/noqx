"""The Dotchi-Loop solver."""

from noqx.puzzle import Puzzle
from noqx.rule.common import area, defined, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction
from noqx.rule.loop import loop_straight, loop_turning, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def dotchi_constraint() -> str:
    """Generate a constraint for the Dotchi-Loop puzzle."""
    rule = "turning_area(A) :- area(A, R, C), white(R, C), turning(R, C).\n"
    rule += "straight_area(A) :- area(A, R, C), white(R, C), straight(R, C).\n"
    rule += ":- area(A, _, _), turning_area(A), straight_area(A)."
    return rule


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(defined(item="white"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="dotchi"))
    solver.add_program_line(fill_path(color="dotchi"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="dotchi", adj_type="loop"))
    solver.add_program_line(single_loop(color="dotchi"))
    solver.add_program_line(loop_straight(color="dotchi"))
    solver.add_program_line(loop_turning(color="dotchi"))
    solver.add_program_line(dotchi_constraint())

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        validate_direction(r, c, d)
        if symbol_name == "circle_L__1":
            solver.add_program_line(f"white({r}, {c}).")
            solver.add_program_line(f"dotchi({r}, {c}).")
        if symbol_name == "circle_L__2":
            solver.add_program_line(f"not dotchi({r}, {c}).")

    for (r, c, _, d), draw in puzzle.line.items():
        solver.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

    solver.add_program_line(display(item="grid_direction", size=3))

    return solver.program


__metadata__ = {
    "name": "Dotchi-Loop",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7Vbvaxs5EP3uvyLoswo70v7Q7rdcmtwXN7lrUkJYjHEcX23qdF3/OMIa/+95I8nY7U7I3RUChcNe+XlG0rx5Gkm7+rYZLSeaEv5ap/GLT0rOP8bl/kni52a2nk+qE326WU+bJYDWVxcX+q/RfDXp1bHXoLdty6o91e3vVa2M0v4hNdDtn9W2/VC1d7q9hktpgq0PREobwPMDvPV+RmfBSAnwZcSAd4Dj2XI8nwz7wfJHVbc3WnGc3/xohuqx+XuiwjD/f9w83s/YcD9aI5nVdLaIntXmofmyiX1psNPtaaDbF+jaA12GgS4jgS5n8dN057OvkyeJaTnY7aD4R3AdVjXT/nSA7gCvqy3aS9+Sb++qrbKEaQhxjrkpa0VrJloLyZqmojWH1XSsTrJmRrSWkjUXs8g5i25f5tDpW4h8C7GvS0Qr69CJ5phvp2/JfDt9S5FvKapOiUiCElE1Sjg9wSzmR4m4IERybyOKT0asITI8d9dsZd5WXBayYh1RKgpIci1SKi4YpWKFUSZnmcvLkHM6P5ix4y78vjO+vcG21K317XvfJr7NfNv3fc6xQw2l2rBq4GQI57FFSI8LYLBibHBWp4jJ2CbASNljAkYBMU6NNhmE8xhzZnHONANG0owzzF/E+TPMWcQ5C4x1cSzuA8vVB4xfbSnEsokBDn0sWW0N9PU4BQ6x4Nc28odf2zTwhx84xIIfOM6ZkrZZ4A8/cJwf/O2ef1Zqw8vAOEfufBh4jNx5HTwGfz4OPIZueRybI8c85p5jnn3uDmNdHOs49zjWWeCorYOGLmrroOGRPoYPA48Ry8VYju/TGMshVhljleDMB8JewyTEwi/wXlvkm0QdkhI6Rw350qY4lqAVRQ2J14LnQRHd+lI6823q29yXWMH3wn++Of5tNavUgFvp+LCGIAywiFyblvkeIT4KgODlFbZhG7yaR42y4VeX7z/Zr2cb9GrVx2V/ctksH0dzXPnnD5+P/l1PR4uJwkvWrqeelH9qy+9s/793vf17F6ufvNke+odb4RU6NYSNe0+3V1otNsPRcNygtqCdd4btKDuxe2UH9vfL02FPv+AM27zjfHPNcIKoh2Y9ns7ezZtmoQa9Zw==",
        },
        {
            "url": "https://puzz.link/p?dotchi/11/11/00g5g5k5k5k5k5k5k1k100fv003v0000000000vo00vu13a0b3j3a6a6j6j6a3a3j6b6b3a3a3b6j6j393a30",
            "test": False,
        },
    ],
}
