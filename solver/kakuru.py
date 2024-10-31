"""The Kakuru solver."""

from typing import List

from .core.common import display, grid
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line("{ number(R, C, (1..9)) } = 1 :- grid(R, C), not black(R, C).")
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(":- adj_8(R, C, R1, C1), number(R, C, N), number(R1, C1, N).")

    for (r, c), clue in puzzle.text.items():
        solver.add_program_line(f":- number(_, _, N), {{ grid(R, C): number(R, C, N), adj_8(R, C, {r}, {c}) }} > 1.")
        if clue != "?":
            assert isinstance(clue, int), "Clue should be integer or '?'."
            solver.add_program_line(f":- #sum {{ N: number(R, C, N), adj_8(R, C, {r}, {c}) }} != {clue}.")

    for (r, c), color_code in puzzle.surface.items():
        if color_code == 4:  # shaded color (BK)
            solver.add_program_line(f"black({r}, {c}).")

    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Kakuru",
    "category": "num",
    "examples": [
        {
            "data": "m=edit&p=7VRNj9owEL3nV6zm7EMSJyH4UtHt0gtNP6BaraxoFWhWiwpKG0hVGfHf9804KFD1sJe2e6icvHk8jzPPH3j3vavaWqVoOlehitDiOJc3Cfk5tcV6v6nNlZp0+8emBVHq/XSqHqrNrg5sn1UGBzc2bqLcW2MpIkUx3ohK5T6ag3tnXKHcHF2kEmgznxSD3gz0VvqZXXsxCsELzzPQO9DVul1t6vsZeqF8MNYtFHGd1zKaKW2bHzX1Pvj3qtku1ywsqz0ms3tcf+t7dt2X5mvX50blUbnJL3a5Sm9XD3aZervMfmOXZ/GH7Y7L4xHL/gmG741l758Hmg90bg4Uh2QSbErkQ+yD9iHxYSxBe1HnEhKfmYwkpH54mvnQiz4z9cMzLoSiBRdFuiWNvfNHQepays4EFLP06kzAVy4EtmNpfCagHKaP43VS2COU/EyBMyh8anqFnV98l81fCvJdrMWgiJdodFIwq8gcgHeCU8FYcIGVVk4LvhEMBVPBmeTcCN4KXgsmgpnkjHivnrmbfnn/gh0b+4uBW/o8VgaW5l37UK1qnNmi2y7r9qpo2m21IVwSx4B+krxWIz35f2/8o3uDtyB8aeftpdnBP6AMngA="
        },
        {
            "data": "m=edit&p=7VRNj9MwEL3nV6zm7EPiOEnrCyrLlksJHy1araxolZastqJVIG0QctX/vvMRcLdwQEjAHpDl8eubGftNxvXuc193jcpxpCMVqwSHznOeiTE842Es1vtNYy/UpN/ftx0CpV5Pp+qu3uyayA1RVXTwY+snyr+0DhJQoHEmUCn/1h78K+tL5efoAmWQm0mQRngV4DX7CV0KmcSIS8E5whuEq3W32jS3M/Qi88Y6v1BA5zznbIKwbb80MOig36t2u1wTsaz3WMzufv1p8Oz6D+3HfohNqqPykzO5dMogNw1yCYpcQj+RS1X8Ybnj6njEz/4OBd9aR9rfBzgKcG4PoDVYg00xsmSyFLykKS9GQoz4jPgyITPJy4TMc14K8RXiKySvoBA8tBwORaUGmyd3gc8/YzDNgaYGf2NwBwfPAkH6HKRxYEjq4yRSfRbD2yRFYKiWxzFUlgNzynDWOBBUKx51sg2VjRuPTpgfqqKPgUx6woic7wx+osQe0N6wnbLVbBfYNuVTti/YxmwztjOOuWJ7zfaSrWGbc0xBjf/FqyG9+gtynNb8zsjIfh9XkYN5393Vqwb/FmW/XTbdRdl223oD+A4dI/gKPF2K4eb/0/SPniZqQfzUbuFTk4P/iyp6AA=="
        },
    ],
}
