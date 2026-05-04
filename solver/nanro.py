"""The Nanro solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, fill_num, grid
from noqx.rule.helper import fail_false, full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect


def nanro_fill_constraint(color: str = "black") -> str:
    """Generate a constraint for the number filling in nanro."""
    return f":- number(R0, C0, N), area(A, R0, C0), #count {{ R, C : area(A, R, C), {color}(R, C) }} != N."


def nanro_avoid_adjacent() -> str:
    """Generate a rule to avoid adjacent cells with the same number."""
    area_adj = area_adjacent()
    area_adj = area_adj[area_adj.find(":-") : -1]
    return f"{area_adj}, number(R, C, N), number(R1, C1, N)."


class NanroSolver(Solver):
    """The Nanro solver."""

    name = "Nanro"
    category = "num"
    examples = [
        {
            "url": "https://puzz.link/p?nanro/11/11/9bdcljmcpj6cpj6dpl6mqi46tt8qpltbdmqnljb2nnc4i3g2l23l2n2n2n2n2i3i2n3n3n3n2l43l2g3i",
            "test": False,
        },
        {
            "data": "m=edit&p=7VdNbxs3FLzrVwR75oHk46dubmr34jpt7aAoBMGQHaUxakOpbBWFDP33ztsdatdAiqAo0gJFYYscznLJx+HwYx9/3a22a+Oc/ksx1gCZEFP/c873P8u/q7un+/X8lTnZPX3YbAGMeXN2Zt6v7h/XswVrLWfP+zrfn5j9N/NF5zrT+f63NPvv58/7b+fd4+7d5pddZ/aXqNAZhyfnQ1UPeDrCH/vnil4PpLPAF8AyvPYT4O3d9vZ+fX0+VPxuvthfmU57+6p/W2H3sPlt3TEaLd9uHm7ulLhZPWFIjx/uPvIJY2N3y4PZn/RB709buGUMV8Zw5RiufCJcjucLh1uXhwPE/wEBX88XGvvbEV7Onw8azHMXfEcFDd7SZw6ss6UoH3tlO4d512JoxehfPM0vnnqXuuOsoFjstCi+HAXVYrDTdyUELfpWrGn6NLoX/abJuwcVVAd11qe+T68wWrOXPv26T22fxj497+ucYrg+OONVCQ9vBg8sxAIciANwJI7AiTgBZ+IMXIgLcCWuxkc74GiBHTH6jew3ot/EdhLaKeQL+Eq+ZiNu4JEb8QOP3AjjR24kko/gM/kMvpAv2QQ78MhNcAMfXJrgCJyIA3AkFuBArO8KMbYKxhacBXZsvwJb4oJ+K7HGUIjRr2VsFe1YapuhTyEuyYgd2kQOHRJ1AC/kBTznBbmRRD6Bz+Qz+Eq+hmM8UgV8IIZWVVgfGlZqmMBnxom5Rpn9gqcHxIEXP8ZGPQU6N+yhv1B/j3nxnJceZ3ovw3uZ3svwXqb3MryXmz7wXm6e8RMM3RibT/Bban6DD1PzIfwZ6U/4BGVitBmbn8NYR719bFO9yjgT4kyMM6F+YpwJcaY0+rzhhPYL4yngK/mqWnFe9PzxnC+fJj4HDqyDNSuRdRCzZPJZzy7yRX3VfOhGP1t75KXCn9YSF8x184POeyFWzzR/RiOMWf2DMucC+mRqmKFtpm4ZmhdqXjAXrb62w3WBHGOMHCP4QD6Aj+Qj+Ew+28l4gQvrlDDB8HOhn4uuffq5qD70Z9F3WzsVuLUPHRi/YH6F4+r9z3kX7G9HLKjDfU8ceCFvwTtqUsBbOWJfqE+BPpX6VNWH3qjqDT9q23DV/ZDtYM16rlmvc9HWMvYc8Ry7By/kBXwkH8GnNsY6apXKhNc13sau+wk9AG8L/SxJ26Hm2OeFa0EEfKijPkLe1RFb1HF1xJbtWLTPPRA5cNtDdN8ox7E3jBzjpeZe+yKPS5xE8tG/xG0sUdcR/RDVb20vRQw8s8SDlzjG7ye8Z32va5bteD+JB1jYl6QRa31JI9/ORD2LY9s3dH9rvOe+dNDLlR7dr/s09Gnqj/Tcp6VddP78AlRe3IU69WsZbkTDDejvXCc+E99htsBx4T7xF/+77HK26C532/er2zUuq6fvfl6/uthsH1b3KF3sHm7W27F82V9jWxlfEIdZ93vX/xbqAePk/8+Kf/WzQqfCfv7j4osvpb+y1Bf7S+w3Zv/GdB9316vr2w28Zpf/bMAHNfNiOfsD"
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not gray"))
        self.add_program_line(avoid_rect(2, 2, color="not gray"))
        self.add_program_line(nanro_fill_constraint(color="not gray"))
        self.add_program_line(nanro_avoid_adjacent())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i, color="gray"))

            unclued = True
            for r, c in ar:
                if Point(r, c, Direction.CENTER, f"corner_{Direction.TOP_LEFT}") in puzzle.text:
                    unclued = False
                    num = puzzle.text[Point(r, c, Direction.CENTER, f"corner_{Direction.TOP_LEFT}")]
                    fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                    self.add_program_line(count(int(num), color="not gray", _type="area", _id=i))

                if Point(r, c, Direction.CENTER, "normal") in puzzle.text:
                    unclued = False
                    num = puzzle.text[Point(r, c, Direction.CENTER, "normal")]
                    fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                    self.add_program_line(f"number({r}, {c}, {num}).")

            if unclued:
                self.add_program_line(count(("gt", 0), color="not gray", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"gray({r}, {c}).")

        self.add_program_line(display(item="gray", size=2))
        self.add_program_line(display(item="number", size=3))

        return self.program
