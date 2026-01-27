"""The Nibun-nogo solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_covering
from noqx.rule.reachable import grid_branch_color_connected


def constrain_branch_size(max_size: int, adj_type: int = 4, color: str = "gray") -> str:
    """Constrain the size of branches."""
    tag = tag_encode("reachable", "grid", "branch", "adj", adj_type, color)
    return f":- grid(R0, C0), {color}(R0, C0), #count {{ R, C: {tag}(R0, C0, R, C) }} > {max_size}."


class NibunNogoSolver(Solver):
    """The Nibun-nogo solver."""

    name = "Nibun-nogo"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZbfT/pIEMDf+SvMvrrJ9RdYmtwDInp6WFEgfKUhpGCBaku9pUWvxP/d2WmRtrt6d8mduUsu0GH4zOzuzGw7281vics8qir8q5sUfuFjqCZemtnAS8k/Az8OPOuItpJ4FTFQKL2x6cINNh69ul9121Hr5az1Y2vG47F6oSSXyujx/PH4Lvz10teZem6bveveta8tW7+0T28bneNGL9kMY297G6qnj8PxYNEbLZva7x17bKTjG6V+NV78tG0Nf645eQiT2i5tWmmLpheWQ1RCiQaXSiY0vbV26bWV2jTtg4lQE1g3c9JA7RzUEdq51s6gqoBuZ3oD1HtQ5z6bB960mzn2LCcdUMLXOcXRXCVhtPVIHgf/P4/Cmc/BzI2hUpuV/5xbNslD9JTkviofmgSxP4+CiHHI2RtNW1kK/X0KfOU8Bf2QAlezFLgmSYEPK6cAK/69KTTlKbzB9txBElPL4fkMD6p5UPvWDqRt7Yimq3yoAmOzTQRicAKb+kEM9DGKRK/61Bv70u5JQxNIszrKFHxMnEcvkpOqTxPjKRBdRZ9ChLpuVvLSDcyrOMrAtQrx6HXBJ8vrYx4om4rFu/8oHhhKd2peQRFjGSWY11LEuLCIsaoSzEsrYqyvBMvnxkqLGMst4KzmIsbCixirL8HSSLJ9kGCJN+zFOe6IhnIAdzhNdZRnKBWUdZRd9OmgHKFsozRQNtDnhD8jf/IpIrpCLJMXg1ha9kgV75B/KDZHzw6J8qf+32OTmkP6CVu4cw9anJ2EM48d2REL3YDAOUM2UTDdZPap9+rOY2JlR13RQqyYJTla4xQlryCKngN/LZtgbypBf7mOmCc1ceg9LD+bipskU80i9lCJ6cUNgnIq+BJQQtk9XkIxg3Oh8N9lLHopkdCNVyVQOENKM3nrSi1jtxyi++RWVgsP5XirkVeCl6NRDd5QYCf/fyv4V78V8M1S/tK7wTc0sj8Ix4GKQ6tLbyh5TqbuFHLCIiJXK1yffHv0+FhE7IsWdTBWsaRTAf2iWRWsMv5JXypYq1xoQjxYsQ8BlbQioNVuBEhsSACFngTsk7bEZ612Jh5VtTnxpYT+xJcqtihnUnsH",
        },
        {"url": "https://pzplus.tck.mn/p.html?nibunnogo/10/10/i16ai3ch22aidj7cjch6bmce53drbg6ddibch2dagcib", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_branch_color_connected(color="gray"))
        self.add_program_line(grid_branch_color_connected(color="not gray"))
        self.add_program_line(constrain_branch_size(max_size=5, color="gray"))
        self.add_program_line(constrain_branch_size(max_size=5, color="not gray"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_covering(num, (r, c), Direction.TOP_LEFT, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
