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
    rule = 'nth_horizontal(R, C, 0) :- grid_direction(R, C, "r"), not grid_direction(R, C, "l").\n'
    rule += 'nth_horizontal(R, C, N) :- grid_direction(R, C, "l"), nth_horizontal(R, C - 1, N - 1).\n'
    rule += 'nth_vertical(R, C, 0) :- grid_direction(R, C, "d"), not grid_direction(R, C, "u").\n'
    rule += 'nth_vertical(R, C, N) :- grid_direction(R, C, "u"), nth_vertical(R - 1, C, N - 1).\n'

    rule += f'len_horizontal(R, C, N) :- nth_horizontal(R, C, 0), {color}(R, C + N), nth_horizontal(R, C + N, N), not grid_direction(R, C + N, "r").\n'
    rule += f'len_vertical(R, C, N) :- nth_vertical(R, C, 0), {color}(R + N, C), nth_vertical(R + N, C, N), not grid_direction(R + N, C, "d").\n'
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
            "data": "m=edit&p=7VVNT+NIEL3nV6A+96G//NG+IIaBvWTD7oYRQlYUhWCGaBLCJHg0cpT/zqt2OfaQjEBCQnNYOW69vH5d9braZa+/l5NVIT0um0olNS6bqnCnjn6Kr8vZ07zIjuRJ+XS/XAFIeXF+Lu8m83XRy1k16m0qn1Unsvory4UWUhjcWoxk9W+2qf7OqqGshpgS0oHr1yIDeNbCqzBP6LQmtQIeADtgwGvA6Ww1nRfjfs38k+XVpRSU51NYTVAslj8KwT7o/3S5uJkR8VAu7uZMrsvb5beSZXq0ldVJ7bR/wKk95JTIl05Z8G6nN5MnlH19P3s8ZNePtltU/D8YHmc5ef/SwrSFw2wjUicyBzwAdrrZr0RNEdVhMhfHxx0m3mN8YFoiTl9KEkUMjnxHmD3JXiYfmI4Zv5fa15laQquQqavRuvbXpcxeem328muT/EqhSDrbYLwO43kYTRgvUU9Z2TB+DqMKYxTGftCcocDax1J7xDWI7xNpNPwCG+VbbKw0FnslbGPgWm+M62BoyDJhh7UxdkQ4NsC2xpFqMWkijp8gThIxjqRJUUXCKfw0ONJYy/Fj6GPWRxS/wdBEnDfBWs/xPfJ6PEmBTzsYmoTjG+S1jPGCMRaHFHjab4OhMXUdtKf6cC4ND5r3pZCLcdDQ+Qce3jT71/Cv2bOitQ2GRnFMA2+O1zrEpE4IPLztMDSmqQ/qH/MZxfAc87lEVKsGQxOxhwTePOfy8ODZP16nO0yalD1E2Dv1UYgPDzHXJKJcDYYmYg8Gax3Hd4jvOKalvTAmjW3qQzVhn5qeQ86lEHOHoVFcqxQx08Yz+WfeQ099afCAX4XH/DSMLoxxePwTetm88XVUv4je02nCUv19SkYlHZ1F82pJxQGi80T5bN2Pr5rOoadPX/eK/ixm1MvFsFzdTaYFPgX92UNxNFiuFhP6jp3dfu38G5SLm2LV/McnedsTP0W4c4tQ7v+v9Md/pan66sOa442P/St2clSXu0tWF1I8luPJeLrEmaCAYbJuuN9M1j14eBLNuzfx4btH3496zw==",
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

        areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(areas.items()):
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
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
