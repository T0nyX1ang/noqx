"""The Yajilin-Kazusan solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.variety import yaji_count


class YajiKazuSolver(Solver):
    """The Yajilin-Kazusan solver."""

    name = "Yajilin-Kazusan"
    category = "shade"
    aliases = ["yk", "yajisan-kazusan"]
    examples = [
        {
            "data": "m=edit&p=7VZNb9NAEL3nV0R7AmmQdv0Rr30LpeESUiBBVWVZlhNcNTTBxakRbJT/3pnxoqwbH+BAKyFkefL8PDP7ZjxeZ/etKeoSVAAx+BokKDzCSOKFBK00n9Iei/X9pkyGMG7ub6oaAcDFZALXxWZXDlLrlQ32Jk7MGMzbJBWeAD6VyMB8SPbmXWJmYOZ4S4BGbopICfAQnh/hJd8ndNaSSiKetQkVwiuEq3W92pT5tGXeJ6lZgKB1XnM0QbGtvpeiTcHXq2q7XBOxLO6xmN3N+s7e2TWfq9vG+qrsAGbcyp33yPWPcgm2cgn1yKUq/rLcODscsO0fUXCepKT90xHqI5wne7SzZC8Cj0KD3Ec19IQwYxAS5eXU4V9UzAvkVJGlQkmUdL1GwUngiHP5bvooar2cXBGnD9xA7Z8ExhzYpawuJ1BJdSJMSc7muaFKsZ+XS5cb9fjZZd18nj7181hLl/O5SarL9Wjxe9b1e9YION8jztbR4Ti201A1sn13642sFtdP80R0/TTX5vQAp0fxDF2xnbD12C5wxMD4bN+wlWxDtlP2OWd7yfaMbcB2xD4RDelvjrGgNnk4jlidbmf6CbSluEXSBtl/hP/2vWyQinlTXxerEvegWbNdlvVwVtXbYiNw0z8MxA/BZ+qje/D/O/BM3wF6BPKPvgbP/1an2N0wAnMB4q7Ji3xVbQT+lQDi8Z17zD+5enz1xc/iy/q2MM3wBaFd8fUVXeHvS5ENHgA=",
        },
        {
            "url": "https://puzz.link/p?yajikazu/9/9/301040104010103040201030101030103040301030101020304010203030401040404040301010304010401030402030402020203040203040302020204040304020402040201010402020102020402040",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent(color="gray"))
        self.add_program_line(grid_color_connected(color="not gray"))
        self.add_program_line(count(("gt", 0), color="gray", _type="grid"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            fail_false(isinstance(clue, int) and label.startswith("arrow"), "Please set all NUMBER to arrow sub.")
            arrow_direction = label.split("_")[1]
            self.add_program_line(yaji_count(int(clue), (r, c), arrow_direction, color="gray", unshade_src=False))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
