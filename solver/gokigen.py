"""The Gokigen (Slant) solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import direction, display, fill_line, grid
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.loop import convert_line_to_edge


def slant_rule() -> str:
    """Generate slant rules."""
    rule = ':- grid(R, C), line_io(R, C, "ul"), not line_io(R - 1, C - 1, "dr").\n'
    rule += ':- grid(R, C), line_io(R, C, "ur"), not line_io(R - 1, C + 1, "dl").\n'
    rule += ':- grid(R, C), line_io(R, C, "dl"), not line_io(R + 1, C - 1, "ur").\n'
    rule += ':- grid(R, C), line_io(R, C, "dr"), not line_io(R + 1, C + 1, "ul").\n'

    rule += "grid_direc_num(R, C, D, 0) :- grid(R, C), direction(D), not line_io(R, C, D).\n"
    rule += "grid_direc_num(R, C, D, 1) :- line_io(R, C, D).\n"
    rule += ':- grid(R, C), grid(R + 1, C + 1), { line_io(R, C, "dr"); line_io(R, C + 1, "dl") } != 1.'
    return rule


def no_loop() -> str:
    """Ensure there is no loop in the grid."""
    rule = "reachable(R, C) :- grid(R, C), not grid(R - 1, C - 1).\n"
    rule += "reachable(R, C) :- grid(R, C), not grid(R + 1, C + 1).\n"
    rule += 'reachable(R, C) :- grid(R, C), reachable(R - 1, C - 1), not line_io(R, C - 1, "ur").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R - 1, C + 1), not line_io(R, C + 1, "ul").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R + 1, C - 1), not line_io(R, C - 1, "dr").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R + 1, C + 1), not line_io(R, C + 1, "dl").\n'
    rule += ":- grid(R, C), not reachable(R, C).\n"
    return rule


class GokigenSolver(Solver):
    """The Gokigen (Slant) solver."""

    name = "Gokigen"
    category = "var"
    aliases = ["slant"]
    examples = [
        {
            "data": "m=edit&p=7VZNT9tMEL7nV0R7aqU97No764/LKwppLzS0L1QIWVZkghsiEkzzUVWO8t+ZGUf17ooicYELsjyaJ/P1eHZ2s+tf22pVSw1SGxmnUkmNj1WphETJ1AC/6vBczDeLOh/Ko+3mtlmhIuXZWP6sFut6UFAgPuVg12Z5eyTbL3khIiEPbynb7/mu/Zq3Y9meo0mgr2xPUdNCRqiOOn9SL9lO2nFn1wr1cadbVK9Qnc5X00U9Oe0SfcuL9kIKqvOJo0kVy+Z3LbowxtNmeT2nH66rDX7L+nb+cLCstzfN3fbgq8u9bI86uqMn6MY9XVI7uqS9Dd2s3O+x7f8j4UleEPcfvZr26nm+QznOdyJOk0OslSgxYZym+Auu/V+c+TgzHjZKBzhGHDuY/CMHg4+18v015XPtkY+jwB5RPqd+5PM3McU72FA9Fwf5DeVz+Bgb2Cm/i/3+GAj4QcAHyN+xW6rv1LPUP9ce1EuIv4spnxOfUrxTL6X+i7hfYZMGK9DNwH+uB9V0cmbUAydnRhFOhszvAfBM9HYIZgCUHw8qiNd+z0GTf88HtN8TCGYCIr8HEMwIREH9OLDH/vcDz4zjb4J6Jvg+Q/mdfEB2Jx/4KwAQ8LH+noBgRsAGfBN/T0IS5E8CPqm/B4BnxvHnmXFw5u9xyAJ/PhNcHKxX5q+XVX4/rfK/z/K89PWsDrE/LzZy9zgebZoPuCuWn1lGLC/w/JNtzPKEpWIJLE/ZZ8TykuUxS8PSsk9CJ+iLzthXoFPY7v/6qSd5t/zbUg4KMbqZ1cOTeTVr7qsF/quOt8vrejUcN6slYrzG7Afij+AXR1RL836zeaObDS2Betn95vl/irc/KQpsPl6xYknXKNmeSfGwnVSTaYOTiB1+3vzaxwzuhEKsF9X9Zvhh1tzNZ/X9R1EOHgE=",
        },
        {
            "url": "http://pzv.jp/p.html?gokigen/40/25/hbg1bha6ah66bcbh7c98d8cdjdk672817chc717die62b8dcg8c26di32ck3d287271617262bg31222c88e2bddcc3bkdeg87dc777228ddg1cehdch6cb2cb122b73d3c26b31377c7e71cc8clbg8bh317677c6d7b63716eh26d2b8c9ch31c7ddj28277d77bg732cg27c61cg83268871ci626b8681cieicg2ddjdi6277226ch8d3d7dgec2cg73dd63622d3cb172b62667cc1c66d37226263c7cdg8d7bg7273cg78cb9c77cg22dg061661668dge71b778c76bgcg717c7cd376677173bgdg81b9dc8dgch231ch8ce897cg7b631682cgcckcjdg318277cg4ceh6166cgb6cc268173cgeg2173c27d367328cgc267di6bi7bg77dg769cg78d8d22ba656776bgb1bibajb",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(direction(["ul", "ur", "dl", "dr"]))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(slant_rule())
        self.add_program_line(no_loop())
        self.add_program_line(convert_line_to_edge(diagonal=True))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(f":- #count{{ D: line_io({r}, {c}, D) }} != {num}.")

        self.add_program_line(display(item="edge_diag_down", size=2))
        self.add_program_line(display(item="edge_diag_up", size=2))

        return self.program
