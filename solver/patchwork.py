"""The Patchwork solver."""

from typing import List, Tuple

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_src_color_connected
from noqx.rule.shape import all_rect_region
from noqx.solution import solver


def count_patchwork_src(target: int, src_cell: Tuple[int, int], color: str = "black") -> str:
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    src_r, src_c = src_cell
    return f":- #count{{ R, C: {tag}({src_r}, {src_c}, R, C), {color}(R, C) }} != {target}."


def avoid_area_adjacent(color: str = "black") -> str:
    """Generate a constraint to avoid the same color in adjacent edges."""
    constraint = f":- grid(R, C), grid(R - 1, C), edge_top(R, C), {color}(R, C), {color}(R - 1, C).\n"
    constraint += f":- grid(R, C), grid(R, C - 1), edge_left(R, C), {color}(R, C), {color}(R, C - 1).\n"
    return constraint.strip()


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(all_rect_region(square=True))
    solver.add_program_line(avoid_area_adjacent(color="black"))
    solver.add_program_line(avoid_area_adjacent(color="white"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        assert isinstance(num, int), f"Clue at ({r}, {c}) must be an integer."
        solver.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))
        solver.add_program_line(count_patchwork_src(target=num, src_cell=(r, c), color="black"))

    for (r, c, d, _), draw in puzzle.edge.items():
        assert d is not None, f"Direction in ({r}, {c}) is not defined."
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    for (r, c, _, _), color in puzzle.surface.items():
        if color == Color.GRAY:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        elif color == Color.BLACK:  # black color
            solver.add_program_line(f"black({r}, {c}).")
            solver.add_program_line(f"not gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"white({r}, {c}).")
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="edge_left"))
    solver.add_program_line(display(item="edge_top"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Patchwork",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VbNbtNAEL7nKao978H7Y8f2rRSXS0mBFFWVZUVu6tKIRClJjdBGeffOzxbXEDcNgSIk5Hjm8zezuzOz63GWX+pyUUkV4M/EEjRcVsV06ziiO/DX2eRuWqUH8rC+u5kvAEh5enwsr8vpsurl3qvorVySukPp3qS50ELSrUQh3ft05d6mbiDdEExCxsCdAFJCaoBZA8/JjuiISRUAHngM8ALgeLIYT6vRCTPv0tydSYHrvKLRCMVs/rUSPIyex/PZ5QSJcno99dyyvpp/rr2XKtbSHXKg2UOgtgnU+EAtQw4U0YZAMf69A70s76Dqy5vJ7aZwk2K9hoJ/gIBHaY6xf2xg3MBhuhImEGkshTGsElLWsuqTCmNSEbv0meyzZ6xYRaQSdklCUirguVWgveYxSvH0SvEopXgBZbyf4SWU9XzIi6jQ+0feL8J1II8B5gFzc635XFEOdNS+EzBrywPzahGYYWsIJpkL0xCYZ2sI5dQaQ1nlInzEYF4/MBTL41GYa5vBrNtrYf6PwoHMVboCeUHymKQmeQYbLJ0h+ZpkQDIkeUI+GclzkkckLcmIfPp4RJ59iCBUC6cH8tRQaNgWeLIQrebd2T9SYTVMnuCh1DA9Am0SqS0cMQPYBoAhCsTKSK2hwIh13/NbU80N97n2Ff57XNHLxbBeXJfjCppDdvWpOhjMF7MSO9ugnl1Wi4dn6Mrrnvgm6M4NNvn/jfrFGzUWP3jmm/a7Xqd9X/zcDaVR0p1KcVuPytF4DtsBtSNe/2F+13V39LdhBx9t4rOmEXWZfW/qMvsW1WX23Wyz2WrbZTC7GvpxhyHZWKhMRirZ0bAlm621eLKS8IX4e7Xo3Iit279nRZTUIfyz+BXzE4en0/Dzu/HinQk+1UXvHg==",
        },
    ],
}
