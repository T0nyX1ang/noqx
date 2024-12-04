"""The Dotchi-Loop solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import area, defined, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.loop import loop_straight, loop_turning, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def dotchi_constraint() -> str:
    """Generate a constraint for the Dotchi-Loop puzzle."""
    rule = "turning_area(A) :- area(A, R, C), white(R, C), turning(R, C).\n"
    rule += "straight_area(A) :- area(A, R, C), white(R, C), straight(R, C).\n"
    rule += ":- area(A, _, _), turning_area(A), straight_area(A)."
    return rule


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="white"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="dotchi"))
    solver.add_program_line(fill_path(color="dotchi"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="dotchi", adj_type="loop"))
    solver.add_program_line(single_loop(color="dotchi"))
    solver.add_program_line(loop_straight(color="dotchi"))
    solver.add_program_line(loop_turning(color="dotchi"))
    solver.add_program_line(dotchi_constraint())

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert d == Direction.CENTER, "The symbol should be placed in the center."
        if symbol_name == "circle_L__1":
            solver.add_program_line(f"white({r}, {c}).")
            solver.add_program_line(f"dotchi({r}, {c}).")
        if symbol_name == "circle_L__2":
            solver.add_program_line(f"not dotchi({r}, {c}).")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Dotchi-Loop",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VZdaxs7EH33rwh6VkEj7Yd239I06Ytv2tukhGBMcBz32tTppv64hDX+7zkzK+O0HriQQknhsl7t8UiaOXP0ufy+Hi0mlhz/QrT44skoyutjIa9Lz+VsNZ/UR/Z4vZo2CwBrP5yd2S+j+XLSG6RWw96mrer22Lbv64HxxspLZmjbv+tN+1fdXtv2AlXGEmx9IDLWA57u4ZXUMzrpjOSAzxMGvAYczxbj+eSm31k+1oP20hqO81Z6MzT3zb8T03WT/+Pm/nbGhtvRCsksp7OHVLNc3zVf16ktDbe2Pe7o9hW6YU+XYUeXkUKXs/hluvPZt8mjxrQabrdQ/BO43tQDpv15D+MeXtQblOdSkpTX9cYEghtCnOfcTAiqNVetpWbNMtVawOoPrFGz5l61Vpq1ULMoOIvDtszhoG2p8i3VttGpVtbhIFpkvgdtK+Z70LZS+Vaq6uRUEuRU1chxeopZzY+cOiBEemuvik9enUPk2fehOei8gzosFNR5RJkqIOlzkTJ1wChTZxjlepaFPgwFp/OTGSvuTNadl/ISy9K2Qcp3Ujopcyn70uYUK9RTZj2rBk6esB8HhBRcAoMVY4+9OkNMxsEBI2XBBIwJxDjz1ucQTjB85slnlgMjacY5/JfJfw6fZfJZom9MfXEeBJ59wPjaQF2s4Dxw1yZQsMFDX8EZcBcL9TYk/qi3Iev4ox64i4V64OQzIxvyjj/qgZN/8A87/nllPQ8D4wK582YgGLnzOAgGf94OBEO3IvUtkGORci/gZ5d7RN+Y+kbOPfWNAThpG6FhTNpGaPhMH8+bgWDEiilW5PM0xYqIVaVYFTjzhrDT0HWx8AXeaYt8XdLBVdA5aciHNqW+BK0oaUg8FuwHk+hKptKJlJmUhUyxks+FF58cL5vN/0lngNHnG8iPT/7n2Ya9genjzD46bxb3ozlO7tO7f579u5iOHiYGd6VtzzwaeQeBr17/X59+//WJ1XevbSm8NjpYnOauWY2nszfzpnkww94T",
        },
    ],
}
