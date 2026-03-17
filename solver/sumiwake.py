"""The Sumiwake solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent, count_covering
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect


class SumiwakeSolver(Solver):
    """The Sumiwake solver."""

    name = "Sumiwake"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZNbxMxEL3nV1Q++7D22LvrvZVSuPQDSBGqoqhKQ0ojUqWkDUJb5b/z7J3tZsugVhUgkFC69utk9s2b8djxzZf1ZDXTJot/VGrM+DhTpseWeXoy/pzMbxezakfvrm8vlysArY+P9MVkcTPTgxF7jQd3dajqXV2/rkbKKK0sHqPGun5b3dWHVb2v6yG+Uroca3W1XtzOp8vFcqWSzcDvoHnRAu538EP6PqK9xmgy4CPGgKeA0/lqupidHTaWN9WoPtEqxn6R3o5QXS2/zhRri/9Pl1fn82g4n9wiwZvL+bXShC9u1h+Xn9eqjbDR9W6TwfCJGVCXAd1nQHIGtp/Bwa/PIIw3GyzOO+RwVo1iOu87WHZwWN1toqw4mjSeVnfK2hw8RvdLDHMhm0vRTFY2k2x2otllslnmdlG3/dFcimYvh/ReNss1yWWBuZHNsu5CNpeyklJcBspEJWR+YjZSTciISsiIyZORlRixIciK9Sa52YgyUaDcVUTiEhMF0VvuKnKyQOdFbifoxgZ6lbaRTeMJdpmuKY0v05il0afxIPnsxw2XF9rmSMHGHsFpnIcGF0an5kjYAhNjAnaMHbBn7IFzxjjRi4I5A3DG9gzYNDjAP7B/gH9g/wA9gfUE6AmsJwSd+symfgM2jA2wZWyBiTEBO8YOmHUaxLXMaaHNcV4OeXnW4ItOZ6xDye+Wvq/HcCyDWLZ5F7Mmx9octPk2LjiJOQmcju0OnJ45fejXuWQ9ZdHP13iO6xE3cFzo4VwwIy6/a1Fbx/V3qL/ntfNYu1abjxp4LZztsEX9HfcA8krHbcvJ+SZOzhdz33/b3sYi8Ls2Fnhy1paDJ2f/HP4587iywwTNjjUQ6kOu4yTqOF2rrej7b9s5FsUrieU+segTavwx67SHE4615d5D7vfYoN9szjiui+04jek4La+X9X3/bXsby4CfmJ/A41ibAw/3DGZNXEOcSh02UXOrAT1jyo7TFB0n9yHmvv+2PcXaxOtEPCr20ujSmKcjpIg/40/8oVcxoTIGaTgf/Oo/7+h6VNuImotm/+P/Pdt4MFLD9epiMp3hKrb/8dNs52i5upos8N/wcnI9U7gObwbqm0rPCJ0eX/p/Q/6Lb8hxobJn35N/0455RM4IBceeqo+1ul6fTc5Q7FSvZDcP7DT+4+qx5ceD7w==",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent(color="gray"))
        self.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            if d == Direction.TOP_LEFT and symbol_name == "circle_M__1":
                self.add_program_line(count_covering(1, (r, c), d, color="gray"))

            if d == Direction.TOP_LEFT and symbol_name == "circle_M__2":
                self.add_program_line(count_covering(2, (r, c), d, color="gray"))

        for r in range(puzzle.row):
            borders_in_row = [c for c in range(1, puzzle.col) if Point(r, c, Direction.LEFT) in puzzle.edge]
            for i in range(len(borders_in_row) - 1):
                b1, b2 = borders_in_row[i], borders_in_row[i + 1]
                self.add_program_line(avoid_rect(1, b2 - b1 + 2, color="not gray", corner=(r, b1 - 1)))

        for c in range(puzzle.col):
            borders_in_col = [r for r in range(1, puzzle.row) if Point(r, c, Direction.TOP) in puzzle.edge]
            for i in range(len(borders_in_col) - 1):
                b1, b2 = borders_in_col[i], borders_in_col[i + 1]
                self.add_program_line(avoid_rect(b2 - b1 + 2, 1, color="not gray", corner=(b1 - 1, c)))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
