"""The Tatamibari solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Point, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, reverse_op, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region, avoid_edge_crossover, count_rect


def tatamibari_cell_constraint(op: str, src_cell: Tuple[int, int]) -> str:
    """Generate a cell relevant constraint for tatamibari."""
    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
    rop = reverse_op(op)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {count_r}, {count_c}, CR {rop} CC."


def encode_symbol_to_text(puzzle: Puzzle) -> None:
    """Encode the symbol clues to text clues for tatamibari."""
    for (r, c, d, label), symbol_name in puzzle.symbol.items():
        validate_direction(r, c, d)
        validate_type(label, "normal")
        if symbol_name == "line__1":
            puzzle.text[Point(r, c, d, label)] = "-"

        if symbol_name == "line__2":
            puzzle.text[Point(r, c, d, label)] = "|"

        if symbol_name == "line__5":
            puzzle.text[Point(r, c, d, label)] = "+"


class TamamibariSolver(Solver):
    """The Tatamibari solver."""

    name = "Tatamibari"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VVLb9NAEL77V1RznsOu13FsX1AoSS8hBRJURVYUOa0hEbYc/EBoo/x3ZseWHyWAKFLVA1rv6JvHjr6Z1ayLr1WUx+jTUh4KlLSUJ3h7jvlEs1aHMomDK5xU5T7LCSDezmb4KUqKGK2wCdtYJ+0HeoL6JgjBBuQtYYP6fXDSbwO9Rr0kF6Ak25yQBLQJTjt4x36DrmujFIQXDSa4DkI9Z/SO0ArB5H/NpwyENPsWQx3O+n2W7g7GsItKqqLYH46Np6gesi8VtKkhrZLycJ8lWQ4NyzPqSU19eoG66qirlrr6LXVIo3K/vYGnFBA/fI6LaneJvX+Z/Zlu5APx3wahKeVjB70OLoPT2dA8gbLNyVd0tL428MRjg/fIIJU7sFAmyfnWlM820TbW1wXKJJOt5pA2ajW3Hzka+Fy77/MGPincgSqHXi6opzr9TFIN6ElHdMFUwIzLsFmuqFOoFcs3LAXLEcs5x0xZ3rG8ZumwdDlmbHr9V7fR7+TT6FBXqTu+R+0dOzWQNNTSH0OgCPsSbUEO9Ufeoe3x69Bfo5dl2VghTGlArhZZnkYJDcmiSndx3unLfXSMgR6pswXfgXeo6Kjz/916ee+WuR3xzPPyr+MbUrPbCUN9i3CsttGWSgP6OWLtbobuspsG9heOsfOT49mrp3dgY/0A",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        encode_symbol_to_text(puzzle)
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(avoid_edge_crossover())
        self.add_program_line(count_rect(len(puzzle.text)))

        all_src: List[Tuple[int, int]] = []
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
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
