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
            "data": "m=edit&p=7VRRb9owEH7nV1R+9oPPCcHJG+tgL4xua6eqiiIUaLqigdIFMk1G/PfeXcIcb7BpQur2MIWcvs93dr4zd7f5UudVIWN8AiOVBHwCo/g1If1U+9wst6siuZDDevtYVgikvBqP5UO+2hS9tI3KejsbJ3Yo7ZskFVpIfkFk0r5PdvZtYqfSXqNLSMC1CSIQUiMcOXjLfkKXzSIoxNMGRwjvEC6W1WJVzCbNQe+S1N5IQd95xbsJinX5tRDNNuaLcj1f0sI832Iym8flU+vZ1Pfl57qNhWwv7bCROzoiN2jlhg1s5BI6IpeyOFtucf+p2NTzY1rjbL/HO/+AamdJSsI/OmgcvE52aKfJTmiDW0MZNX+L0LFHA0AaOap9b+DTPlJwNPK8IQXHjg482g+RBo7SUR3qi4x8VRGpct+NKAVHB/53jfIped2HDMnoeElG31GS4U6OKdipAkVHOzcougAnE5SfBQDpHnQ4ndfZr+k83eEU78SB/jHev3AI/GSA/xCXDQSk5+DHcgAuiju2Y7aa7Q3WjLQB29dsFds+2wnHjNjesr1kG7KNOGZAVfdHdXm+HKw/zDc2mB2OLYix3gKsbxVLDXixhEEhxlo6YI3FgBiMkVo162AGiCn+t+ml2vC87D79f2sl66VihNPjYlpW63yFE2Rar+dFdeA4r/c98U3wi20BMvw/wv/GCKf7Vy/cMOf2b4pX+73XpL2S4qme5bNFiXWG98fuQ/udcrcd+Ss3NukJ96FvT7qbVj7uxmnxk+PFLxiHiMir/EFkvWc=",
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

        for (r, c, d, tp), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(tp, "normal")
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
            self.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
