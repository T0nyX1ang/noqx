"""The Dominion solver."""

from typing import List, Tuple

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(":- grid(R, C), black(R, C), #count{ (R1, C1): adj_4(R, C, R1, C1), black(R1, C1) } != 1.")

    for (r, c), letter in puzzle.text.items():
        solver.add_program_line(f"not black({r}, {c}).")
        if letter != "?":
            solver.add_program_line(grid_src_color_connected((r, c), color="not black"))

    tag = tag_encode("reachable", "grid", "src", "adj", 4, "not black")
    for (r, c), letter in puzzle.text.items():
        for (r1, c1), letter1 in puzzle.text.items():
            if (r1, c1) == (r, c) or letter == "?" or letter1 == "?":
                continue
            if letter1 == letter:
                solver.add_program_line(f":- not {tag}({r}, {c}, {r1}, {c1}).")
            else:
                solver.add_program_line(f":- {tag}({r}, {c}, {r1}, {c1}).")

    solver.add_program_line(avoid_unknown_src(adj_type=4, color="not black"))

    solver.add_program_line(display())
    print(solver.program)
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Dominion",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VRNj5swEL3zKyqf54BtPn3LsqGXNO02qVYrhFYsZbWoidjyUVVG+e8ZD2hBKJce2uawsvz0eDO2n8dimp9dVhfAJXAfZAA2cByuFOAFDmoBTXsc+7I9FOoDrLr2paqRAHyOY3jODk1hJWNWavU6VPoO9EeVMM6ACZycpaDvVK8/Kb0FvcMQA47aZkgSSNcTvae4YdEgchv5duRIH5DmZZ0fisfNoHxRid4DM+fc0GpD2bH6VbDRh/nOq+NTaYSnrMXLNC/l6xhpuu/Vj27M5ekJ9Gqwu7tgV052DR3sGnbBrrnFX7YbpqcTlv0rGn5UifH+baLBRHeqR9yqnjncLI3Qy/A2zJVGuJ0EzzXCzST4lLGaCeEig9v+UuG0aHYO9+jk2TY8FItVQi7dCYdyZvaEHxglnimBt1RC2mc9KZLTPm8KVoNTTR4IY0JBuMeSgZaEt4Q2oUu4oZw14T1hROgQepTjm6L/0bP8AzuJ9OgfvzTc98g1R1IrYbuufs7yAptAVB1fq6ZsC4Yd92Sx34xmgq0cnPcm/J+asHkC+9r++Wuzg10otc4="
        },
        {
            "data": "m=edit&p=7ZRPj5swEMXvfIrKZx8wJlnwpUpIaA9p2i2pogihFUtZLWoitvypKiO+e2bGqJAqlx7aplLl+OXl54nzbGLXX9u0yrmw8SU9Du/QXOFRd7w5dXtou6I55uoVX7TNc1mB4fx9GPKn9FjnVjxUJVanfaXvuX6jYiYYZw50wRKu71Wn3ym95TqCIcYFsI0pcsCuR7uncXSBgcIGvx082APYrKiyY/6wMeSDivWOM/ydJX0bLTuV33I25MDPWXl6LBA8pg0spn4uXoaRuv1cfmmHWpH0XC9M3OhKXDnGRWviorsSF1fxm+P6Sd/Dtn+EwA8qxuyfRuuNNlId6FZ1TEr86gqymGfDpP8TmDsIghHcEXg7Al8gWIxA2FQymUTYLpLlhAgi4YQ4NM96QlxKN62ZUc3rCTH5LgjN/IPASgWt90AakjqkO9gOriXpitQmnZFuqGZNuicNSF3SOdXc4Yb+0pb/gTixNOf3ss3+PZZYMYva6inNcvi7B+XppayLJmdwt/QW+86oxxKvqv/XzV+6bvAR2Ld2Am4tDpzJxDoD",
        },
    ],
}
