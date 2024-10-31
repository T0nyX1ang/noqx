"""The sun_moon__4__0sweeper solver."""

from typing import List

from .core.common import count, display, grid, shade_c
from .core.neighbor import adjacent, count_adjacent
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    mine_count = puzzle.param["mine_count"]

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="sun_moon__4__0"))
    solver.add_program_line(adjacent(_type=8))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"sun_moon__4__0({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not sun_moon__4__0({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(f"not sun_moon__4__0({r}, {c}).")
        solver.add_program_line(count_adjacent(num, (r, c), color="sun_moon__4__0", adj_type=8))

    if mine_count:
        assert isinstance(mine_count, str) and mine_count.isdigit(), "Please provide a valid mine count."
        solver.add_program_line(count(int(mine_count), color="sun_moon__4__0", _type="grid"))

    solver.add_program_line(display(item="sun_moon__4__0"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Minesweeper",
    "category": "var",
    "aliases": ["minesweeper"],
    "examples": [
        {
            "data": "m=edit&p=7VTBjpswEL3zFSuffbANS8C3dLvpJcu2TapVhBAiqaughpBCaCtH+fedGWgAKVLVHqIeKstP73nG9ssMcf2tySrDAxhuwAWXMFxP0VQipCm6scyPO6Pv+LQ5bssKCOfPsxn/ku1q48RdVuKcbKjtlNt3OmaScaZgSpZw+0Gf7JO2EbcLCDEuYW3eJimgjz19oTiyh3ZRCuBRx4GugG7yarMz6bxdea9ju+QM73lDu5GyovxuWOcD9aYs1jkurLMj/Jh6mx+6SN18Lr82Xa5MztxOW7urK3bd3i7S1i6yK3bxV6DdutmnRVnu/8puke9Nfc1pmJzPUPGP4DXVMdr+1NOgpwt9Aoz0iakJbMVGU1OYG4DErrfSE2OpRsmeN5I+RvtkH6MDOT55gvd6vcTo/UUGeK+6yBBPHkh3dG+IewfREKR7kVLgWf1NUuBhQz32KaUcnS4l3vYrDlWTVLsV4YxQES6htNy6hG8JBeE94ZxyHglfCB8IPUKfcibYnD9q3w3sxMqnZ6Af2KYb6sSJWdQUa1PdRWVVZDv48Bfb7GAYPC5nh/1kNKnl3v/35vbvDVZf/Guf7W/sxFBY3+X2mbNDk2bppoTPCipzdV0kN3cP/7u26j+MOZiKJc4r",
            "config": {"mine_count": 10},
        },
        {
            "data": "m=edit&p=7VZLb9pAEL7zK6I972Efft9oGnqh9BGqCFkWAuoKVByndtxWRvz3zIxJ9yF6aA8Rh8h4NJ/n9e3Msnb7o1s1JZch/nTCBZdwRSKhWyaA4X6+5rvHfZld8XH3uK0bUDj/MJnwb6t9W47yk1cxOvRp1o95/y7LmWScKbglK3j/KTv077N+xvtbMDEu4dl0cFKg3hj1juyoXQ8PpQB9dtJBXYC62TWbfbmcDk8+Znk/5wzrvKFoVFlV/yzZiQfiTV2td/hgvXqExbTb3cPJ0nZf6+/dyVcWR96PB7qLM3S1oYvqQBe1M3RxFUi37e6XVV3f/xfdandftueYpsXxCB3/DFyXWY60vxg1MeptdgA5yw4sUBAKAx+GwoIIoDYwAYibYIChAKgM1E5smAIM/sDItUaY2bLGDowxc2Qg1jU0EiRpnBPMbKypa00x1tSVQjpmKQInWgp3yVK4taVEalY+icwtrDCfjd02SB26+bTHj1pu+QeY3/IPvfjQ7ZyM3NZJ6ntsYW99EdY3Q5Qx8rex5x9760nQ38YeXxoHHh3PGP3NHpKpt16alx2P9Qwf5c1PCXfHKpqHiVca/U09pbEfVj6ahxXvzUMFGG/6pwK3nypEu+UfuutR1F+LT+zuVuX1V8XuPJXXb5XgfG3s+afIx8qXevWo/7a/V5/6bdajhbuftHDnoaX9/4FTRNJZsiA5IalIzuGo4b0m+ZakIBmSnJLPDck7ktckA5IR+cR4WP3TcfYCdPJgeC3+7cJOvlov2lqMcjbrqnXZXM3qplrt4VV6u109lAw+V44j9pvRTZs8eP2CefkvGOy+uLQ//qXRgaNoaOOvsnwoG1aMngA=",
        },
    ],
    "parameters": {"mine_count": {"name": "Mines", "type": "number", "default": ""}},
}
