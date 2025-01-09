"""The Regional Yajilin solver."""

from typing import List

from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, count, direction, display, fill_path, grid, shade_cc
from noqx.rule.helper import full_bfs
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_cc(colors=["black", "white"]))
    solver.add_program_line(fill_path(color="white"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
    solver.add_program_line(grid_color_connected(color="white", adj_type="loop"))
    solver.add_program_line(single_loop(color="white"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))

        if rc:
            num = puzzle.text[Point(*rc, Direction.CENTER, "sudoku_0")]
            assert isinstance(num, int), f"Signpost clue at ({rc[0]}, {rc[1]}) should be integer."
            solver.add_program_line(count(num, color="black", _type="area", _id=i))

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Regional Yajilin",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7ZZda+NGGEbv/SuCrudCmg/NSHdpdtOb1P1IyrIYsziptuvWWbdOXLYK/u97ZvS4biFQ6ELZQrE1PpZ1/D4j6x354df9ajeYps5PlwyvPHyTymZTW7Zaj5v142boz8z5/vHddgcY8/XlpXm72jwMs4WOWs6exq4fz834Zb+omspUlq2plmb8tn8av+rHuRmv+agynn1X00EWfHnCV+XzTBfTzqaG57CDwdfg3Xp3txneXE17vukX442pcp0vip2xut/+NlTKkd/fbe9v13nH7eqRyTy8W/+iTx72P2x/3uvYZnkw4/kU9/qZuO4UN+MUN9MzcfMsPjnuZv1++PBc0m55OHDGvyPrm36RY39/wnTC6/6JcV7Gpn+qutrzDT5nqbrGwk7cntjWsBXn44/7E8yVktn9yXXZ1fE+u/kYCr4uZS/LaMt4QyozujK+KGNdxlDGq3LMS2Laxhpr+VrLddQ4OIo9TIzCAe7EXLKO0oUj3Ii5nHPUwh3sJrY1zNQK4+bYhXG9XIvr5VpcL9fhermugYOYzF6ZHZm9Mjsye2X2uEGuxw1yPW6Q63GDXI8bji7zDZqvJ3OrzJ7MrTJ7MrfKHHBbuQG3lRtwo9yAG+UG3Hh0mW/UfFsyR2VuyRyVuSVzVOY2LxtyW9wkN+ImuRE3yY24SW5kvknzjWROyhzJnJQ5krlT5oTbyU24ndyE28lNuJ1cljJXH90Ia74pwcqcOliZO9bE3CaFcRu5HW4jt8PN7VMYt5lc6sCTSx14mi914CkzdeApM3XgKTN1jMvtVhjXyqUXnHqBOrBcesGpF6gDT/OljnHqBerAU2bqwFNm6sByLa6TSy849QJ1YLn0glMvUAfWfOkFp16gDqzM9IJTL1DHuCDX4Qa59IJTL1AHlksvOPUCdWDNl15w6gXqwMpML7hjL/D7/nH98DvaLudnUXlVlpaLMvoytmXJiXmZ/AcL6aesbn8bZ8FZzTfkvz7Cf2/fcraorve7t6u7gZvYFTezs/l2d7/a8G6+v78ddsf3/H04zKoPVdnyfYXb7v//KP71fxT57NefWzt8bnFo0Go3/Ljevl9tzn5f/bTmnFbL2Uc=",
        },
        {
            "url": "https://puzz.link/p?yajilin-regions/11/18/c6c69alhlhg1lhhh4h91gdict8jomt4aemu3001i3tk00uuff1g3vovve81oiu2k1sfvmrto68g2g22g222g222111111111g11g11111h",
            "test": False,
        },
    ],
}
