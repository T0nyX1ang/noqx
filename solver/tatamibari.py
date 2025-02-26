"""The Tatamibari solver."""

from typing import Tuple

from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, reverse_op, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region, avoid_region_border_crossover
from noqx.solution import solver


def tatamibari_cell_constraint(op: str, src_cell: Tuple[int, int]) -> str:
    """Generate a cell relevant constraint for tatamibari."""
    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
    rop = reverse_op(op)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {count_r}, {count_c}, CR {rop} CC."


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    fail_false(len(puzzle.text) > 0, "No clues found.")
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_rect_region())
    solver.add_program_line(f":- {{ upleft(R, C) }} != {len(puzzle.text)}.")

    for (r, c, d, pos), clue in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        solver.add_program_line(f"clue({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

        if clue == "+":
            solver.add_program_line(tatamibari_cell_constraint("eq", (r, c)))
        elif clue == "-":
            solver.add_program_line(tatamibari_cell_constraint("lt", (r, c)))
        elif clue == "|":
            solver.add_program_line(tatamibari_cell_constraint("gt", (r, c)))

    for (r, c, d, _), draw in puzzle.edge.items():
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
    solver.add_program_line(f":- clue(R, C), clue(R, C), (R, C) != (R1, C1), {tag}(R, C, R, C1), {tag}(R1, C1, R, C1).")
    solver.add_program_line(avoid_region_border_crossover())
    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))

    return solver.program


__metadata__ = {
    "name": "Tatamibari",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VRRb9MwEH7Pr5j8yiHZcdo6fkFltLyUDGjRNEVRlXaBVbTKSBqEXPLfdz6H1YQihCYGD8jNpy/fne0v557rT01eFRDjkAo4CBxScXpUZH+8G4vNflvoMxg3+5uyQgJwMZ3C+3xbF0HaZWXBwcTajMG81CkLGdAjWAbmjT6YV9okYOYYYiBQmyETDEKkkyO9pLhl504UHHnScaRXSNebar0tljOnvNapWQCz+zyn2ZayXfm5YG4ava/L3WpjhVW+x4+pbza3XaRursuPTZcrshbM2NmdnLArj3YtdXYt+1N2i+sPRd2sTnmNs7bFmr9Ft0udWuPvjlQd6VwfEBN9YKGyU7+iEXcwTHIrPPWE0ArPPCGywhNPGPbWGPQzhrSGl6FoF29R1Z+iyJiXITht46UI0Z8knNnvFMrxthbOrr+y7BdBROTvfh0slqCSXRFOCUPCBVYUjCR8QcgJB4QzypkQXhKeE0aEQ8oZ2TP5rVN7uB08M6xCrPDwRlggSwR2t4hHTEvksYCQY0D+0ncaKrom/DH4t5QsSNkEm+YsKatdvsXGSZrdqqi+veM11QbsC6MnlTgl+n9z/Y2by9afP3InPLQxUyztfe+AuQB22yzz5brE/xnWz4W7djodxlb8SWAU/RB49K/HDs+COw==",
        }
    ],
}
