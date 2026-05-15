"""The FiveCells solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape


class FiveCellsSolver(Solver):
    """The FiveCells solver."""

    name = "FiveCells"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7Vbfb9owEH7nr6j87Af77CR2Xqauo3vp6LYyVVWEEKXZigZKB2Wagvjfd3YSoGesaapW7aEKOX3cr3y+c85Z/VhPliWXifspwwWXeKXC+Fsa4e/uGs4e52V+wk/Xj/fVEgHnl+fn/Otkvip7Res16m1qm9envH6fFwwY97dkI15/yjf1h7we8PoKTYxL1F0gkowDwv4eXnu7Q2eNUgrEgxYjvEE4nS2n83J80Wg+5kU95Mw9562PdpAtqp8la8L8/2m1uJ05xe3kERezup89tJbV+q76vmbdI7a8Pm3o9o/QVXu6akdX/Uu684fqGFE72m6x4J+R6jgvHOsve2j28CrfbB2jDUtFt8amKyyVrGnUTgFUoZxCHSi0U4gDRUI9UvqUjHoY6mGJRyYIj4wyzSjTzBKFlSSpNcRDSloQKSlXCZb6KLpAqYM8WgYaoJm1ony0DjSGRiW03jKh1ZNB12TTg0M+maY+WVAf49f15lADpP3SpDSPDZ5uaVVB0OaASMjTQdKKgaSVh6ZfT6Lo5gJJdwYA3V4AtBqgAoZNvw7WDomgmjTgHOxtMHQvg6FdBhNwtgFnS/cYWPpSQNALsPQFBkt3FNigzmEHbVBnS1eqxFPOOIakH0Y3Xp57CV4OcVbxWnn5zkvhZeLlhffpe3nt5ZmX2svU+2Ru2v3VPHw+HZa598oanD7uNXDAmKQBVugW6NZkE9WCtPNxU8wD2+aRQrbeUuo96qyQ6h1qc0gFe9RFKAU7pDqU7axZm0+LjGsXpP5Y2EI3HwixK3m1/u/WUa9g/btv5cmgWi4mc/ymGKwXt+Wy+4+fb9se+8X8XSgM0a9fdC/+ReeKL154jj13rBZYVxyFvL7k7GE9noynFW4vLJszuEEWtURicJweN+B4jeTC0XjcgoM4GhJJZqOMcdhGQmK53FSOhNhYxXBURyx4PERjItnw2ImFKIiEZBGDO06OW3ZnSWB+8b2Kh9Wo9xs=",
        },
        {
            "url": "https://puzz.link/p?fivecells/10/10/a32213a32a1h22c31a3b3a3d3a23a2b2a2a23a1a1b2a22a2d2a3b3a31c11h3a22a21321a",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row * puzzle.col % 5 == 0, "It's impossible to divide grid into regions of this size!")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))

        for i, o_shape in enumerate(OMINOES[5].values()):
            self.add_program_line(general_shape("omino_5", i, o_shape, color="grid", adj_type="edge"))

        self.add_program_line(all_shapes("omino_5", color="grid"))
        self.add_program_line(count_shape(target=puzzle.row * puzzle.col // 5, name="omino_5", color="grid"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent_edges(num, (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
