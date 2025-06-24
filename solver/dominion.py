"""The Dominion solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected
from noqx.rule.variety import nori_adjacent


class DominionSolver(Solver):
    """The Dominion solver."""

    name = "Dominion"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VRNj5swEL3zKyqf54BtPn3LsqGXNO02qVYrhFYsZbWoidjyUVVG+e8ZD2hBKJce2uawsvz0eDO2n8dimp9dVhfAJXAfZAA2cByuFOAFDmoBTXsc+7I9FOoDrLr2paqRAHyOY3jODk1hJWNWavU6VPoO9EeVMM6ACZycpaDvVK8/Kb0FvcMQA47aZkgSSNcTvae4YdEgchv5duRIH5DmZZ0fisfNoHxRid4DM+fc0GpD2bH6VbDRh/nOq+NTaYSnrMXLNC/l6xhpuu/Vj27M5ekJ9Gqwu7tgV052DR3sGnbBrrnFX7YbpqcTlv0rGn5UifH+baLBRHeqR9yqnjncLI3Qy/A2zJVGuJ0EzzXCzST4lLGaCeEig9v+UuG0aHYO9+jk2TY8FItVQi7dCYdyZvaEHxglnimBt1RC2mc9KZLTPm8KVoNTTR4IY0JBuMeSgZaEt4Q2oUu4oZw14T1hROgQepTjm6L/0bP8AzuJ9OgfvzTc98g1R1IrYbuufs7yAptAVB1fq6ZsC4Yd92Sx34xmgq0cnPcm/J+asHkC+9r++Wuzg10otc4=",
            "test": False,
        },
        {
            "data": "m=edit&p=7ZRfb9owFMXf8ymq++wHOw4U/DIFSrYHlv0JU1VZURWyVI0GyhZINRnx3XvvdbSkUx/2sq2TJuPD4eeLOXawD9+6oq2EkvTSM4Hv2CI14x7Optxl3zb1cVeZCxF3x/umRSPEuyQRd8XuUAW2r8qDk5sbFwv32lhQICDEriAX7oM5ubfGpcJlOAQiQrb2RSHa1WCveZzc0kMl0ae9R3uDtqzbclfdrj15b6zbCKDfWfC3ycK+eaigz0Gfy2a/rQlsiyMu5nBff+1HDt3n5kvX16r8LFzs42bPxNVDXLI+Lrln4tIqfnPceX4+47Z/xMC3xlL2T4OdDTYzJ9ASTCRAKzAhopSQpnmuMJh/UKDnP4FpSGA5gEsGbwYwx/ksxANQkktGkygZEVmMiGKSjEjI86xGJOJ045oJ17waEZ/vCeGZfxBcqTIn1BvWhDVk3eDeCKdZr1gl64R1zTUr1mvWJWvEOuWaS9rdX9x/v+V/II7V/jA/bZN/j+WBhaxr74qywv9+2u23VXuRNu2+2AFeNucAvgN3q+nu+n///KX7hx6BfGmn4KXFwXOZB48=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(nori_adjacent(color="black"))
        self.add_program_line(avoid_unknown_src(adj_type=4, color="not black"))

        tag = tag_encode("reachable", "grid", "src", "adj", 4, "not black")
        for (r, c, d, label), letter in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            if letter != "?":
                self.add_program_line(grid_src_color_connected((r, c), color="not black"))

            for (r1, c1, _, _), letter1 in puzzle.text.items():
                if (r1, c1) == (r, c) or letter == "?" or letter1 == "?":
                    continue
                if letter1 == letter:
                    self.add_program_line(f":- not {tag}({r}, {c}, {r1}, {c1}).")
                else:
                    self.add_program_line(f":- {tag}({r}, {c}, {r1}, {c1}).")

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display())

        return self.program
