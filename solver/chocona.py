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
            "data": "m=edit&p=7ZfPbhs3EIfvfopgzzws/+6uLoWb2r04Tlu7CAJBMGRHaYzaUCJbRbGG3z3fcIdiVBhNg6LpJZC0+pFLzsxy+I2ouw/b5WZlrJe3701rLK/oXf7YEPKn1df59f3NavbMHG7v3603CGNeHh+bt8ubu9XBXEctDh7GYTYemvHH2byxjWkcH9sszPjz7GF8MRuPzHjGrcb09J1MgxzyqMpX+b6o51OnbdGnqpGvkVfXm6ub1cXJ1PPTbD6em0b8fJ9ni2xu13+sGo1D2lfr28tr6bhc3vMwd++u3+udu+2b9e9bHWsXj2Y8nMI9eyJcX8MVOYUr6olw5Sn+43CHxeMjy/4LAV/M5hL7r1X2VZ7NHriezh4an5hK1qfMNMHTtJJ9be/fjkFu75qd3bvbyeC0a9o2j67DrZXx1bh1cb8dnExgv+06xELzHStVepIE+MmUTkzUEGzX7d/vBzHJ9tUOZ8XAUNtO2tWA8xJD/KS9/8guyjOUNoto81K+ztfjfHX5es5Km9Hn6w/52uZrzNeTPOZIEtAOxjtWzpnGs1je9aodmuizDsZ7HGed0ASddYcmQNEuGi8LmDVjJJVZ92hWSbRv0axQ1vgK6sszN+pcz9yocwMxRI0B/n3SGALjk44PxJA0hsCzJH2WiK+kviL9sjtEJ/x26jdJsWlVY79X+4mYe405MbfXuR2+BvXVMWbQMT2+BvXVE/OgMffehFbt9xGtMfcdWu0MyQTZFFnTb6f+0Fr0FCfz0JNN5pngpjgDpAQ3+Q3kLmjusGeCn/wGi1/ZVFnjS3OHbfQUf3DY8WrHYcerHUc8wkDWA3paB2yjdbwnHtmUWeNL88g8EzRfzEOr34DfpH7JV9B8YQOtfiPxdxp/xI6ALjqxDp2uA7kLmruQiLPXOMld0NxhA61xdswVGkX3+BrUF/kKmi9smNiqrz6hNWbyFTVf2EBrzEM00erzkseoeYxti578Yg89+cKeiW6KObbMddNc7KF1LqxFZS2SO37/VBODshYtMUjlFE3uouYOe2jde8Jj4VoYLCyTRzisPBauPSwUlskpTFY21VfmsXAtPBauhcHCMvmFw8pjVF9RWNa55NdLLc+a8YVxYbNwLWwWrhM1obBMruGzcpp0bkechfGO8VKJC7OFd+G0MM4egNXKbK+xwemOd/Lue5078LyFd3K9431gDyvjfKN1/wi/yntmttU9Sb2F28qv/CgVZgv7wqzVPSacFvbJO6xWZksdEE4L++QaViuzpQ5wjtqxL8wW9j1zC++cvILunxCIp7Av/BbeyTUMV5Y115nfwr7wq/kNiThLHRB+Sx1IPGNhn/zCcGW51AHht7DfYb9T+8Jyp3Y6nrHUAfIL25Vxza9wvasJcL2rCbAcBp1LfuF5xzU8q+YZS30g17BdGddcZ661PmSutT5QG2pNIL+wXRm3k6/MdakP5Bq2K+OlVgjXuT7wo/0q/3Q/z9eQryn/pHdytPqHh698kOqnA5TY5CT2748Sn41tzk+7nFyeesmJ59udL76zOJg3Z9vN2+XVivP40ZvfVs9O15vb5Q2t0+3t5WpT2vwdejxo/mzyJx84w7d/SP/TPyRJQftF/5O+Ap2fCWfO6sp/8PGlad5vL5YXV2s2GYv3tzc4vD3ZTzH/a/9Xf14KUrP8sFk1i4OP",
        },
        {
            "url": "https://puzz.link/p?chocona/26/22/885kcco5lc912qccuksc8u9k8cdbs24ujt2ctre2ifbuagd77ah6bbjpubmjvt7n57t4gldt0oa6t0gi3uci41s4icrs32ar3j7cqhjpkk2lik3g3302fuitovkgv3g7tge73ifv7jejuc0r4v3ei4e1o79r01jpqune0kg1ov1f300bf783vukb00fg2mvvvggs0tvovs0g3frku1s0tg7v270064a13422432332444724242322633942221232249322222423462242621324325398321344611532442412253236225",
            "test": False,
        },
    ],
}
