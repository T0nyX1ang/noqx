"""The Araf solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def araf_region_clue_count(src_cell: Tuple[int, int]) -> str:
    """Generates a constraint for counting the number of clues in a row / col."""
    src_r, src_c = src_cell
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    rule = (
        f"araf_link({src_r}, {src_c}, R, C) :- {tag}({src_r}, {src_c}, R, C), clue(R, C, _), (R, C) != ({src_r}, {src_c}).\n"
    )
    rule += f":- #count {{ R1, C1 : araf_link({src_r}, {src_c}, R1, C1) }} != 1."
    return rule


def araf_region_count(src_cell: Tuple[int, int]) -> str:
    """Generates a constraint for counting the number of cells in an araf area."""
    src_r, src_c = src_cell
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    cnt_area = f"N = #count {{ R0, C0: {tag}({src_r}, {src_c}, R0, C0) }}, (N - N1) * (N - N2) >= 0"
    rule = f":- araf_link({src_r}, {src_c}, R, C), clue({src_r}, {src_c}, N1), clue(R, C, N2), {cnt_area}."
    return rule


class ArafSolver(Solver):
    """The Araf solver."""

    name = "Araf"
    category = "region"
    aliases = ["araf"]
    examples = [
        {
            "data": "m=edit&p=7VTBjtowEL3zFSuf5+Cxk+DkRrfQC2XbLqvVKooQsGkXFZQtkKoK4t87noSGaaFVtdW2h8pk9F6eHT+bmdl8KqfrHGIa1oEGpGGd5scF/qebMV5sl3lyAb1y+1CsCQBcDQbwfrrc5J20mZV1dlWcVD2oXiWpMgr4QZVB9TbZVa+TagTVNUkKkN4NCaECQ7DfwlvWPbqsX6ImPKpxRPCO4Hyxni/zybD+0Jskrcag/D4veLWHalV8zlW9jPm8WM0W/sVsuqXDbB4Wj42yKe+Lj2UzF7M9VL3abv+EXdvYDWpY27Wn7Zo/YTe//5Bvytkpr3G239OdvyO3kyT1xm9a6Fp4nez23tROGUdLA4jqv0WZWFCLRKOWGqlaSUOi2NJIqIGfHLe0K2gYELUtDSWVJiPpKjJi3ygWtCv3dVpSKzZygVS9jbClTnw5DoQr1FrIqCNhE7U8BaL33T3igVxv/PfMETfCHJrv58sLRysPg/yHhEfcHemUDshJccdxwNFwHFPOQGU5vuSoOYYchzynz/GW4yXHgGPEc7o+634rL59uh/KPzhs7Oh21LYwp3yzlt47BoK4xasLYYmMZo3NgNDa4S9jP/+XxUuO4Xx6P8N96k3VS1afucTEq1qvpkjrIqFzN8vWBU7/ed9QXxQ+VBULwv4X/jRbu718/c8E8tX5TutpvtQbVFajHcjKdzAvKM7o/lg/ld05uKvJnMhXpGflQt2flupRPy9QtfhCe/YKpiWSdrw==",
        },
        {"url": "https://puzz.link/p?araf/10/10/1h4h1h7i6h6heldh34n5icrai8nc9hblahah3ibh-32h-32hd", "test": False},
        {"url": "https://pzplus.tck.mn/p?araf/10/11/1l6p7q4467h5g55q7g7647g1q-108g-10h-1075-10q9p-10ld", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")

            exclude = []
            for (r1, c1, d1, tp1), num1 in puzzle.text.items():
                validate_direction(r1, c1, d1)
                validate_type(tp1, "normal")
                fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
                if abs(r - r1) + abs(c - c1) >= max(int(num), int(num1)):
                    exclude.append((r1, c1))

                if (r, c) != (r1, c1) and abs(int(num) - int(num1)) <= 1:
                    exclude.append((r1, c1))

            self.add_program_line(f"clue({r}, {c}, {int(num)}).")
            self.add_program_line(grid_src_color_connected((r, c), exclude_cells=exclude, color=None, adj_type="edge"))
            self.add_program_line(araf_region_clue_count((r, c)))
            self.add_program_line(araf_region_count((r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
