"""The Firefly (Hotaru Beam) solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import convert_line_to_edge, directed_route, route_turning

drdc = {"1": (0, 1), "2": (1, 0), "3": (0, -1), "4": (-1, 0)}
dict_dir = {"1": Direction.RIGHT, "2": Direction.BOTTOM, "3": Direction.LEFT, "4": Direction.TOP}


def restrict_num_bend(r: int, c: int, num: int, color: str) -> str:
    """Generate a rule to restrict the number of bends in the path."""
    rule = f"reachable({r}, {c}, {r}, {c}).\n"
    rule += f"reachable({r}, {c}, R, C) :- {color}(R, C), grid(R1, C1), not terminal(R1, C1), reachable({r}, {c}, R1, C1), adj_line_directed(R, C, R1, C1).\n"
    rule += f":- #count{{ R, C: grid(R, C), reachable({r}, {c}, R, C), turning(R, C), not terminal(R, C) }} != {num}.\n"
    return rule


class FireflySolver(Solver):
    """The Firefly (Hotaru Beam) solver."""

    name = "Hotaru Beam"
    category = "route"
    aliases = ["hotaru", "hotarubeam", "firefly"]
    examples = [
        {
            "data": "m=edit&p=7VZNbxoxEL3zKyKffVh/7seNprQXStomURStECJk06CCSCFUqRH/vePxJgvjjVDSKqdo2dHwPH77bL/1evVrPV5WXGj/UxlPuIDLpAneOrV4J/V1Nr2fVcUR767vbxdLSDg/GfCb8WxVdUqBXcWws3F54brcfS5KJhmv7yF334qN+1K4AXen0MSglrs+ZIJxCWmvSS+w3WfHARQJ5IOQW0gvIZ1Ml5NZNeoHoq9F6c4488/5gL19yuaL3xUL3fD/ZDG/mnrganwPY1ndTu/qltX6evFzXdeK4Za7bpDba5GrGrnqSa5qlyv/h9zq+kf10KY0H263MOPfQeuoKL3s8ybNmvS02Gy9pA1TVrIwHg4EwKds5gG1g6SaIpmkSJ48TlaN6ESxsOQNYkgvLXKKSMqspaE8ChXqHURLWmP0/rC0jYhTQyVnkZxc0Jo8JcR5vg8YoQiLkdYjZgdRmvAabQmNSSiNFaTEYp9kB0kF7ZTtPwmWXeDiXz4tvuTsZrqsbmZ/0J61AwRF0QWKougETVF0A60NjqC8wRVUQ3AG5Q3uiGrRIdHTVNsoglMiBnRLVGvbxhZsE9VmrXrRPlEtWijSiz6itcFMEYqGoqMIpqIagrEiBnRXVIsOi1HbojdYLdKQxTMJZvuElpMYz2AL4k5h/IgxwWgw9rGmh/EC4zFGjdFiTeo3sRdtc7uuf50cZjNYtTzzr4eEbyNMnzoosTQpF63XO14fD0rWg4/Z0WCxnI9n8EkbrOdX1fLxPxwfth32wPAGCwqu308Ub3+i8LOfvPEL96/vf+n6fpPiJmPcnXB2tx6NR5MFeAzm7kBjr3nLn2vOEq7y53sfaD5Abv3pW76uN+xTL6V985WDnXHY+Qs=",
        },
        {"url": "https://puzz.link/p?firefly/10/10/4.40g20c32j1.b3.h32d41a23c4.d3.b2.g3.j2.a3.e1.d1.b10h30", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="terminal"))
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white", directed=True))
        self.add_program_line(adjacent(_type="line_directed"))
        self.add_program_line(directed_route(color="white"))
        self.add_program_line(route_turning(color="white", directed=True))
        self.add_program_line(grid_color_connected(color="white", adj_type="line_directed"))
        self.add_program_line(convert_line_to_edge(directed=True))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            shape, style = symbol_name.split("__")
            if shape != "firefly":  # pragma: no cover
                continue  # warning: incompatible encoding with penpa+/puzz.link

            dr, dc = drdc[style]
            clue = puzzle.text.get(Point(r, c, Direction.TOP_LEFT, "normal"))  # the text is also placed in the top-left corner

            if isinstance(clue, int):
                self.add_program_line(restrict_num_bend(r + dr, c + dc, clue, color="white"))

            self.add_program_line(f"terminal({r}, {c}).")
            self.add_program_line(f"pass_by_route({r}, {c}).")
            self.add_program_line(f':- not line_out({r}, {c}, "{dict_dir[style]}").')
            self.add_program_line(f':- line_out({r}, {c}, D), D != "{dict_dir[style]}".')

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
