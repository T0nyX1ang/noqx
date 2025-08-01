"""The Look Air solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.shape import all_rect


def square_size(color: str = "black") -> str:
    """Generate a rule to determine the size of the square."""
    rule = (
        f"square_size(R, C, N) :- upleft(R, C), MC = #min{{ C0: grid(R, C0 - 1), not {color}(R, C0), C0 > C }}, N = MC - C.\n"
    )
    rule += f"square_size(R, C, N) :- grid(R, C), {color}(R, C), square_size(R, C - 1, N).\n"
    rule += f"square_size(R, C, N) :- grid(R, C), {color}(R, C), square_size(R - 1, C, N).\n"
    return rule


def avoid_same_size_square_see(color: str = "black") -> str:
    """Generate a constraint to avoid the same size square seeing each other."""
    rule = f"left_square(R, C, C - 1) :- grid(R, C), {color}(R, C - 1), not {color}(R, C).\n"
    rule += "left_square(R, C, C0) :- grid(R, C), not left_square(R, C, C - 1), left_square(R, C - 1, C0).\n"
    rule += ":- upleft(R, C), left_square(R, C, MC), square_size(R, C, N), square_size(R, MC, N).\n"
    rule += ":- left(R, C), left_square(R, C, MC), square_size(R, C, N), square_size(R, MC, N).\n"

    rule += f"up_square(R, C, R - 1) :- grid(R, C), {color}(R - 1, C), not {color}(R, C).\n"
    rule += "up_square(R, C, R0) :- grid(R, C), not up_square(R, C, R - 1), up_square(R - 1, C, R0).\n"
    rule += ":- upleft(R, C), up_square(R, C, MR), square_size(R, C, N), square_size(MR, C, N).\n"
    rule += ":- up(R, C), up_square(R, C, MR), square_size(R, C, N), square_size(MR, C, N).\n"
    return rule


class LookAirSolver(Solver):
    """The Look Air solver."""

    name = "Look Air"
    category = "shade"
    aliases = ["rukkuea"]
    examples = [
        {
            "data": "m=edit&p=7VTBbtswDL37KwqeebAl20l1GbKu2SVztyVDUQiG4XguatSGOiceBgX591KUOxfdDluBtZdB0MPLE6k8UmF234ayrzGlJecYYkRLpCnvKI55h+PaNPu2Vie4GPY3pieCeLFc4nXZ7upAj1F5cLCnyi7QvlcaBCDvCHK0n9TBflA2Q7umI8A5aStiEaAgej7RSz537MyLUUg8GznRK6JV01dtXay88lFpu0Fw3/OWsx2Fznyvwafx58p028YJ23JPxexumrvxZDd8NbfDGBvlR7QLb3f9YNfZGe3Kya6j3q5jv7Hr0v6x3dP8eKS2fybDhdLO+5eJzie6VgfCTB1ACJcqyYt/GxAzJ7yZBPk0QiZPhJhTXLWjkEgn0HM/CCkL4SOB73gUMeOIn3eQu4g9XjEuGQXjhkpAKxnfMYaMCeOKY84ZLxnPGGPGlGNmrgl/2CYQZGxObYlBCd+zF/CmheAB9Ct5Ps8DDeuhvy6rmn4v2dBt6/4kM31XtkADegzgB/DWksLj/zP7SjPrniD8q8l9/QnR1F0h0V4g3A1FWVSmBfrbx2fp8S/6i1dLYwetMbdl00Me3AM="
        },
        {"url": "https://puzz.link/p?lookair/9/9/g2a2b4d2i2y1i3d4b1a1g", "test": False},
        {"url": "https://pzplus.tck.mn/p?lookair/20/10/1b2f12b1c3d2l2zzg2a1b4a3zzg2l4d2c1b32f3b2", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4, include_self=True))
        self.add_program_line(all_rect(color="gray", square=True))
        self.add_program_line(square_size(color="gray"))
        self.add_program_line(avoid_same_size_square_see(color="gray"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="gray", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
