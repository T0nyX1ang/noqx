"""The Yajilin-Kazusan solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import validate_direction
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
            "data": "m=edit&p=7VbNbtswDL7nKQqdedCPHTu+DFnX7JKlW5OhKIzAcDwXDebAnRMPg4K+e0nKQOTGh+2wDhsGQwT1iaT4UYyU/bc2b0pQAUzAxCBB4RdGEicSYhXzkN232h6qMrmAaXt4qBtUAK5nM7jPq30Jo7QzW4+OdpLYKdj3SSq0AB5KrMF+So72Q2IXYJe4JCBGbI6aEqBRvTqpt7xO2qUDlUR94QIqEDcU7g6nxbYpqjKbI4rIxyS1KxC0+JYjkCp29fdSuDA8L+rdZkvAJj8go/3D9rFb2bdf6q9tZ4sBxa6tDtuiruqGQMKewE4djeUADXOiQaqjQdoADWL3mylMhik84RHdIIksSYnP55Man9RlckS5SI4ikOT5JjNcek27BJqgoAeFBOnMHZCDJpxHRsQ7KORY0rcaB2eOY45l/PBR5Ky8WBGHD3zH2Jw5TtixD3V5eY5KqrPElORo2ndViu10Jn1sPGDXbevH0/G5neZc+pjhIqk+NpCLGdjXDOzhDvAF1vHoYezbK6gad3X3+UZdLr5dzB3Rt4uZm1cDbCjFbXXHcsZSs1xh14E1LN+xlCxDlnO2uWJ5y/KSZcByzDYR9e1PdragMmlsR2QXuzZ/hdxSvGLpgh3+wn97bT1KxbJt7vOixKtq0e42ZXOxqJtdXgl8M55G4ofgkRo0D/4/I3/BM0LHJX/pMfnzN0CKFQ8jsNcgHtssz5CTwH8tQDj+Pl/ir549XhPr0TM=",
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
            if isinstance(clue, int) and label.startswith("arrow"):
                arrow_direction = label.split("_")[1]
                self.add_program_line(yaji_count(clue, (r, c), arrow_direction, color="gray", unshade_src=False))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
