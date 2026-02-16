"""The Key West solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, fill_line, fill_num, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent
from noqx.rule.reachable import grid_color_connected


def keywest_rule(color: str = "black") -> str:
    """Generate a rule to ensure the keywest constraints are met."""
    rule = f"number(R, C, 0) :- {color}(R, C).\n"
    rule += ":- number(R, C, N), #count { D: line_io(R, C, D) } != N.\n"
    rule += f':- grid(R, C), line_io(R, C, "{Direction.LEFT}"), not line_io(R, C - 1, "{Direction.RIGHT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.TOP}"), not line_io(R - 1, C, "{Direction.BOTTOM}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.RIGHT}"), not line_io(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.BOTTOM}"), not line_io(R + 1, C, "{Direction.TOP}").'
    return rule


class KeyWestSolver(Solver):
    """The Key West solver."""

    name = "Key West"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7Vbfb9pIEH7nr6j2tSudf/+S7oFQ6LVHCGlBXLAQMsQQp3acMzbpGfG/d3YcwnowUU9X9e7hZBjNfmPPt7Pe+dabP4sgC7kNl+5whatw6YqBf0sRv8M1ivI49N7wdpHfpRk4nF/1enwVxJuQf7y563fS9tO79h9bJ59O1fdK8UGZ3Pfu335Kfv8Q6ZnaGzjDy+FlpK3bv3Uurq3uW2tYbMZ5uL1O1Iv78XS0Gk7WrvZXdzA1yumVYn6crn7Ztse/tvznOcxau9L1yjYv33s+0xlnGv5nvLz2duWlVw54+RlCjKszzpIizqNlGqcZO2BlHzyVcQ3c7tGdYFx4nQpUFfAHlW+BewPuMsqWcTjvV4mGnl+OOBPcF/i0cFmSbkNBBo/heJkmi0gAiyCH5dvcRY+M6xDYFLfpl+L5VnW252W7qqD/nRVAkkMFwq0qEN6/UoE72+/h5XyCGuaeL8oZH13n6H72dmAH3o5pRlWSxeF5SKeZZGw9p34BbHKDQ8ZufawrZIwEsGleAGSQxoRAJwQ6EkgzMpABtuALoNafMAiDgQyKBBAKg9RgkhpMQmBqJKFJajAJgUkILCSQEliEwUIGaayTMRJIi2IRBpuUYBMCmxDYSCDNyCYbxSYEDhIYEoAM0ot2CIVDanAIg4M7RXqvLqnBJTW4hMAlBC4SSIvkks3u1jYKdIiKfXKDtodWQzuCNuKljvYdWgWtibaP93TRTtB20BpoLbzHFo34t1r1n0wHuhY2iOuIdoX3JhxDOTgqLCuG4LiBBdFFj3LRM5Un+lP/znp8yCGOrsNl/vjRrOWzfvQQvhmkWRLEII+DIlmE2WEMhxPbpPF8U2SrYBnOw6/BMmdedT7KkRr2gDlqUJymjzEQNWQ4hGpgtH5Is7AxJMDwdn0ulQg1pFqk2S2Z01MQx/Va8LuhBlWnSw3KMzg6pHGQZelTDUmC/K4GSMdMLVP4QBYzD+pTDL4EhC05Lse+xb4y/Ps618TL/P9L4j/8JSFelPLTROrHaKYPCw5qx8srzh6LeTCH1WbwzcpFAESvOQCyeOYJVWkOPMvlmWCloOeDIKonwZ++kNidafaKVB6DFG4QTEBf0Uwp2oSfkUcpSvETLRSTPZVDQBsUEVAqigCd6iKAJ9II2Bl1FFmpQIpZUY0UVCcyKahkpfRnrW8=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_num(_range=range(1, 5), color="black"))
        self.add_program_line(fill_line(color="not black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_same_number_adjacent(adj_type=4))
        self.add_program_line(grid_color_connected(color="not black", adj_type="line"))
        self.add_program_line(keywest_rule())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if isinstance(num, int) and num > 0:
                self.add_program_line(f"not black({r}, {c}).")
                self.add_program_line(f":- not number({r}, {c}, {num}).")

            if isinstance(num, int) and num == 0:
                self.add_program_line(f"black({r}, {c}).")
                self.add_program_line(f"number({r}, {c}, 0).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="number", size=3))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
