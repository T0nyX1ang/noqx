"""The Dotchi Dotchi Loop solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, defined, display, fill_line, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_straight, route_turning, single_route
from noqx.rule.variety import classify_area


def dotchi2_constraint() -> str:
    """Generate a constraint for dotchi dotchi loop."""
    rule = ":- black_clue_area(A), area(A, R, C), black_clue(R, C), not turning(R, C).\n"
    rule += ":- white_clue_area(A), area(A, R, C), white_clue(R, C), not straight(R, C)."
    return rule


class DotchiDotchiLoopSolver(Solver):
    """The Dotchi Dotchi Loop solver."""

    name = "Dotchi Dotchi Loop"
    category = "route"
    aliases = ["dotchi2"]
    examples = [
        {
            "data": "m=edit&p=7Vhbb2NFDH7Pr1id53mY8dzzVpaWl7ILtAhVUVV1u4FWtKT0glCq/ne+mfjkdMFWaQUSSKso5zgejy+f7bnk9tf705ulccU4Mr4Yaxw+mciEGkx0qX8tfw4v7i6X8zdm5/7ufHUDwpj3e3vmx9PL26WZLVjsePawrvP1jll/NV8MNJj+dcOxWX87f1h/PV8fmfUBhgbjwNsH5QZDIHcn8oc+3qi3G6azoN8xDfII5NnFzdnl8mR/w/lmvlgfmqHZ+aLPbuRwtfptOWym9d9nq6sPF43x4fQO0dyeX1zzyO39x9XP98PWxHB1f3l3cba6XN0M7O2jWe9sQtgXQvBTCH4bgpdDoH8/hCqH8Ij0fIcgTuaLFs/3E3kwf3hsDran68+j+cMQMqY686mnQ6gSNzZZ+jM3OZFbJG4WZXMQuVHyISdJtpDIFTVU0YdKomwQuSI6zjqZ7SV7ziZR2nmZLTrinJgR50TwHVlRCckOklgZzougOl9FJcHKbBmqIKbRBTn4ICMoV7QLMiZRrAYXi6gkyplPMrBJjjKJpeaSDGwSC94lOcosI5jl4IvsSZELosh4FxmqKme+yphU2WQVMSErJo2sGDzJDUhWrCqyUZYW8SYrBk9W7AaSu5hIjtKLSwF52UEv1gl5cYUgL/sdZE/kliJ5l6AoppiinJ0oYxJlT6JYgxRlB+W+pCRjkuRwshxOlrMj72WUZQezXCdF7B0qsidyF5PUadj09/rWT/15iJOBWfv+/LI/bX/G/tzvMrv9kBBwYgT01I4G7dRYOo23iW2Jb/yIU2WLfqSjZ9qDZn6FPFmeW5/Q4Lu6kcl+0pObzlGPBU0bOlToZLuhmBB4bvXtZMt0P+GyfvjsC+uEnsp6qpvoBJ0Ns64zm5DqRIcnczPL5DZ341v00B8Zk4hYYmUaMSaOEefvkYZN+BbYN/jpR2zt5ENp/tgtHZ1jeQf50a6Hrci2ImiONzZ/MtN565uv2fg60gV0ZRq2LNuy8MFubPlct3TnE2PVbhCBcQ7+UzpFxjM8oRt/I+NL0896LPQQzyXIB8YhJMgz5qlMOKRoQsmMCfJSWKZAptRpbhhjD0/waVgx5qjPyPUZI/CMNNVY5HipTrSFLWKsCnyw7AP0h5yYDx8c++mgx7NOT9v67znK7FtGXhh/vE2ijS28TQrsG7BKjBXekAksEyAz5hp1VbjGkkWNcZ0kxFVGPR56IuuJ0JNZT4Ye9iG0uTTNHekCWzZt6VgYT+CQGAeMb2nMw1y2i7xHzjveoHku8hg5j3hjbmU9wMEzDh44jDlq8ol9SKjtNNoChpz3WMoTuvG5H9E7iXsHb9AcF3ptS6PGYrWTTq49jEOG15+MuuLewbqFtYtxRr4i9wXeoNlnQuyB4w1x8tm6rUxAf8Wxv1qvlbHfUT/FTXa5ZvAGPa5FqLe2f9Bju4y2pfptf4b+LOPFT78Qlmfuhi/dLIbWeXDUt0Y1DUK/2T9EB1Oflpv92QLy7tlP/CzzX5E5ni2G/Ytflm/erW6uTi8HM+x+/OnJr4Pz0+vlcDx7eJwNvw/9u/j879H/4d+jlir76iWj/2mzfr/5i6S9+38OnWhHhE6kLvK6k+izK8kzji9QXjjPNT+u709OTxD9gKI0r+JXmY+znch3zmsDQRnwURnAnq8MKE45nAzkgaK4i/uxpsppA4qqqmjKSnhVC4K0IILmUkladAqCuOgrA1GxgZugMqBVCK6UygApiJBWhLi0KgNVsxG0okraQNGqLWglYtUSUeJwQUmU0yJ3aoBqO5GmyirGi4ZI1fLktbLS+o/U/itqvakVqgROUXVXK92o9U1UjCclcC1LWgs4pyXJa6uCU8tTwTxr65Fag9qSTgp+GkrOKhO0KtCWVJWvwaqtXi5rsQUN1qoVjdcK02vVVLSuyNqypm6JVdsbkroFaDai1pJa4biiQWK1ztMKgay6H6sZ1BpDH1BXqReegbSufylf1r9v+EqpD+KW+ZfBf+xC+3fPnLjAHs/+AA==",
        },
        {"url": "https://pzplus.tck.mn/p.html?dotchi2/7/7/h8ka54i90f0107s01ojj001k50976l003li", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black_clue"))
        self.add_program_line(defined(item="white_clue"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_straight(color="white"))
        self.add_program_line(route_turning(color="white"))
        self.add_program_line(classify_area([("black_clue", "white"), ("white_clue", "white")]))
        self.add_program_line(dotchi2_constraint())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_L__1":
                self.add_program_line(f"white_clue({r}, {c}).")
            if symbol_name == "circle_L__2":
                self.add_program_line(f"black_clue({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
