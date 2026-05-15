"""The KaitoRamma solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def straight_line() -> str:
    """Generate a straight line rule."""
    rule = f':- grid(R, C), grid(R + 1, C), edge(R, C, "{Direction.LEFT}"), not edge(R + 1, C, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), grid(R + 1, C), not edge(R, C, "{Direction.LEFT}"), edge(R + 1, C, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), grid(R, C + 1), edge(R, C, "{Direction.TOP}"), not edge(R, C + 1, "{Direction.TOP}").\n'
    rule += f':- grid(R, C), grid(R, C + 1), not edge(R, C, "{Direction.TOP}"), edge(R, C + 1, "{Direction.TOP}").\n'
    return rule


class KaitoRammaSolver(Solver):
    """The KaitoRamma solver."""

    name = "KaitoRamma"
    category = "region"
    aliases = ["kaitoramma"]
    examples = [
        {
            "data": "m=edit&p=7Vbva9s8EP6ev6LcZw10ku3Y/pZlyb6k6bZmlGJMcFOvNUvqLj+2twr533s6G8LwlUHLAi8MR5cnj06nR2edlM2PXbEuFWr/sbGib3oCjLmZOOKm22dWbZdleqYGu+19vSag1MV4rL4Vy03Zy1qvvLd3SeoGyn1MMzCguCHkyn1O9+48hUW9uqlAuUvqB4XUMSGEoAzB0RFecb9Hw4ZETXjaYoLXBBfVerEs55OG+ZRmbqbAT/aeR3sIq/pnCc0w/t0IIOJm+eu+5Ta72/r7rvXC/KDcgNW6kSDUHoV62Aj1SBDq9f81oUl+OFC+v5DUeZp51V+PMD7Cy3RPdsoW2V6ne7CWwiBN00g7Z2lgA2JNh41E31jyDcQIgY/QZcUIIUqzhUZkE4mNxLVFfWm2vtfb8e173y7r9XbYWFxFIsZNQolFraUQqMUYqMWFIIo5RhRThEae0ohLRCtmH61fTjcI75cuHfjXItByEN4y3Snl3YGhnJPI6xZoIbFUF2OuDsN2RsWjnGX7ga1mG7KdsM+I7RXbIduAbcQ+fV9+ry7Q18mBCOkFJjEdvCZUxlAO7R8lZrY5+n9/wv8fl/cyGN3elWfTer0qlnRoDuvVY72ptiXQ1XTowX/ALbP+pvt3W536tvK51ycuibdWaEZ5BYOGq0m5CwWPu3kxX9S0vyh5TbehP0uBfrH7LaOpol8c15R4p/vkGaQzBJ6qh3dPxcMd5L1n",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black"))
        self.add_program_line(defined(item="white"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(straight_line())
        self.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

        tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__1":
                self.add_program_line(f"white({r}, {c}).")
                self.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
                self.add_program_line(f":- {tag}({r}, {c}, R, C), black(R, C).")

            if symbol_name == "circle_M__2":
                self.add_program_line(f"black({r}, {c}).")
                self.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
                self.add_program_line(f":- {tag}({r}, {c}, R, C), white(R, C).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
