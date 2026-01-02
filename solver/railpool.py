"""The Rail Pool solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, full_bfs
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected


def len_segment_area(color: str = "grid") -> str:
    """
    Generate a rule to get the length of segments.
    """
    rule = 'nth_horizontal(R, C, 0) :- grid_io(R, C, "r"), not grid_io(R, C, "l").\n'
    rule += 'nth_horizontal(R, C, N) :- grid_io(R, C, "l"), nth_horizontal(R, C - 1, N - 1).\n'
    rule += 'nth_vertical(R, C, 0) :- grid_io(R, C, "d"), not grid_io(R, C, "u").\n'
    rule += 'nth_vertical(R, C, N) :- grid_io(R, C, "u"), nth_vertical(R - 1, C, N - 1).\n'

    rule += f'len_horizontal(R, C, N) :- nth_horizontal(R, C, 0), {color}(R, C + N), nth_horizontal(R, C + N, N), not grid_io(R, C + N, "r").\n'
    rule += f'len_vertical(R, C, N) :- nth_vertical(R, C, 0), {color}(R + N, C), nth_vertical(R + N, C, N), not grid_io(R + N, C, "d").\n'
    rule += f"len_horizontal(R, C, L) :- {color}(R, C), nth_horizontal(R, C, N), len_horizontal(R, C - N, L).\n"
    rule += f"len_vertical(R, C, L) :- {color}(R, C), nth_vertical(R, C, N), len_vertical(R - N, C, L).\n"

    rule += f"area_len(A, L) :- {color}(R, C), area(A, R, C), len_horizontal(R, C, L).\n"
    rule += f"area_len(A, L) :- {color}(R, C), area(A, R, C), len_vertical(R, C, L).\n"
    return rule


class RailPoolSolver(Solver):
    """The Rail Pool solver."""

    name = "Rail Pool"
    category = "loop"
    examples = [
        {
            "data": "m=edit&p=7VZdT9tKEH3nV1T72pXqXX/Ea6mqAoRKCFK4wOWChSITHBJw4tZJABnx33tmvSb+oq1UqerDlZPV8ZnZmbOz9qyX39ZRFnOFy/a5xQUu27f033foZ5nrdLZK4uAd769X0zQD4PzL3h6fRMky5vsXd9u79/3HQf+/D+6lbZ8NJ+/vdo/P7m7O/xXH1uxDZg0Tf3F4tLudvP+cXx5O+w/xIPaOlul4msTRTZRfnu8/JYs9/3Y6ETv70x1/Ei2s5Tf/VD1sH3/8uBUaIVdbz7kK8j7PPwchk4zrv2BXPD8OnvPDID/h+QlMjDvgDoAE4xJwsIHn2k5opyCFBTwEdoABLwDHs2ycxKODgjkKwvyUM8qzrWcTZPP0IWZFCH0/TufXMyIW6/kkMeRyfZPer40bYrH5OlnNxmmSZkQS98LzfqH+oEO93aWeyKZ64/Db6q+jFXZ7OZ197VqC6l7CC3bmHyxiFIS0nrMN9DfwJHhmvsMCB3gI7IiyLhy1R2AHxpB9+lRhvBajNLMhPL/p0rOIwaPxSsiWSyuT0kxFjGqlVkWmDSEsnanqI0Shr0rJVnohW/mF7NUpFEkEzxgv9LinR6nHU9ST57Yed/Vo6dHV44H2GaDAQnlcKMSViK96XAroBZaW2mBpc2ljrYRtD7jwl9KpYPiQZMIO5npYEWFPAtsFdq0NJh/XxO8hTs812OXSRxUJ+9BTYldgronvwd8z/i7FLzF8XJO3h7nKxFfIq/Akad6vYPj0THyJvLbB6HXSxiZpntZbYvjIog5CUX1MLgENwqzLQi6DtQ/tv+ahTRj9AvqF0WzR3BLDxzIxJbQ5Zq6DmPQmaB7aXjF8ZFkf1N8ze+RBs2f2xaValRg+rtHQgzZlciloUEY/OvsrJh/faHCxdnqPdHxo8ExNXMpVYvi4RoPEXMfEdxDfMTFtWovB5GOX9aGaGJ2CnkOTy0LMVwwfy9TKR0y/1Ez6Da/gT++lxAN+rh/zHT06evT049+jZvOL7ahoRL/zpjGb6q98Espp62y8vIJTcYBoP1E+u3gffyo6hD+dwtXL/buYq62QnayzSTSOcTwczBbxu2GazSM67wY3t5W74Xp+HWflPY5utkyT0bKYO4qfovGKBcUnRNVS43CSIkaNStL0a4K0HRFKU42c3S7SLO40ERlD8xuhyNQR6jrNbhqaHqMkqa9Ff1rVqOJMrlGrDAdu5T7KsvSxxsyj1bRGVA7nWqR40SjmKqpLjO6jRrb5phwvW+yJ6X9oY5Od/7+z/t7vLNol64+1t19sXD+RE6Lipj/y/AtnX9ejaISFMXzSc20sWuYbxqKLdhvRfluGP756/T6l2Q+a28bYpDtaHNgfdLmKtYt/o6FVrE2+1b1IbLuBge3oYWCbbQxUu5OBbDUzcG/0M4rabGmkqtnVKFWrsVGqam8Lr7a+Aw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line("railpool(R, C) :- grid(R, C), not black(R, C).")
        self.add_program_line(fill_path(color="railpool"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="railpool", adj_type="loop"))
        self.add_program_line(single_loop(color="railpool"))
        self.add_program_line(len_segment_area(color="railpool"))

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
            self.add_program_line(f"black({r}, {c}).")

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_io", size=3))

        return self.program
