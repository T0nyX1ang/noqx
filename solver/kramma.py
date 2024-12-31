"""The KaitoRamma solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected
from noqx.solution import solver


def straight_line() -> str:
    """Generate a straight line rule."""
    rule = ":- grid(R, C), grid(R + 1, C), edge_left(R, C), not edge_left(R + 1, C).\n"
    rule += ":- grid(R, C), grid(R + 1, C), not edge_left(R, C), edge_left(R + 1, C).\n"
    rule += ":- grid(R, C), grid(R, C + 1), edge_top(R, C), not edge_top(R, C + 1).\n"
    rule += ":- grid(R, C), grid(R, C + 1), not edge_top(R, C), edge_top(R, C + 1).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="black"))
    solver.add_program_line(defined(item="white"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(straight_line())
    solver.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.CENTER, "The symbol should be placed in the center."
        if symbol_name == "circle_M__1":
            solver.add_program_line(f"white({r}, {c}).")
            solver.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
            solver.add_program_line(f":- {tag}({r}, {c}, R, C), black(R, C).")

        if symbol_name == "circle_M__2":
            solver.add_program_line(f"black({r}, {c}).")
            solver.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
            solver.add_program_line(f":- {tag}({r}, {c}, R, C), white(R, C).")

    for r, c, d in puzzle.edge:
        solver.add_program_line(f":- not edge_{d.value}({r}, {c}).")

    for r, c, d in puzzle.helper_x:
        solver.add_program_line(f":- edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "KaitoRamma",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7Vbva9s8EP6ev6LcZw10ku3Y/pZlyb6k6bZmlGJMcFOvNUvqLj+2twr533s6G8LwlUHLAi8MR5cnj06nR2edlM2PXbEuFWr/sbGib3oCjLmZOOKm22dWbZdleqYGu+19vSag1MV4rL4Vy03Zy1qvvLd3SeoGyn1MMzCguCHkyn1O9+48hUW9uqlAuUvqB4XUMSGEoAzB0RFecb9Hw4ZETXjaYoLXBBfVerEs55OG+ZRmbqbAT/aeR3sIq/pnCc0w/t0IIOJm+eu+5Ta72/r7rvXC/KDcgNW6kSDUHoV62Aj1SBDq9f81oUl+OFC+v5DUeZp51V+PMD7Cy3RPdsoW2V6ne7CWwiBN00g7Z2lgA2JNh41E31jyDcQIgY/QZcUIIUqzhUZkE4mNxLVFfWm2vtfb8e173y7r9XbYWFxFIsZNQolFraUQqMUYqMWFIIo5RhRThEae0ohLRCtmH61fTjcI75cuHfjXItByEN4y3Snl3YGhnJPI6xZoIbFUF2OuDsN2RsWjnGX7ga1mG7KdsM+I7RXbIduAbcQ+fV9+ry7Q18mBCOkFJjEdvCZUxlAO7R8lZrY5+n9/wv8fl/cyGN3elWfTer0qlnRoDuvVY72ptiXQ1XTowX/ALbP+pvt3W536tvK51ycuibdWaEZ5BYOGq0m5CwWPu3kxX9S0vyh5TbehP0uBfrH7LaOpol8c15R4p/vkGaQzBJ6qh3dPxcMd5L1n",
        }
    ],
}
