"""The Juosan solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs


def jousan_constraint():
    """Constrain consecutive lines. Black for horizontal, not black for vertical lines."""
    rule = ":- grid(R, C), grid(R + 2, C), black(R, C), black(R + 1, C), black(R + 2, C).\n"
    rule += ":- grid(R, C), grid(R, C + 2), not black(R, C), not black(R, C + 1), not black(R, C + 2).\n"
    rule += f'line_io(R, C, "{Direction.LEFT}") :- grid(R, C), black(R, C).\n'
    rule += f'line_io(R, C, "{Direction.TOP}") :- grid(R, C), not black(R, C).'
    rule += f'line_io(R, C, "{Direction.RIGHT}") :- line_io(R, C, "{Direction.LEFT}").\n'
    rule += f'line_io(R, C, "{Direction.BOTTOM}") :- line_io(R, C, "{Direction.TOP}").\n'
    return rule


def count_lines(area_id: int, num1: int, num2: int = 0):
    """Limit the number of horizontal or vertical lines."""
    rule = f"count_area({area_id}, N) :- #count{{ R, C: area({area_id}, R, C), black(R, C) }} = N.\n"
    rule += f":- not count_area({area_id}, {num1}), not count_area({area_id}, {num2})."
    return rule


class JuosanSolver(Solver):
    """The Juosan solver."""

    name = "Juosan"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VbbbhMxEH3PV1R+9oNv68u+oFJaXkoKtKhCURSlIagRG6XkgtBG+XeOveNsEKWVEpWChJL1HnvGc/GZnd3F19VwPuZSxL/2HHf8jPTpUt6mS9DvarKsxuURP14tb2dzAM4vzs7452G1GPNOj9T6nXUdyvqY16/LHlOMp0uyPq/flev6TVl3eX0JEeMSa+dAknEFeNrC6ySP6KRZlAK4C6ybbR8BR5P5qBoPzpuVt2WvvuIs+nmZdkfIprNvY9aYSPPRbHoziQs3wyWyWdxO7kiyWH2afVmRroxbV9VyMppVszmjaDe8Pm5SuL4nBd2moLcp6HtSoByfOIVwfwob0PMeSQzKXsznQwt9Cy/L9SbGGkdZrlkQBgZMOpYgFbBtsBLAsXzSxGwFUkiLiaaJtjsSE9UUTdyORIpojb1gNC1sqyit2EYgpTetcWV8a0LtqmlldiaFaidG5+g2kYeY5lkaVRqvcAq81ml8lUaRxiKN50nnFMeipOZKOVYqFLksgANhPDhaNFgJYEPYcWUk4QCsG6yhY0hHG55SithgvaB1I4ELwvBbkF8D/SLrw68lvwXWLa0XiM1SbAVicBRDgYfcqQZb+HLky8aHn9Yd/Hry61RsCIRh35N9B/ue7DvEECgGD/1A+h46gXTQVLTIOh6YfPkATGcSoCNJJzhgijlARzY6sAFsCEvggrABbmLDPq4VrYMvTXxhH3DWgS/iC/uAm3iwDzgQRgzEHfYBkw6408Qd9gFbwoizoDjBnSbusA+YdMCjJh5hA9i3NaDpzHWsE9HWQ66fyLvJ9YCzJb+pBkyuDdfWUqyHXD+Ra0t2LPi1uQbAl6Xzt/DryK8Tbc1E3l2uB/h1uR7g15FfL9v6CdgbMneIJ1A8wW/rIfEoZMsj1QPu23rAHZjOOb6tqB7AObBteZSZX7dTA+BLZh5jDZAdZdraiLyYzBfWTV4viNNN7Onx0T9Jo0mjTS3Bxba5R2M9pPs04TAj8LJWOC/NmZWB29iS9QNR9nTzlv/5V/x7a/1Oj10Pqwovv+5qejOeH3Vn8+mwYvgC2XTYd5au2OW5+f9R8pd/lESqxLM8Qfs/0D2c+Pb54/UFZ3erwXCA1Bg+g3kSW7Qhizb0W7GHOOwtftD4YaE9stugBxv00f3EVmtu9fPsPlAsAsT6iQ71YeOPEnpIMR3m+zkjz6+9X8R/vF/g7drv/AA=",
        },
        {
            "url": "https://puzz.link/p?juosan/21/12/4ql08qtg9qt59ul5bunltnn9tntd72ta72h636h5b641bm04vmcvjo0fu1vo3s6fhuv1u0gf7fvpjo0fvjro0fs3vu0tvvgg33g42554342h553444g2g24211g121g2221341225h121g252442224465g25g1g2425g273",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(jousan_constraint())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, f"corner_{Direction.TOP_LEFT}"))
                if isinstance(num, int):
                    self.add_program_line(count_lines(i, num, len(ar) - num))

        for (r, c, d, _), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
