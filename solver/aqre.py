"""The Aqre solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(4, 1, color="gray"))
    solver.add_program_line(avoid_rect(1, 4, color="gray"))
    solver.add_program_line(avoid_rect(4, 1, color="not gray"))
    solver.add_program_line(avoid_rect(1, 4, color="not gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.text[rc]

            if data == "?":
                continue

            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="gray", _type="area", _id=i))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Aqre",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VZNa9tAEL37V4Q970H7Jcu6lDRNekmdtk4JQQijuAoxtVEiR6XI+L/nzWhkNSUllNIvKLJGb0ezozdvdiVv7pqiLrWJ6OcSjSsObxI+bRLzGclxvrxflemBPmzub6oaQOuzkxN9Xaw25SiTqHy0bSdpe6jb12mmjNLK4jQq1+27dNu+Sdupbme4pXQC32kXZAGPB3jB9wkddU4TAU8FA14CLpb1YlXOTzvP2zRrz7Wi57zk2QTVuvpcKuFB40W1vlqS46q4RzGbm+Wt3Nk0H6tPjcSafKfbw47u7Am6bqBLsKNL6Am6VMUvpjvJdzvI/h6E52lG3D8MMBngLN3CTtOtcg5TLXrNnVFuTJlegFrvmDy67z2GyTBMHt019puxo3BaSzL29qsxGBjmccn2hK1lew6aunVsX7GN2Aa2pxxzDPbWWG1trFKL1WU8MAgwHmvrjOAJMMokbCNgkGIMvxe/g59qY4ycXnI65KQiCXunbYA+jLEpYhQD7IzRzgbBFrib60wAhnyMY+1cJHgM3HFz2FzOSR7rgbtnIR+wzLWY62UuODvhjHnA8iyPXRs6/s4jT5A8HnlCl8ci514rC/7CjXUQbqxDrxvp0OuGnNZ3NeI66BNIE9EtICZITEBM6GPw8uh1C+iLcMMVWDgEcIiFQwwOsXCIzV5nXIGl9gg6mF5P1G56PdEL0/cF+hiJNw5Y9ME6QW+GHpm+X+iLEd2oL6bXH3OtzIU++97hNbnvEdYGdB80Z32wSC94qR6x9WxjXsJj2oc/tFN/frc8SydDdfTaf3yEf8+XjzI1a+rrYlHiLTlt1ldlfTCt6nWxUvgs7Ubqi+Izc/SV+/+l+kNfKmpB9LftgmfoZFDXjXV7ptVtMy/mi2ql8GdHf8f/29ljG6viri5VPnoA",
        },
        {
            "url": "https://puzz.link/p?aqre/18/18/aba2qqg6mi2nhodt6jfc57m8qt96l6a1828b1j6ucn7p5bspeseknpl0od86h00o00svvhe3e41s3g8r2gr3v9u0241vvvrufs3gf3soc0m1g21c3o3k3sn000s0g1g1g22g11g2g22g1g2212g1g1112233355g555355g3g3g355",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?aqre/21/17/144g3ab85s7kb44ql7sl61gc600ccc66cc66ic69c286i1g9cfu6nlltag1a4g1420081q5816tq1dvmh850l248h00g0321300001800kkbkaa18552l2lllllcdhkbvvk2fv404g7411g0115111339001112000182",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?aqre/25/18/g60o30c1g4000014o20vtofvvrgvu971vt1e30o0820g0gs1o1g2fg2g8v8d0hm1q138jk32r7cfdn6ouo0280000000vvvvvvuvo194fis9001014000vu07svufnsvv0nu80fu4nvfvq1u0011s000707to603oo0c000vvvvvg2g2g2h346g31gf1221g11311dg22451-10c9g36420505",
            "test": False,
        },
    ],
}
