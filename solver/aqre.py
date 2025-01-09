"""The Aqre solver."""

from typing import List

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
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
            num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
            if isinstance(num, int):
                solver.add_program_line(count(num, color="gray", _type="area", _id=i))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Aqre",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VbRa9s+EH7PX1H0rAdLJzmOX0bWtb+XLt2WjlKMCW7m0rCEtE49hkP+9346n+NfR1lbxjoGw7H86XQ6f/edZGVzWxdVqU0UfpRoPHE5k/Btk5jvSK6zxd2yTA/0uL67XlcAWp8eH+urYrkpB5l45YNtM0qbsW7+SzNllFYWt1G5bj6m2+Z92kx0M8WQ0glsJ62TBTzq4TmPB3TYGk0EPBEMeAE4X1TzZTk7aS0f0qw50yq85y3PDlCt1t9KJTxCf75eXS6C4bK4QzKb68WNjGzqL+uvtfiafKebcUt3+ghd6ukG2NIN6BG6IYvfTHeU73aQ/RMIz9IscP/cw6SH03SLdpJuFRGmWtSaK6NoGCK9AbXOMHow7hy6Sd9NHowa+0OfgntYS9J39n99MDDM44LbY24tt2egqRvi9h23Ebee2xP2OQJ7a6y2NlapxeoyDhgEGA+1JSN4BIw0A7YRMEgxht2JnWAPuTFGTCcxCTFDkgE70tZDH8bYFDGSASZjNFkv2AK3c8l4YMjHONZEkeAhcMuNsLmIJI51wO27EA9Y5lrMdTIXnEk4Yx6wvMth1/qWPznE8RLHIY5v41jE3GtlwV+4sQ7CjXXodAs6dLohpnVtjnj2+vigiejm4ePFx8PHdz74eHS6edRFuOEJLBw8OMTCIQaHWDjEZq8znsCSewQdTKcncjednqiF6eoCfYz4GwIWfbBOUJu+RqarF+piRLdQF9Ppj7lW5kKffe3wmdzXCGsDuveasz5YpOe8VA+5ddzGvISHYR8+c6ciWyGl0qTdtr++dZ7kliHVcAY8vPzfZ8sHmZrW1VUxL/HJnNSry7I6mKyrVbFUOKN2A/Vd8Z1ROPL+HVt/6NgKJYhedHi9wi54gk4GdWmom1OtbupZMZuvlwr/fPRP7dEL7ebZ/q+uDj4TqritSpUP7gE=",
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
