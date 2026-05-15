"""The Gokigen (Slant) solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, fill_line, grid
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.route import convert_line_to_edge


def slant_rule() -> str:
    """Generate slant rules."""
    rule = f':- grid(R, C), line_io(R, C, "{Direction.TOP_LEFT}"), not line_io(R - 1, C - 1, "{Direction.BOTTOM_RIGHT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.TOP_RIGHT}"), not line_io(R - 1, C + 1, "{Direction.BOTTOM_LEFT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.BOTTOM_LEFT}"), not line_io(R + 1, C - 1, "{Direction.TOP_RIGHT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.BOTTOM_RIGHT}"), not line_io(R + 1, C + 1, "{Direction.TOP_LEFT}").\n'

    rule += "grid_direc_num(R, C, D, 0) :- grid(R, C), direction(D), not line_io(R, C, D).\n"
    rule += "grid_direc_num(R, C, D, 1) :- line_io(R, C, D).\n"
    rule += f':- grid(R, C), grid(R + 1, C + 1), {{ line_io(R, C, "{Direction.BOTTOM_RIGHT}"); line_io(R, C + 1, "{Direction.BOTTOM_LEFT}") }} != 1.'
    return rule


def no_loop() -> str:
    """Ensure there is no loop in the grid."""
    rule = "reachable(R, C) :- grid(R, C), not grid(R - 1, C - 1).\n"
    rule += "reachable(R, C) :- grid(R, C), not grid(R + 1, C + 1).\n"
    rule += f'reachable(R, C) :- grid(R, C), reachable(R - 1, C - 1), not line_io(R, C - 1, "{Direction.TOP_RIGHT}").\n'
    rule += f'reachable(R, C) :- grid(R, C), reachable(R - 1, C + 1), not line_io(R, C + 1, "{Direction.TOP_LEFT}").\n'
    rule += f'reachable(R, C) :- grid(R, C), reachable(R + 1, C - 1), not line_io(R, C - 1, "{Direction.BOTTOM_RIGHT}").\n'
    rule += f'reachable(R, C) :- grid(R, C), reachable(R + 1, C + 1), not line_io(R, C + 1, "{Direction.BOTTOM_LEFT}").\n'
    rule += ":- grid(R, C), not reachable(R, C).\n"
    return rule


class GokigenSolver(Solver):
    """The Gokigen (Slant) solver."""

    name = "Gokigen"
    category = "var"
    aliases = ["slant"]
    examples = [
        {
            "data": "m=edit&p=7VZLT9tAEL7nV6A9z2Ffs35cKgppLzS0hQohK4pCcCFqUtM8qspR/nvHawsyI1pEqUoPyPJoPn+zs/NYj738th4vSjAIxoNLQYOhK+gUMNGQeoy37q7T6WpW5nuwv15dVwtSAI4H8Hk8W5bQK0xca4a9TZ3l9T7Ub/NCWQXdPYT6Q76p3+X1AOoTohTZQn1EmlFgSe239o16FvlGO2h5o0kftHog9ZzUyXQxmZWjo9bR+7yoT0E1+7yOqxtVzavvpWqXRTyp5hfT5sHFeEXJLK+nNx2zXF9WX9adrWmWrmer6aSaVQvVRbuFer9NoX9PCu4uBXebgnu2FLL7U9hSez5SEqO8aPL5dKemd+pJvtk2sW6US5POXwCS5NOlKT0xOzjjOPMMe20EdoTdDm7s7Q5Gjo3m9sYI3nJsBW+R7295/N5Zjr0WWPj3yOPxQfCpwLw+HkV8KOLBjPPB8v2CE7zYL9ECZ3x96vh+aVN/5dTOE9GB9gy82rVIuc8scJ9Zwj1kvAaoeQ1QnAHUicBiveE1R5OweNDwmqA4E2h5DVCcEbRifyd4x/NHz2uOXuznRX4+4f7Qc3/IO4Ao4gn8nUBxRjCIeBMvsPCfiHhSLTA/c5iKfDL+jmMm7DNpL/qV8X4FrQXm+QXN8wlGYn5egt19x2m0mTjgzqN8E6WN8pTmH9QuysModZQY5VG06Ud5FuVBlD7KEG2SZoI+asY+PRyawQ7iXHXQ6dQP92CURWi/9/ddyQvza2bYK1T/8qrcO5yOr6qv4xl9gAfr+UW52BtUizlh+gva9tQPFW86uQb8y4/Rf/5j1LRKP+736PcfmucfNAU15HYiQH0M6mY9Go8ocwVU9X9BW6LtH9P+SXQ7FR8b+V+ezg/3kCbxsPcT",
        },
        {
            "url": "http://pzv.jp/p.html?gokigen/40/25/hbg1bha6ah66bcbh7c98d8cdjdk672817chc717die62b8dcg8c26di32ck3d287271617262bg31222c88e2bddcc3bkdeg87dc777228ddg1cehdch6cb2cb122b73d3c26b31377c7e71cc8clbg8bh317677c6d7b63716eh26d2b8c9ch31c7ddj28277d77bg732cg27c61cg83268871ci626b8681cieicg2ddjdi6277226ch8d3d7dgec2cg73dd63622d3cb172b62667cc1c66d37226263c7cdg8d7bg7273cg78cb9c77cg22dg061661668dge71b778c76bgcg717c7cd376677173bgdg81b9dc8dgch231ch8ce897cg7b631682cgcckcjdg318277cg4ceh6166cgb6cc268173cgeg2173c27d367328cgc267di6bi7bg77dg769cg78d8d22ba656776bgb1bibajb",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(
            fill_line(
                directions=(
                    f"{Direction.TOP_LEFT}",
                    f"{Direction.TOP_RIGHT}",
                    f"{Direction.BOTTOM_LEFT}",
                    f"{Direction.BOTTOM_RIGHT}",
                ),
                color="grid",
            )
        )
        self.add_program_line(slant_rule())
        self.add_program_line(no_loop())
        self.add_program_line(convert_line_to_edge(diagonal=True))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(f":- #count{{ D: line_io({r}, {c}, D) }} != {num}.")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
