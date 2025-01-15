"""The Simple Loop solver."""

from typing import List

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="black"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("simpleloop(R, C) :- grid(R, C), not black(R, C).")
    solver.add_program_line(fill_path(color="simpleloop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="simpleloop", adj_type="loop"))
    solver.add_program_line(single_loop(color="simpleloop"))

    for (r, c, _, _), color in puzzle.surface.items():
        fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
        solver.add_program_line(f"black({r}, {c}).")

    for (r, c, _, d), draw in puzzle.line.items():
        solver.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Simple Loop",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VZNb9pMEL7zK9Ce57Cf/rrRNPRCSd9CFUWWhRzqKFZNTQFXkRH/PbMzG3EoUSPlFZcis888OzPrnZ2VZ9j+6spNBVr6n0lAgsInThMaiVM0ZHjm9a6psiGMut1ju0ECcDMew0PZbKtBHryKwb5Ps34E/acsF1oADSUK6P/L9v3nrJ9BP0OTAIu6CTIlQCO9PtJbsnt2xUolkU8DR3qHdFlvlk21mLDmS5b3cxB+nw+02lOxan9XgpfRfNmu7muvuC93eJjtY70Olm33vf3RBV9VHKAfcbiTE+GaY7iecrienQjXn+Ld4Tb1z+rpVKRpcThgxr9irIss92F/O9LkSGfZXjgrMgvCJSQiTSJVJJSULJVjqdmsdJjblGUU5rFhmQR9GvQpz7Xk92rJfjq8T0e8jwl2I2OWhtcZF/QuYpm8SPazYZ01vJ91/F4b8T42Cn5x8It5vU348Dbl0zsZpGY/F+JzdF5M2DTbIyrCO8IxoSacY1ahN4QfCSWhI5yQzzXhLeEVoSWMyCf29/LGm3t/OHhPMR4MP2qBw9+RQZaC0pg2pCiRY4qQxxZ8kswbj5A7rhp/f9zF7+L37/kVg1zMus1Duaywgk+wkg+n7WZVNgJ75WEgngSNHL9A7DGX9nn29umzL89Wiv+fzpBjYkMph/4GxLpblItl2wj8BwZs5Or+ivWl4L9i5h5w2uhbyR+Ws6cHG4/Y1qt1Uw2btl2LYvAM",
        },
        {"url": "https://puzz.link/p?simpleloop/15/15/124000400000a0004g0002008h12000482008400004i1", "test": False},
    ],
}
