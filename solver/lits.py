"""The LITS/Inverse LITSO solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, avoid_rect, count_shape, general_shape


def avoid_area_adjacent_same_omino(num: int = 4, color: str = "black", adj_type: int = 4) -> str:
    """Generates a constraint to avoid area adjacent ominos with the same type."""
    tag = tag_encode("belong_to_shape", "omino", num, color)
    tag_adj = tag_encode("area_adj", adj_type, color)
    return f":- {tag_adj}(A, A1), A < A1, {tag}(A, _, _, T, _), {tag}(A1, _, _, T, _)."


class LitsSolver(Solver):
    """The LITS/Inverse LITSO solver."""

    name = "LITS"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZda9swFH3Pryh61oOlK1mS37ou3UvXfaRjFBNCmqZrWIq7pBnDIf99R/LVxFhhg5XCYLi+Pr0+vvdYx5Ky/bKbb5ZSVfGPvMQVh1E+ndrX6az4uFg9rJfNkTzePdx2GwAp35yeypv5ersctcyajvZ9aPpj2b9qWqGEFBqnElPZv2v2/eumH8t+gltCeuTOBpIGHBf4Md2P6GRIqgr4nDHgJeBitVmsl7OzIfO2afsLKWKfF+npCMVd93UpWEf8f9HdXa1i4mr+gJfZ3q7u+c52d9193onc4iD740Hu5BG5VOTSD7n0uFz9JHLX991jQsP0cMCAv4fUWdNG1R8K9AVOmv0hKopRpXiZ4mmKOsULUGVPKb5MsUrRpniWOONmL7TSUutaNBreKgscGDupSQ1YAxvGVAEbxnjW8LNkgP2AjZLaWsbgWOYYcGzmoJflXgb1a65v8KnWesAWnJo5FhzHHAuOY04NPY711OjruG8dP/nMCcA0YAe+Z74jYMcYvTz38sgHzntoDqzZe0kV1/QBmGsGzLeKawYnSbHOAI4aOFQpYMuYgIf6FOeqNow1cM3YAHvGtSSqBqyRJ85rCxwYQ5sZtBF8IfaFDOpbro/xpzz+GsuB5nfUGB+uD8+BdfGX+B0JY0KmeGo4b6h8D9Ffk31HfeOKj/kbiD5mDRZ9a+5bo2ZNxbvse/Qr++7AcdlHU7z2qngdvcv+evTyxbviL/oG7huQD6F4xP7CT2BbPGJPcQVmjoo+Zu9M8Tf6lf2NHmVPMeakc94Vf6N3OvsYiteYa8RzEFfg7K8r3wCBb5hvou/8vcEXMtl39E1eHOLyFqf+SYomxTotCS6uLX+4+ogsENr8Uy1Fv9XW0rCj/XzYfy83HbVistvczBdLbAPj60/Lo/NuczdfC+y3h5H4JtLZUty+/2/Bz74Fx8Gvnnkj/tuZ2WJcsUT0b6S4383ms0W3Fvj9JlO++iX/7Ooxfaej7w==",
        },
        {
            "data": "m=edit&p=7VZNb9QwEL3vr0A++xB/xs6tlC0cymeLUBWtqu0SaMWiLdsuoFT733l2njctAnGgqoSEtrFfnfHMezMTJ1dfNvN1J1WV/kyQmPGzKuRLB5+vir/ji+tl1zySe5vr89UaQMqXBwfyw3x51U1aWs0mN31s+j3ZP21aoYQUGpcSM9m/bm76500/lf0RbgkZsHY4GBnA6QA14Lt8Py3uZ6QqwBfDfQV4Ari4WC+W3enhsONV0/bHUqQwj/OWBMXn1ddOkEb6f7H6fHaRFs7m19BydX5xyTtXm/erTxtRQmxlvzewPfo7tvpe2C6/nf+KZ5xtt0j3GzA9bdpE+u0Ij5qbbaKRRpXHkzwe5FHn8Rimsjd5fJLHKo8uj4fZZtrcCK2d1NqLRqOcGl2ha+IaOBCjY3QkjlKbasCmAlbEClgTa2BDbIAtsQV29KNGrIB1WQcfw1gGsSxjWcSyjGVhbxnLIpZlLAv/ln4s/FjqstBl65FPwRYaPX16+Ky5t7a3MOxr8nfgU5vRv4ujTaDPUEtTDT4xS6MGP5ilYQ4xS8McYgamvapHXBnsLT5hXzFujbiBfpBzQ72YpSEf48ItDJ8u0AY+XT1yKHlLdbGstUWtPXPrkduaOayRw8haRHCuLHla8KR/nCyGPYAZ/j3jemk89SKHO+zhh/k3qMUOo0aGNTIq5cowFjQq5jxCe1VqhDrGUsdUr1Jf1MsXjakfuNdBr6den05D6g3QG6k3grMiz3SEaurV0Guo16Q8U6+DXkee6NsdRj8b9rNBn5vS5xF6FTkHcI7k7ME5kLMDZx/Hnnelt/EsuPJMwd4Ve/jxxQ9yEop/7I0lLvhU5FOBpy48kXPDnJvUM6yFU6NGBY2K9gr2uvQS7G2pY7JnTyLPI069R84BumKpY9z5zHkIxQY1Cm60D6xLfnNRI3pb1+VMwF72NtZ2exEfcdmHzu/6P9tbO9ZFJY3bdOSno3E/jzaPPh+ZdR5DOYV/fzqHOwe14HOeQoX7OrX/QHM7ac3wvr/7c//e2mzSiqPN+sN80eE1OX3/sXv0rFtedmuBr5HtRHwX+Wrx4HpZ//9CeeAvlJT76iG+U+7xwWyRVnwo9C+luNyczk8Xq6XAx61M63hsfl5/WCHb1NXtbPID",
            "config": {"invlitso": True},
        },
        {
            "url": "https://puzz.link/p?lits/24/24/0000000o01lnmg5dvc0dntsq94ia94i814i914i976i94i294i294i8t4i90ci94ki94s294j094ia14i9pki944i94o1mregamtm0rddc00010002002dhm02i14080044vvvk6001os0001vvvq1g00a4000sfvvvsc003p80073fvvq700080000g3vvu100021g0087vvv8114102295g296oo",
            "test": False,
        },
    ]
    parameters = {"invlitso": {"name": "Inverse LITSO", "type": "checkbox", "default": False}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_rect(2, 2, color="gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

        color = "not gray" if puzzle.param["invlitso"] else "gray"
        shapes = ["L", "I", "T", "S"]
        if puzzle.param["invlitso"]:
            shapes.append("O")  # add O shape for Inverse LITSO

        for i, o_type in enumerate(shapes):
            o_shape = OMINOES[4][o_type]
            self.add_program_line(general_shape("omino_4", i, o_shape, color=color, _type="area", simple=True))

        self.add_program_line(all_shapes("omino_4", color=color, _type="area"))
        self.add_program_line(count_shape(1, "omino_4", _id=None, color=color, _type="area"))
        self.add_program_line(area_adjacent(color=color))
        self.add_program_line(avoid_area_adjacent_same_omino(4, color=color))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
