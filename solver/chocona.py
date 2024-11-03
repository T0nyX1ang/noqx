"""The Chocona solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import all_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent())

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

    solver.add_program_line(all_rect(color="gray"))
    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Chocona",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7Zddb9s2FIbv8ysKXfNC/JZ8l3XJbrLsIxmKwjAKJ3XXYAmyOvEwKMh/73OoQzMBAgzFMKwXhW35pUSe84qHDy3ffdqttxtjvbz9YHpjeUXvyseGUD69vs6v7q83i1fmcHf/8XaLMOan42PzYX19tzlYaq/VwcM0LqZDM/2wWHa2M53jY7uVmX5ZPEw/LqYjM51xqTMD507mTg551OSbcl3U6/mk7dGnqpFvkZdX28vrzbuT+czPi+V0bjrJ810ZLbK7uf1r06kPaV/e3lxcyYmL9T03c/fx6k+9crd7f/vHTvva1aOZDme7Zy/Y9c2uyNmuqBfsyl38x3bH1eMj0/4rht8tluL9tyaHJs8WDxxPFw+dTwyl6nNluuBpWqm+tp9fjkEu75vZPruapXPaN21ferfu1kr/Fty6+LwdnAxgve1PSIQnHZLYe9LOEqAZsDk/vz6MEpDFqyeclQBjaztptwDOi4P4pP38hl2UO6htptCWiXxbjsfl6MrxnHk2ky/H78uxL8dYjielz5FMfz8a75g3ZzrPVHk3qHZo3BcdjPckLjqhMV10RmNQtIvGy/QVTR8pZNEDmlkS7Xs0M1Q0uYLm8oyNOtYzNurYgIeoHqDfJ/UQ6J+0f8BDUg+Be0l6L5FcSXNFzsvaEJ3ImzVvkq2mV038QeMnPA/qOTF20LGZXKPmyvQZtc9ArlFzDXge1fPgTeg1/hDR6nnIaI0zJhNkURTNeTufD71Fzz4Zh55jMs4EN/sMcBLcnDdQu6C1I54Jfs4bLHllURVNLq0dsdGz/+CI4zWOI47XOA4/QkDRI3qeB2Kjtb/HjyzKosmldWScCVovxqE1byBv0rzUK2i9iIHWvBH/Wf1H4gjmohPzkHUeqF3Q2oWEz0F9UrugtSMGWn1mxgqNogdyjZqLegWtFzFM7DXXkNDqmXpFrRcx0Op5jCZavV/qGLWOse/Rc17ioedcxDPRzZ5jz1g3jyUeWsfCWlTWIrXj1081HpS1aPEg+6Zoahe1dsRD69oTHivXwmBlmTrCYeOxcu1hobJMTWGysam5Co+Va+Gxci0MVpapLxw2HqPmisKyjqW+XnbyoulfGRc2K9fCZuU6sSdUlqk1fDZOk47N+KyMZ/rLTlyZrbwLp5Vx1gCsNmYH9Qane96pux907Mj9Vt6p9Z73kTWsjPON1vUj/Crvhdle1yT7Ldw2fuUnqTJb2Rdmra4x4bSyT91htTFb9wHhtLJPrWG1MVv3AZ6i9uwLs5V9z9jKO89dQddPCPip7Au/lXdqDcONZa114beyL/xqfUPCZ90HhN+6DyTusbJPfWG4sVz3AeG3sp+JnzW+sJw1TuYe6z5AfWG7Ma71Fa73ewJc7/cEWA6jjqW+8LznGp5Vc491f6DWsN0Y11oXrnV/KFzr/sDe0PYE6gvbjXE75ypc1/2BWsN2Y7zuFcJ12R/40X5Tfrpfl2Mox1R+0rM8WH3Ro9e/f3r4RztLfs3lYeWllzzkfLvyxVdWB8vubLf9sL7c8AB+9P73zavT2+3N+prW6e7mYrOtbf7/PB50f3flU54xw7e/RP/TXyIpQf+10fm12WG/6NaftptudfAZ",
        },
        {
            "url": "https://puzz.link/p?chocona/26/22/885kcco5lc912qccuksc8u9k8cdbs24ujt2ctre2ifbuagd77ah6bbjpubmjvt7n57t4gldt0oa6t0gi3uci41s4icrs32ar3j7cqhjpkk2lik3g3302fuitovkgv3g7tge73ifv7jejuc0r4v3ei4e1o79r01jpqune0kg1ov1f300bf783vukb00fg2mvvvggs0tvovs0g3frku1s0tg7v270064a13422432332444724242322633942221232249322222423462242621324325398321344611532442412253236225",
            "test": False,
        },
    ],
}
