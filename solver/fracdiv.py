"""The Fractional Division solver."""

from typing import Dict, Optional, Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


class SimpleFraction:
    """A simple class to represent a fraction."""

    def __init__(self, numerator: Optional[int] = None, denominator: Optional[int] = None):
        self.numerator = numerator
        self.denominator = denominator


class FractionalDivisionSolver(Solver):
    """The Fractional Division solver."""

    name = "Fractional Division"
    category = "region"
    aliases = ["fractionaldivision"]
    examples = [
        {
            "data": "m=edit&p=7VVbb+pIDH7nV1Tz2pFOLoRCpH0ACt12KaUtiAMRQgEGSJswbEhoN4j/XntCAhPoZS+qzsNqiGV/djy2Z/Kx+jO0fUYNWHqRKlSFpWlF8eQV/CWr7QQuM89oOQzm3AeF0rt6nU5td8XoTW/eqPLyy2X557oY9PvqlRJeK92n+tP5g/fHtaP7ar1ZbN22bh1tVv69Wrkv1M4LrXDVCdj63lMrT51+e9rqzkraX7VmPx/17xTjpj/9sS53fstZuxoGuU1UMqMyja5Mi2iEikclAxrdm5vo1ox6NHoEF6HqgBIvdANnzF3ukwSLGqCphGqg1vZqV/hRq8agqoDe3Omg9kCdOGMWWy3TitqU4L4V8SaqxONrhhvBK8Iec2/kIDCyAxjdau4sCdXBsQon/DnchaqDLY3KcfW1L1YPSZLqUY2rR+1E9dgUVj92/LHLho3/voPSYLuFg3mAHoamhe109mpxrz6aG5BNc0O0UtJ8fHrEKCCgJACEqRCWV/LpkChYF2jBiQtLFa+kVpoRLU2RLB0tI7aMgvCllvDpu2PoYW3oL1DCX4eVOEhTAbHU9EOIF3rSG0HEHvJbWLuE6Ls8uHY5cEl5dOxD7LWPye6VT+uRHjlG5EnfT/JJMYbIk/aTdCbH4Mw/i8G9pE7FjD+cGAy7Lq6DJmQbbgiNdCEvhVSENIRsiJiakF0hq0LmhSyImAu8Y3/rFsaXLD71f1YO0fD6lIpwZxVoT4F56p+WaGm7c4dlfE0b5CxSm8zYWZP7nu3Cx9kMvRHz9/bj3F4yAvRIVtwdrkJ/ao/ZkL3a44CYMUMfeiRsIXJJkMv50nUWpzIkLgl0Zgvus5MuBBnU/k4qdJ1INeL+JFPTi+26ci/in0uCYo6ToMAHAjuwbd/nLxLi2cFcAg7ITsrEFplhBrZcov1sZ3bz9uPY5sgrEY+lU+3//7Jf+L8MD0n5Zi75t9RmwcBTGqLRHSXLcGgPYeYE6RrdwFZHjm/vQnwW3P+Ao/bOLHyCqQD9gKwOvKfwd3jpwJvFj0gIiz3mIUBPUBGgWTYC6JiQADziJMDeoSXMmmUmrCpLTrjVET/hVocUZQ1ybw==",
        },
        {
            "data": "m=edit&p=7Vbvb7JIEP7uX9Hs125y/BBUkstFrfbaa61tNZ4SY1BRacHti2B7GP/3zixysGhL7817l0vuQpjMPDO7++zAPrD5Flq+TatwqVUqURkutazwW5Fq/JYOV88JXNs4o/UwWDEfHErv2m26sNyNTa+Hq5smq79e1H/fVoPRSL6Uwitp8NR+On/wfrtyVF9ud6rd2+6toyzrvzYb93rrXO+Gm35gb+89ufHUH/UW3cGypvzR6ozK0ehO0q5Hi5+29f7PJfPAYVzaRTUjqtPo0jCJQii/ZTKm0b2xi26NaEijR0gRKo8p8UI3cGbMZT5JsOgGPJlQBdxW6g54Hr1mDMoS+J2DD+4Q3Lkzs+Ooa5hRjxJct8FHoks8trVxIRjC4xnzpg4CUyuA1m1WzguhKiQ24Zw9h4dSebynUT1m3/oie5gkYY9uzB69E+xxU8ievU0aP559bbzfw0N5AP4Tw8St9FO3mrqPxg5sx9gRTcahvwAV/uQAlQGtSNKf/aAQqRhpSVQWchWMKodIqWKkHiKVTy6Xk1DJDlS17MAyH5jkYlbJgpowThPGVfTsgpVauiBsZQhb4Rx0mjaccBoigouLCE4kIGXsgYhgHwREw64JiI5kk/MCPU5ODk1fX6LjFgpqKtjlohrcRUFNDfdeVIM7LarB/hTUyPwlKizCLhYWfaGNsoxPurCosAHw3rT58VC47cGJoZHK7QW3Ercatze8psXtgNsmt2VudV5TwTP3l05lfArjF/hvomMqOv+8pJf2z8bjkkla86V91mG+Z7kgc53Qm9p+Gj+urBebwEeGbJg72YT+wprZE/vNmgXEiL9z2YyArflcAuQy9uI661MzJCkBdJZr5tsnUwjawP2DqTB1Yqop8+c5Tq+W64p74X8AAjRz/JkrQoEPn4JMbPk+exUQzwpWApD5bAgz2etcMwNLpGg9W7nVvLQd+xJ5I/w2Var8/0fwL/0jwAckfbcC8U9fdPff0MVYbJj/id6kyTx8QnUA/UR4MtlT+Acak8nm8SNBQbLHmgLoCVkBNK8sAB2LC4BH+gLYBxKDs+ZVBlnlhQaXOtIaXCorN+a49A4=",  # a little bit slow
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

        for (r, c, _, _), symbol_name in puzzle.symbol.items():
            symbol, tag = symbol_name.split("__")
            if symbol == "dice":
                dice_cnt = bin(int(tag)).count("1")
                self.add_program_line(f"number({r}, {c}, {dice_cnt}).")

        all_src = set((r, c) for (r, c, _, _) in puzzle.text)
        frac_dict: Dict[Tuple[int, int], SimpleFraction] = {}

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)

            if (r, c) not in frac_dict:
                current_excluded = [src for src in all_src if src != (r, c)]
                self.add_program_line(
                    grid_src_color_connected((r, c), exclude_cells=current_excluded, color=None, adj_type="edge")
                )
                frac_dict[(r, c)] = SimpleFraction()

            if label == "normal" and isinstance(num, int):
                frac_dict[(r, c)].numerator = num
                frac_dict[(r, c)].denominator = 1

            if label == "sudoku_0" and isinstance(num, int):
                frac_dict[(r, c)].numerator = num

            if label == "sudoku_3" and isinstance(num, int):
                frac_dict[(r, c)].denominator = num

        for (r, c), frac in frac_dict.items():
            if frac.numerator is not None and frac.denominator is not None:
                tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
                region_cnt = f"#count {{ (R, C): {tag}({r}, {c}, R, C) }}"
                total_dice = f"#sum {{ N, R, C: {tag}({r}, {c}, R, C), number(R, C, N) }}"
                self.add_program_line(
                    f":- N1 = {total_dice}, N2 = {region_cnt}, N2 * {frac.numerator} != N1 * {frac.denominator}."
                )

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
