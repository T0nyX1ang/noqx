"""The Akari solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent


def lightup() -> str:
    """A rule specially designed for akari."""
    tag = tag_encode("reachable", "sun_moon__3", "branch", "adj", 4, None)
    initial = f"{tag}(R0, C0, R, C) :- grid(R, C), sun_moon__3(R, C), R0 = R, C0 = C."
    propagation = f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), grid(R, C), adj_4(R, C, R1, C1), (R - R0) * (C - C0) = 0."
    constraint1 = f":- sun_moon__3(R0, C0), sun_moon__3(R, C), |R0 - R| + |C0 - C| != 0, {tag}(R0, C0, R, C)."
    constraint2 = f":- grid(R, C), not sun_moon__3(R, C), {{ {tag}(R0, C0, R, C) }} = 0."

    return initial + "\n" + propagation + "\n" + constraint1 + "\n" + constraint2


class AkariSolver(Solver):
    """The Akari solver."""

    name = "Akari"
    category = "var"
    aliases = ["bijutsukan", "lightup"]
    examples = [
        {
            "data": "m=edit&p=7VVNj9owEL3zK9Cc5xDHCRDf6HbphbJtYbVCFkKBZkW0YUMDqSoj/nvH4wiCllRLpX5JVfB45tkev+cvtl/KuEhQePYne0g1fYHocfF7HS5e9U3SXZaoNvbL3SovyEG8GwzwMc62CbZ01W3W2ptImT6ad0qDAASfioAZmo9qb94rM0YzpibAgLCh6+STe3tyH7jdejcOFB75I+d3yZ2Su0yLZZbMh9RKyAelzQTBzvOGR1sX1vnXBCoeNl7m60VqgUW8IzXbVbqpWrbl5/yprPoKO7TMdukyz/ICOJ+YHdD0nYTpBQnyJEEeJcgfS9iWz/N1nj//lIT4KS7SS+yjy+wPtDOfiP9caSvl/uT2Tu5Y7UH6oAKEUHDVcVFXctVzYORA4TlUiMDVfoXLCg8qvGPjg9Xv0msfu+5U8DRaHEM7nYY2HAE7ca3dEqiNjs6TMaF6bInVY0uwlo2J1mNL+Gx6pn7MQBKE2h/s7lk7YOuzndACopFs37L12IZsh9znlu0D2xu2AdsO9+naLXj1JnmgfIQg5CqMqHLrW6cILE/i2UH7Rby1dM/H+Rf+e9ispWFcFo/xMqHbNSrXi6Roj/JiHWcUj1fxJgF65Q4t+AZcaIHp1fz/8P29D5/dJe+VN+vlLfozF13TYkuB5g5hU87jOWkC+ntFTeco6FyH09W83D+8jIdRQ54GPi9wvwGXFm/SNW3g34xLeR1+RZ7ffhroBZ21vgM=",
        },
        {
            "url": "https://puzz.link/p?akari/17/17/g666.g6.g6.x6.x6.x6.obl6.gbi6cv.gblcmbl7cv6bi66blam6.x.gbv.gcv66.g666.g.g",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?akari/20/20/................................h............h1...h............i...i...........i1.bg........t.....i6cn...hbibi1b..kbl1b0.g6bgc..l..k.j1.l..hciam...i6.q...v0...bs....b.b..h2..h....i..h..i..h....i..h..b..h....h1..h...h..h....................../",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="sun_moon__3"))
        self.add_program_line(adjacent())
        self.add_program_line(lightup())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="sun_moon__3"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(symbol_name, "sun_moon__3")
            self.add_program_line(f"sun_moon__3({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"hole({r}, {c}).")

            if color == Color.WHITE:
                self.add_program_line(f"not sun_moon__3({r}, {c}).")

        self.add_program_line(display(item="sun_moon__3"))

        return self.program
