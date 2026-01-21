"""The Ichimaga solver."""

from typing import Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import target_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import convert_line_to_edge, route_turning, single_route


def restrict_num_bend(r: int, c: int, target: Union[int, Tuple[str, int]], color: str) -> str:
    """Generate a rule to restrict the number of bends in the path."""
    rop, num = target_encode(target)
    directions = [
        (Direction.BOTTOM, r + 1, c),
        (Direction.RIGHT, r, c + 1),
        (Direction.TOP, r - 1, c),
        (Direction.LEFT, r, c - 1),
    ]

    rule = ""
    for d, nr, nc in directions:
        rule += f'reachable({nr}, {nc}, {nr}, {nc}) :- line_io({r}, {c}, "{d}").\n'
        rule += f"reachable({nr}, {nc}, R, C) :- {color}(R, C), not intersect(R, C), not intersect(R1, C1), grid(R1, C1), reachable({nr}, {nc}, R1, C1), adj_line(R, C, R1, C1).\n"
        rule += f":- #count{{ R, C: grid(R, C), reachable({nr}, {nc}, R, C), turning(R, C) }} {rop} {num}.\n"
    return rule


def count_edges_around_vertex(target: Union[int, Tuple[str, int]], src_cell: Tuple[int, int]) -> str:
    """A rule to compare the number of the edges around a vertex to a specified target."""
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    v_1 = f'edge({src_r}, {src_c}, "{Direction.LEFT}")'
    v_2 = f'edge({src_r - 1}, {src_c}, "{Direction.LEFT}")'
    h_1 = f'edge({src_r}, {src_c}, "{Direction.TOP}")'
    h_2 = f'edge({src_r}, {src_c - 1}, "{Direction.TOP}")'
    return f":- {{ {v_1}; {v_2}; {h_1}; {h_2} }} {rop} {num}."


class IchimagaSolver(Solver):
    """The Ichimaga solver."""

    name = "Ichimaga"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7Vbvb7JIEP7uX9Hs125ysCgiyX2w1vZtz1L7vhqvEmNWi0oLbg/B9jD+751dNLIL9noxae7DhTCZeebH7uzAA6u/Ehp52ILLsLCGdbiMKhE30Rri1nZXz48Dzz7DzSResAgUjO8dPKPBysO3j4tOizXfLpt/rq14ONSvteRGGzxfPZ//DP+48Y1Iv3Ks7l33zifz5o/WxYPZPje7yaofe+uHUL947g97s+5g3iB/t51hNR3ea7Xb4ey3dbP/e8XdbWFU2aQNO23i9Np2EUF4d49w+mBv0js7dXD6C1wI6yOMwiSI/SkLWIT2WNoBTUeYgNo+qAPh51orA3UNdCfTTVAfQZ360TTwxp2sUNd20x5GfO0Lkc1VFLK1xxeDNGFPWTjxOTChMZzeauG/ImyAY5U8sZdkF6qPtjhtZh20v9gBFBEdVDM164BrJR3wxk7uwHuae+8lm2+MtluYy0/Y/th2eSf9g2od1F/2BqRjb5BesyBXxyaGfCinm5piE7BJzq7ytc5gFHukzjOMnF1XIyy9gBjyKlYhp8EjZMSUcoimVoUXRI7Q1aqE8G5yEaSmRhiFqgaPyeUYhapVnpOLqMpnSmr8zPK20okyAyLNAAali3E9CnklJBGyB9PEqSHkpZCakDUhOyKmLeRAyJaQVSFNEVPnz8O/emJO3w4yNJhCw8KgwJC5Ak8hFs+R8Y97dYkpmPFw1b7XHlVc1Ib378xhUUgDeDWdJJx40d4GYkQrFoxXSTSjU2/svdNpjOyMm/MeCVuKGhIUMPYa+MuyCnuXBPrzJYu8UhcHOWccKcVdJaUmLHpS9vRGg0DuRXy0JChjNgmKI6CtnE2jiL1JSEjjhQTkSFqq5C2Vw4ypvEX6QpXVwsNxbCvoHYkbGIvwYf7/FftvfsX4jLRvZqZTidKFswYuq2P+VcXpPUavyZiO4bgR/DDhr7kzJjzBXWuc4j5aHMj6mIMUHN8+GPGis+gT1j04VbiEewH9hH5z3jL8CNPmvCpeoFW+2SKzAlpCroCq/ApQkWIBLLAsYEeIlldVuZbvSqVbvlSBcflSedJ1kT9d+CGdUzSqfAA=",
        },
        {"url": "https://puzz.link/p?ichimaga/14/10/cdlcicdehcg2ddkbhddgdhbjbhcbcj8bg6bbjdhbgcgbbi6cgcbc", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_turning(color="white"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(convert_line_to_edge())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            self.add_program_line(f"pass_by_route({r}, {c}).")
            self.add_program_line(f"intersect({r}, {c}).")
            self.add_program_line(restrict_num_bend(r, c, ("le", 1), color="white"))

            if isinstance(num, int):
                self.add_program_line(count_edges_around_vertex(num, (r, c)))
            else:
                self.add_program_line(count_edges_around_vertex(("gt", 0), (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
