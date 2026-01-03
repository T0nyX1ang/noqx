"""The Tatamibari solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, reverse_op, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region, avoid_edge_crossover


def tatamibari_cell_constraint(op: str, src_cell: Tuple[int, int]) -> str:
    """Generate a cell relevant constraint for tatamibari."""
    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
    rop = reverse_op(op)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {count_r}, {count_c}, CR {rop} CC."


class TamamibariSolver(Solver):
    """The Tatamibari solver."""

    name = "Tatamibari"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VRRb9MwEH7Pr5j8yiHZcdo6fkFltLyUDGjRNEVRlXaBVbTKSBqEXPLfdz6H1YQihCYGD8jNpy/fne0v557rT01eFRDjkAo4CBxScXpUZH+8G4vNflvoMxg3+5uyQgJwMZ3C+3xbF0HaZWXBwcTajMG81CkLGdAjWAbmjT6YV9okYOYYYiBQmyETDEKkkyO9pLhl504UHHnScaRXSNebar0tljOnvNapWQCz+zyn2ZayXfm5YG4ava/L3WpjhVW+x4+pbza3XaRursuPTZcrshbM2NmdnLArj3YtdXYt+1N2i+sPRd2sTnmNs7bFmr9Ft0udWuPvjlQd6VwfEBN9YKGyU7+iEXcwTHIrPPWE0ArPPCGywhNPGPbWGPQzhrSGl6FoF29R1Z+iyJiXITht46UI0Z8knNnvFMrxthbOrr+y7BdBROTvfh0slqCSXRFOCUPCBVYUjCR8QcgJB4QzypkQXhKeE0aEQ8oZ2TP5rVN7uB08M6xCrPDwRlggSwR2t4hHTEvksYCQY0D+0ncaKrom/DH4t5QsSNkEm+YsKatdvsXGSZrdqqi+veM11QbsC6MnlTgl+n9z/Y2by9afP3InPLQxUyztfe+AuQB22yzz5brE/xnWz4W7djodxlb8SWAU/RB49K/HDs+COw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(avoid_edge_crossover())
        self.add_program_line(f":- {{ top_left(R, C) }} != {len(puzzle.text)}.")

        all_src = []
        tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if clue == "+":
                self.add_program_line(tatamibari_cell_constraint("eq", (r, c)))
            elif clue == "-":
                self.add_program_line(tatamibari_cell_constraint("lt", (r, c)))
            elif clue == "|":
                self.add_program_line(tatamibari_cell_constraint("gt", (r, c)))

            all_src.append((r, c))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
