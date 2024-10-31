"""The Gokigen solver."""

from typing import List

from .core.common import direction, display, fill_path, grid
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def slant_rule() -> str:
    """Generate slant rules."""
    rule = ':- grid(R, C), grid_direction(R, C, "ul"), not grid_direction(R - 1, C - 1, "dr").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "ur"), not grid_direction(R - 1, C + 1, "dl").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "dl"), not grid_direction(R + 1, C - 1, "ur").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "dr"), not grid_direction(R + 1, C + 1, "ul").\n'

    rule += "grid_direc_num(R, C, D, 0) :- grid(R, C), direction(D), not grid_direction(R, C, D).\n"
    rule += "grid_direc_num(R, C, D, 1) :- grid_direction(R, C, D).\n"
    rule += ':- grid(R, C), grid(R + 1, C + 1), { grid_direction(R, C, "dr"); grid_direction(R, C + 1, "dl") } != 1.'
    return rule.strip()


def no_loop() -> str:
    """Ensure there is no loop in the grid."""
    rule = "reachable(R, C) :- grid(R, C), not grid(R - 1, C - 1).\n"
    rule += "reachable(R, C) :- grid(R, C), not grid(R + 1, C + 1).\n"
    rule += 'reachable(R, C) :- grid(R, C), reachable(R - 1, C - 1), not grid_direction(R, C - 1, "ur").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R - 1, C + 1), not grid_direction(R, C + 1, "ul").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R + 1, C - 1), not grid_direction(R, C - 1, "dr").\n'
    rule += 'reachable(R, C) :- grid(R, C), reachable(R + 1, C + 1), not grid_direction(R, C + 1, "dl").\n'
    rule += ":- grid(R, C), not reachable(R, C).\n"
    return rule.strip()


def convert_direction_to_edge() -> str:
    """Convert (diagonal) grid direction fact to edge fact."""
    rule = 'edge_diag_down(R, C) :- grid_direction(R, C, "dr").\n'
    rule += 'edge_diag_up(R, C) :- grid_direction(R + 1, C, "ur").\n'
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
    solver.add_program_line(direction(["ul", "ur", "dl", "dr"]))
    solver.add_program_line(fill_path(color="grid"))
    solver.add_program_line(slant_rule())
    solver.add_program_line(no_loop())
    solver.add_program_line(convert_direction_to_edge())

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be an integer."
        solver.add_program_line(f":- #count{{ D: grid_direction({r + 1}, {c + 1}, D) }} != {num}.")

    solver.add_program_line(display(item="edge_diag_down", size=2))
    solver.add_program_line(display(item="edge_diag_up", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Gokigen",
    "category": "draw",
    "aliases": ["slant"],
    "examples": [
        {
            "data": "m=edit&p=7VZNb9s8DL7nVwQ6vQN0sGxR/rh1bbZLl25vMxSFEQRu6qVBk7rLxzA4yH8vSQeIRHQbdml3KAwTfMKvRxSleP19W61qbUAbq5NMR9rg46JMQxrpzAK/0eEZzTeLuujrk+3mrlmhovXFUH+rFuu6V1IgPuPers2L9kS3H4tSxUof3rFuvxS79lPRDnV7iSaFvro9R80oHaM66PxJvWI7aaed3USoDzvdoXqN6nS+mi7qyXmX6HNRtiOtqM57jiZVLZsfterCGE+b5c2cfripNriW9d388WBZb2+b++3B14z3uj3p6A6eoZsc6ZLa0SXtdejm4/0e2/4/Ep4UJXH/elSzo3pZ7FAOi51KshRjcac1xmO6JMsEzkOc2wDbyAicIE48TP6xhyHEJgr9DeXz7XGIY2GPKZ9XPw7524TiPWypno9Ffkv5PD7WCTvl93HYHwuCHwg+QP6e3VF9r56j/vl2US8l/j6mfF58RvFevYz679tF/3m/PXtO6/Xic5oPzz8P1wu8/0c7iP2GKIyHSMSbsL9gyP/IB0y4fhD7D3G4XhDzALGonwh7Eq4feD48fyvqWbE+G54fgLDfAGG/AQQfF84/iHkAJ/im4fmDVORPBZ8snHfg+fD8eT48nIfnGXLhz+ffx2K/8nC/XBT200Xh+hzPy7GeMxKH8+Ji/zzjJWb4Krtm+YFlzHKEN51uE5ZnLCOWwPKcfQYsr1iesrQsHfukdFf+1W36AnRK1/0zP/ekb5ZfW8a9Ug1uZ3X/bF7Nmodqgf+fw+3ypl71h81qiRg/WPY99VPxiyNqtH37hnmlbxjaguhfO3t/oFNid/F7KdH0TaTbC60et5NqMm1w1LCFvze/+FrwKlHrRfWw6f83a+7ns/rhnRr3ngA=",
        },
        {
            "url": "http://pzv.jp/p.html?gokigen/40/25/hbg1bha6ah66bcbh7c98d8cdjdk672817chc717die62b8dcg8c26di32ck3d287271617262bg31222c88e2bddcc3bkdeg87dc777228ddg1cehdch6cb2cb122b73d3c26b31377c7e71cc8clbg8bh317677c6d7b63716eh26d2b8c9ch31c7ddj28277d77bg732cg27c61cg83268871ci626b8681cieicg2ddjdi6277226ch8d3d7dgec2cg73dd63622d3cb172b62667cc1c66d37226263c7cdg8d7bg7273cg78cb9c77cg22dg061661668dge71b778c76bgcg717c7cd376677173bgdg81b9dc8dgch231ch8ce897cg7b631682cgcckcjdg318277cg4ceh6166cgb6cc268173cgeg2173c27d367328cgc267di6bi7bg77dg769cg78d8d22ba656776bgb1bibajb",
            "test": False,
        },
    ],
}
