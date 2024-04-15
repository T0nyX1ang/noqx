"""The Tatamibari solver."""

from typing import List, Tuple

from . import utilsx
from .utilsx.encoding import Encoding, reverse_op, tag_encode
from .utilsx.fact import display, edge, grid
from .utilsx.reachable import bulb_src_color_connected
from .utilsx.rule import adjacent
from .utilsx.shape import all_rect_region
from .utilsx.solution import solver


def tatamibari_cell_constraint(op: str, src_cell: Tuple[int, int]) -> str:
    """Generate a cell relevant constraint for tatamibari."""
    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
    rop = reverse_op(op)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {count_r}, {count_c}, CR {rop} CC."


def tatamibari_global_constraint() -> str:
    """Generate a global constraint for tatamibari."""

    no_rect_adjacent_by_point = [
        "vertical_line(R, C + 1)",
        "vertical_line(R + 1, C + 1)",
        "horizontal_line(R + 1, C)",
        "horizontal_line(R + 1, C + 1)",
    ]
    rule = f":- grid(R, C), {', '.join(no_rect_adjacent_by_point)}."

    return rule


def encode(string: str) -> Encoding:
    return utilsx.encode(string)


def solve(E: Encoding) -> List:
    if len(E.clues) == 0:
        raise ValueError("Please provide at least one clue.")

    solver.reset()
    solver.add_program_line(grid(E.R, E.C))
    solver.add_program_line(edge(E.R, E.C))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_rect_region())
    solver.add_program_line(f":- {{ upleft(R, C) }} != {len(E.clues)}.")

    for (r, c), clue in E.clues.items():
        solver.add_program_line(f"clue({r}, {c}).")
        solver.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

        if clue == "+":
            solver.add_program_line(tatamibari_cell_constraint("eq", (r, c)))
        elif clue == "-":
            solver.add_program_line(tatamibari_cell_constraint("lt", (r, c)))
        elif clue == "|":
            solver.add_program_line(tatamibari_cell_constraint("gt", (r, c)))

    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
    solver.add_program_line(f":- clue(R, C), clue(R, C), (R, C) != (R1, C1), {tag}(R, C, R, C1), {tag}(R1, C1, R, C1).")
    solver.add_program_line(tatamibari_global_constraint())
    solver.add_program_line(display(item="vertical_line", size=2))
    solver.add_program_line(display(item="horizontal_line", size=2))
    solver.solve()

    return solver.solutions


def decode(solutions: List[Encoding]) -> str:
    return utilsx.decode(solutions)
