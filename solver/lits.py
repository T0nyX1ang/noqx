"""The Lits solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, avoid_rect, count_shape, general_shape
from noqx.solution import solver


def avoid_area_adjacent_same_omino(num: int = 4, color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint to avoid area adjacent ominos with the same type.

    An area adjacent rule, an omino rule should be defined first.
    """
    tag = tag_encode("belong_to_shape", "omino", num, color)
    return f":- area_adj_{adj_type}_{color}(A, A1), A < A1, {tag}(A, _, _, T, _), {tag}(A1, _, _, T, _)."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for i, o_type in enumerate(["L", "I", "T", "S"]):
        o_shape = OMINOES[4][o_type]
        solver.add_program_line(general_shape("omino_4", i, o_shape, color="gray", _type="area", simple=True))

    solver.add_program_line(all_shapes("omino_4", color="gray", _type="area"))
    solver.add_program_line(count_shape(1, "omino_4", _id=None, color="gray", _type="area"))
    solver.add_program_line(area_adjacent(color="gray"))
    solver.add_program_line(avoid_area_adjacent_same_omino(4, color="gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "LITS",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7Vbfa9swEH7PX1H0rAdLJ9my37ou3UvXbktHKSaENE3XsJR0+TGGQ/73fiedMGOFDToKg5H49OX86e50n2Vl8203Xc+1KfhLQWPEx5kQLxvKeBXyuVxsl/PmSB/vtverNYDWF6en+m663MwHrbDGg31XN92x7t41rTJKK4vLqLHuPjb77n3TDXU3wi2lA3xniWQBhz28ivcZnSSnKYDPBQNeA84W69lyPjlLng9N211qxXnexNkM1cPq+1xJHfx7tnq4WbDjZrrFYjb3i0e5s9ndrr7uhGvGB90dp3JHz5RLfbkMU7mMnimXV/HycpePq+cKrceHAxr+CaVOmpar/tzD0MNRs4c9j9ZEex3tabQ22ktQdUfRvo22iNZHexY5w2avrLHa2lI1FtoaD1wLrrQlk7AFdoKpAHaCMdfJXHLAIWFntPVeMDheOA4cnznI5SWXQ/xS4js8qqVN2INTCseDUwnHg1MJp0Q9ldRTIm8leUt+5DOnBqaEK/CD8CsCrgQjV5BcAf5a/AE111JzCJoKiRlqYIlZY78VErOuNBmpswbHJA4VBjjVhnnAKT7xXrVpLkELEi3IOOCUl0ypiYqELfwkfuuBU83ganKpNoIuJLqQQ3wv8dF/yv23eB1YWaNFfyQ+NAeWNbK+JGsk9IRkjaypE7+DPz8PrK/LuiO+k/isY34GWMdcg0feUvKWiFlKTNYu6856Zd0rcKqsI3JlrQNqzlqzdlnfgFyh167XF3lryVvDX0sPWSPRF3oCi16skWiKEVg4hnXM2oGf9WW9sr6sUdYUPSfpOcZeX9ZO9h3GXmvsNZI9iBE464u5+Rkg8J3woQuJLhiBs+7IG7XApr+KW/8kWhdtGV8JFb9b/vDtg+7IQlUT/tar6Le1tWgHn2g/f/y/5xsPWjXare+mszmOgeHtl/nR+Wr9MF0qnLeHgfqh4tUSH9//j+BXP4K5+cUrH8Qv3Zkt+opXRHeh1eNuMp3MVkuF/286+otf/K9ePbavWi62GzUePAE=",
        },
        {
            "url": "https://puzz.link/p?lits/24/24/0000000o01lnmg5dvc0dntsq94ia94i814i914i976i94i294i294i8t4i90ci94ki94s294j094ia14i9pki944i94o1mregamtm0rddc00010002002dhm02i14080044vvvk6001os0001vvvq1g00a4000sfvvvsc003p80073fvvq700080000g3vvu100021g0087vvv8114102295g296oo",
            "test": False,
        },
    ],
}
