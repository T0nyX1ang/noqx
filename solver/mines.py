"""The Minesweeper solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent


class MinesSolver(Solver):
    """The Minesweeper solver."""

    name = "Minesweeper"
    category = "var"
    aliases = ["minesweeper"]
    examples = [
        {
            "data": "m=edit&p=7VRNj5swEL3zKyKffbCB5euWbje9pGzbpFpFCCGSugpqCCmEtnKU/74zA41BymG7UtNLZXn03sxgP88YN9/bvFY8gOEEXHAJw3FtmrYIaYp+LIvjTkUTPm2P26oGwPnjbMa/5rtGWUmflVonHUZ6yvW7KGGScWbDlCzl+mN00u8jHXO9gBDjEnzzLskG+GDgE8UR3XdOKQDHPQa4Argp6s1OZfPO8yFK9JIz3OcNfY2QldUPxXodyDdVuS7Qsc6PcJhmWxz6SNN+qb61fa5Mz1xPO7mrK3IdIxdhJxfRFbl4CpTbtPusrKr9q+SWxV4115SG6fkMFf8EWrMoQdmfDQwMXEQnsHF0YrYPn2KjqSnMCYBi1zvqijG1R8muO6IeRk2yh9EBHa/s476uoRi9u9AA97UvNMSVB9QZ7Rvit4NoCNS5UClwLbOTFLjYkI91SilHq0uJu/2OQ9Uk1W5FdkbWJruE0nLtkH1LVpC9IzunnAeyT2TvybpkPcrxsTl/1L6hHObjwV28EeZq/SWNie3R22AG9u6GPLUSFrflWtWTuKrLfAd/w2KbHxSDF+dssV+MJt0D9/8jdPtHCKsvXn2X/82vlUBhPYfrR84ObZZnmwquFVTmqh/KiX4/fLH/5qeF/7Tr0k+lDqpmqfUM",
            "config": {"mine_count": 10},
        },
        {
            "data": "m=edit&p=7VZLb9pAEL7zK6I972Efft9oGnqh9BGqCFkWAuoKVByndtxWRvz3zIxJ9yF6aA8Rh8h4NJ/n9e3Msnb7o1s1JZch/nTCBZdwRSKhWyaA4X6+5rvHfZld8XH3uK0bUDj/MJnwb6t9W47yk1cxOvRp1o95/y7LmWScKbglK3j/KTv077N+xvtbMDEu4dl0cFKg3hj1juyoXQ8PpQB9dtJBXYC62TWbfbmcDk8+Znk/5wzrvKFoVFlV/yzZiQfiTV2td/hgvXqExbTb3cPJ0nZf6+/dyVcWR96PB7qLM3S1oYvqQBe1M3RxFUi37e6XVV3f/xfdandftueYpsXxCB3/DFyXWY60vxg1MeptdgA5yw4sUBAKAx+GwoIIoDYwAYibYIChAKgM1E5smAIM/sDItUaY2bLGDowxc2Qg1jU0EiRpnBPMbKypa00x1tSVQjpmKQInWgp3yVK4taVEalY+icwtrDCfjd02SB26+bTHj1pu+QeY3/IPvfjQ7ZyM3NZJ6ntsYW99EdY3Q5Qx8rex5x9760nQ38YeXxoHHh3PGP3NHpKpt16alx2P9Qwf5c1PCXfHKpqHiVca/U09pbEfVj6ahxXvzUMFGG/6pwK3nypEu+UfuutR1F+LT+zuVuX1V8XuPJXXb5XgfG3s+afIx8qXevWo/7a/V5/6bdajhbuftHDnoaX9/4FTRNJZsiA5IalIzuGo4b0m+ZakIBmSnJLPDck7ktckA5IR+cR4WP3TcfYCdPJgeC3+7cJOvlov2lqMcjbrqnXZXM3qplrt4VV6u109lAw+V44j9pvRTZs8eP2CefkvGOy+uLQ//qXRgaNoaOOvsnwoG1aMngA=",
        },
    ]
    parameters = {"mine_count": {"name": "Mines", "type": "number", "default": ""}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="sun_moon__4"))
        self.add_program_line(adjacent(_type=8))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"not sun_moon__4({r}, {c}).")
            self.add_program_line(count_adjacent(int(num), (r, c), color="sun_moon__4", adj_type=8))

        mine_count = puzzle.param["mine_count"]
        if mine_count:
            fail_false(isinstance(mine_count, str) and mine_count.isdigit(), "Please provide a valid mine count.")
            self.add_program_line(count(int(mine_count), color="sun_moon__4", _type="grid"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(symbol_name, "sun_moon__4")
            self.add_program_line(f"sun_moon__4({r}, {c}).")

        self.add_program_line(display(item="sun_moon__4"))

        return self.program
