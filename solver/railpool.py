"""The Rail Pool solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, defined, display, fill_line, grid
from noqx.rule.helper import fail_false, full_bfs, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route


def len_segment_area(color: str = "grid") -> str:
    """
    Generate a rule to get the length of segments.
    """
    rule = f'nth_horizontal(R, C, 0) :- line_io(R, C, "{Direction.RIGHT}"), not line_io(R, C, "{Direction.LEFT}").\n'
    rule += f'nth_horizontal(R, C, N) :- line_io(R, C, "{Direction.LEFT}"), nth_horizontal(R, C - 1, N - 1).\n'
    rule += f'nth_vertical(R, C, 0) :- line_io(R, C, "{Direction.BOTTOM}"), not line_io(R, C, "{Direction.TOP}").\n'
    rule += f'nth_vertical(R, C, N) :- line_io(R, C, "{Direction.TOP}"), nth_vertical(R - 1, C, N - 1).\n'

    rule += f'len_horizontal(R, C, N) :- nth_horizontal(R, C, 0), {color}(R, C + N), nth_horizontal(R, C + N, N), not line_io(R, C + N, "{Direction.RIGHT}").\n'
    rule += f'len_vertical(R, C, N) :- nth_vertical(R, C, 0), {color}(R + N, C), nth_vertical(R + N, C, N), not line_io(R + N, C, "{Direction.BOTTOM}").\n'
    rule += f"len_horizontal(R, C, L) :- {color}(R, C), nth_horizontal(R, C, N), len_horizontal(R, C - N, L).\n"
    rule += f"len_vertical(R, C, L) :- {color}(R, C), nth_vertical(R, C, N), len_vertical(R - N, C, L).\n"

    rule += f"area_len(A, L) :- {color}(R, C), area(A, R, C), len_horizontal(R, C, L).\n"
    rule += f"area_len(A, L) :- {color}(R, C), area(A, R, C), len_vertical(R, C, L).\n"
    return rule


class RailPoolSolver(Solver):
    """The Rail Pool solver."""

    name = "Rail Pool"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VZdb9owFH3nV1R+9oO/4th5qbqu3QvrPug0TRFClKYrGpQOyDQF8d937FyajDC1UqWqD1OIdXJ9fO/xta/N6mc5Xhbc49GOCy7xaCfi60z4CXoup+tZkR3xk3J9u1gCcP7h/JzfjGergvdyog17m8pn1Qmv3mU5U4zHV7Ihrz5lm+p9Vg14NUAX4wa2PpBkXAGeNfBr7A/otDZKAXwBbIABvwFOpsvJrBj1a8vHLK8uOQtx3sTRAbL54lfBahfxe7KYX02D4a6c38zIuCqvFz9Koskwqpytp5PFbLFk0ZUcbnl1UqvvH1CvD6nXB9QT4dnqr8ZrrMXqdnp/aAr+8BS2WJnPmMQoy8N8vjTQNXCQbZgzLDPboHjDjNzlhSP3cGxMMBwftyy2Y/HR0his26ekgtXb48GgOpROJG/2xPhOaO/2Qksh9jlS+o5JdcJL1YkvVfq3CUmS2WYbVjS057FVsb1EPnmlY/s2tiK2SWz7kXOGBEtvufTwq+Dfp1xJEbESvsFKc6VtjbUFTsluWhicIDlgg7FW1dgqYF3jRDQ4cBLyn8JPmhBOuHKuxi5tcCIxlvxb8C3xE9XC4CQUN8VYT/494npJdtfC4KTkXyGuJoyTSGlPdtvC4ChLuQr5oVgSGiTNS4gHHDlil09ok6RfQr8kzUK1MDiCfCpoMzTWwKchzcq1MDhqlx/k39IaWWi2tC6JaWFwEtKQQpunWB4aPOl3osGB40hDgrlbimWhwVJOEtvC4CSkQWGsIf8G/g351KLBgaN3+Qk5IZ0y7EOKJZIWBkdQrhx8Ot1gT3YPfqhLtQ0nYdjmp7E1sbVx+6fhsHnicVQfRM+pNKZD/r0LQnlYOo3ilTwkR0ebQvp0XY+Pis7Bl3tP8rosw17OBuXyZjwpcD30p3fF0cViOR+H++7s+nvr66KcXxXL3Teu7m2P/WbxzTVcmf+3+eu9zcMqiRcroieWxyNycmScqpBXHzi7L0fjESbG8MeRx866MP/RWdfq4U4UeafjxWeP82HY+wM=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="grid", adj_type="line"))
        self.add_program_line(single_route(color="grid"))
        self.add_program_line(len_segment_area(color="grid"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            if rc:
                len_data = 0
                for j in range(4):
                    num = puzzle.text.get(Point(*rc, Direction.CENTER, f"tapa_{j}"))
                    if isinstance(num, int):
                        self.add_program_line(f":- not area_len({i}, {num}).")
                        len_data += 1
                    len_data += num == "?"
                self.add_program_line(f":- #count{{ N: area_len({i}, N) }} != {len_data}.")

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
