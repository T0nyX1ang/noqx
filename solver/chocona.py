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
            "data": "m=edit&p=7Zdfb9s2F8bv8ykKXfNC/CvJN0PWJe9Nlm5LhqIwjMBx3TVYArdOPAwK8t37O9ShWQMZimLY3l0UtuWHEnnOIx7+aPn+4265XRvr5e170xrLK3qXPzaE/Gn1dXnzcLuevTDHu4f3my3CmFenp+bd8vZ+fTTXXoujx3GYjcdm/N9s3tjGNI6PbRZm/Hn2OP44G0/MeMGlxvScO5s6OeRJla/zdVEvp5O2RZ+rRr5Brm62q9v11dl05qfZfLw0jeT5Po8W2dxt/lg36kPaq83d9Y2cuF4+cDP3728+6JX73dvN7zvtaxdPZjye7F48Y9dXuyInu6KesSt38Q/bHRZPT0z7Lxi+ms3F+69V9lVezB45ns8eG58YStWnyjTB07RSfW0fXo5BLu+bnT242knntG/aNveu3a2V/jW4dfGwHZwMYL3tT0iE5jtmqpxJYvCzIZ2EqBZs1x1e7wcJyfLVE85KgKG2nbRrAOfFQ/ysfXjLLso9lDaTaPNUvsnH03x0+XjJTJvR5+MP+djmY8zHs9znRArQDsY7Zs6ZxjNZ3vWqHRr3WQfjPYmzTmhMZ92hMSjaReNlArOmj5Qy6x7NLIn2LZoZyppcQXN5xkYd6xkbdWzAQ1QP8O+Tegj0T9o/4CGph8C9JL2XSK6kuSLnZXWITuTtNG+SzaZVTfxe4yc89+o5MbbXsR25Bs3V0WfQPj25Bs3V43lQz703odX4fUSr575Da5whmSCLImvO2+l8aC168sk49BSTcSa4yWeAlOCmvIHaBa0d8UzwU95gySuLKmtyae2IjZ78B0ccr3EccbzGcfgRBrIe0NM8EBut/T1+ZFFmTS6tI+NM0HoxDq15A3mT5qVeQetFDLTmjfjv1H8kjoAuOjEPnc4DtQtau5Dw2atPahe0dsRAq8+OsUKj6J5cg+aiXkHrRQwTW83VJ7R6pl5R60UMtHoeoolW75c6Rq1jbFv0lJd46CkX8Ux0k+fYMtZNY4mH1rGwFpW1SO34/VONB2UtWjzIzima2kWtHfHQuvaEx8K1MFhYpo5wWHksXHtYKCxTU5isbGquzGPhWngsXAuDhWXqC4eVx6i5orCsY6mvl708a/oXxoXNwrWwWbhO7AmFZWoNn5XTpGM7fBbGO/rLTlyYLbwLp4Vx1gCsVmZ79Qane96pu+917MD9Ft6p9Z73gTWsjPON1vUj/CrvmdlW1yT7LdxWfuVHqTBb2Bdmra4x4bSwT91htTJb9gHhtLBPrWG1Mlv2AZ6j9uwLs4V9z9jCO09eQddPCPgp7Au/hXdqDcOVZa115rewL/xqfUPCZ9kHhN+yDyTusbBPfWG4slz2AeG3sN8Rv9P4wnKncTrusewD1Be2K+NaX+F6vyfA9X5PgOUw6FjqC897ruFZNfdY9gdqDduVca115lr3h8y17g/sDXVPoL6wXRm3U67MddkfqDVsV8bLXiFc5/2BH+3X+af7ZT6GfEz5J72TR6uvevj6+08PX7Qz59dcHlaee8lDzrcrX31lcTRvLnbbd8vVmkfwk7e/rV+cb7Z3y1ta57u76/W2tPkH9HTU/NnkT37GDN/+FP2f/hRJCdr/Gp1fsDNnduVv9/jKNB92V8ur1YZFxuT91YV/3T8bTLP8uF03i6NP",
        },
        {
            "url": "https://puzz.link/p?chocona/26/22/885kcco5lc912qccuksc8u9k8cdbs24ujt2ctre2ifbuagd77ah6bbjpubmjvt7n57t4gldt0oa6t0gi3uci41s4icrs32ar3j7cqhjpkk2lik3g3302fuitovkgv3g7tge73ifv7jejuc0r4v3ei4e1o79r01jpqune0kg1ov1f300bf783vukb00fg2mvvvggs0tvovs0g3frku1s0tg7v270064a13422432332444724242322633942221232249322222423462242621324325398321344611532442412253236225",
            "test": False,
        },
    ],
}
