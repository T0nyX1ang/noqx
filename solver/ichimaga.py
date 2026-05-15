"""The Ichimaga solver."""

from typing import Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import tag_encode, target_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import convert_line_to_edge, crossing_route_connected, route_crossing, route_turning, single_route


def limit_turning(color: str) -> str:
    """A rule to limit the number of turning points in the route."""
    tag = tag_encode("reachable", "turning", "branch", "adj", "line", color)
    rule = f"{tag}(R, C, R, C) :- grid(R, C), turning(R, C), not intersect(R, C).\n"
    rule += f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), {color}(R, C), grid(R1, C1), not intersect(R1, C1), adj_line(R, C, R1, C1), (R - R0) * (C - C0) = 0.\n"
    rule += f":- turning(R, C), not intersect(R, C), turning(R1, C1), not intersect(R1, C1), {tag}(R, C, R1, C1), (R, C) < (R1, C1)."
    return rule


def bulb_src_color_connected(src_cell: Tuple[int, int], color: str = "black") -> str:
    """A rule to collect all the color cells that are orthogonally connected to a source cell in a grid.

    This rule is specially designed for magnetic ichimaga.
    """
    r, c = src_cell
    tag = tag_encode("reachable", "bulb", "src", "adj", "line", color)
    rule = f"{tag}({r}, {c}, {r}, {c}).\n"
    rule += f"{tag}({r}, {c}, R, C) :- {tag}({r}, {c}, {r}, {c}), {color}(R, C), adj_line(R, C, {r}, {c}), (R - {r}) * (C - {c}) == 0."  # initial propagation manually
    rule += f"{tag}({r}, {c}, R, C) :- {tag}({r}, {c}, R1, C1), {color}(R, C), grid(R1, C1), not intersect(R1, C1), adj_line(R, C, R1, C1), (R - {r}) * (C - {c}) == 0."
    return rule


def avoid_magnetic(color: str) -> str:
    """A rule to avoid two connected clues have the same number."""
    tag = tag_encode("reachable", "turning", "branch", "adj", "line", color)
    tag_st = tag_encode("reachable", "bulb", "src", "adj", "line", color)
    rule = f"connected(R0, C0, R1, C1) :- turning(R, C), not intersect(R, C), intersect(R0, C0), intersect(R1, C1), {tag}(R, C, R0, C0), {tag}(R, C, R1, C1), (R0, C0) < (R1, C1).\n"
    rule += (
        f"connected(R0, C0, R1, C1) :- intersect(R0, C0), intersect(R1, C1), {tag_st}(R0, C0, R1, C1), (R0, C0) < (R1, C1).\n"
    )
    rule += ":- connected(R0, C0, R1, C1), number(R0, C0, N), number(R1, C1, N)."
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
    aliases = ["ichimaga", "ichimagam", "ichimagax"]
    examples = [
        {
            "data": "m=edit&p=7Vbvb7JIEP7uX9Hs125ysCgiyX2w1vZtz1L7vhqvEmNWi0oLbg/B9jD+751dNLIL9noxae7DhTCZeebH7uzAA6u/Ehp52ILLsLCGdbiMKhE30Rri1nZXz48Dzz7DzSResAgUjO8dPKPBysO3j4tOizXfLpt/rq14ONSvteRGGzxfPZ//DP+48Y1Iv3Ks7l33zifz5o/WxYPZPje7yaofe+uHUL947g97s+5g3iB/t51hNR3ea7Xb4ey3dbP/e8XdbWFU2aQNO23i9Np2EUF4d49w+mBv0js7dXD6C1wI6yOMwiSI/SkLWIT2WNoBTUeYgNo+qAPh51orA3UNdCfTTVAfQZ360TTwxp2sUNd20x5GfO0Lkc1VFLK1xxeDNGFPWTjxOTChMZzeauG/ImyAY5U8sZdkF6qPtjhtZh20v9gBFBEdVDM164BrJR3wxk7uwHuae+8lm2+MtluYy0/Y/th2eSf9g2od1F/2BqRjb5BesyBXxyaGfCinm5piE7BJzq7ytc5gFHukzjOMnF1XIyy9gBjyKlYhp8EjZMSUcoimVoUXRI7Q1aqE8G5yEaSmRhiFqgaPyeUYhapVnpOLqMpnSmr8zPK20okyAyLNAAali3E9CnklJBGyB9PEqSHkpZCakDUhOyKmLeRAyJaQVSFNEVPnz8O/emJO3w4yNJhCw8KgwJC5Ak8hFs+R8Y97dYkpmPFw1b7XHlVc1Ib378xhUUgDeDWdJJx40d4GYkQrFoxXSTSjU2/svdNpjOyMm/MeCVuKGhIUMPYa+MuyCnuXBPrzJYu8UhcHOWccKcVdJaUmLHpS9vRGg0DuRXy0JChjNgmKI6CtnE2jiL1JSEjjhQTkSFqq5C2Vw4ypvEX6QpXVwsNxbCvoHYkbGIvwYf7/FftvfsX4jLRvZqZTidKFswYuq2P+VcXpPUavyZiO4bgR/DDhr7kzJjzBXWuc4j5aHMj6mIMUHN8+GPGis+gT1j04VbiEewH9hH5z3jL8CNPmvCpeoFW+2SKzAlpCroCq/ApQkWIBLLAsYEeIlldVuZbvSqVbvlSBcflSedJ1kT9d+CGdUzSqfAA=",
        },
        {
            "data": "m=edit&p=7VZfb9s4DH/Ppyj0dIcJOMuSXdvAPaRdutsuzdKtRa8JgsJN3cSdHe8cu+256HcfyTSwpLjD/QEOfRgcM+SPFEVSFqX1n3VcJlxI/MmAO1zA40mXXqEUvc7zc5pWWRLt8X5dLYsSGM4/jvhNnK0T/uFiOTws+vdv+3/cBdVkIt459Xvn/Pbo9s2n/Pf3qSzF0SgYH4+PU3fR/+3w4MQfvPHH9fqsSu5OcnFwezY5vRmfL0L3r8FooprJR8f7MLn55a5/9mtv+hzCrPfYhFHT5827aMpcxp/fGW9OosfmOGpGvPkMKsbFjLO8zqp0XmRFybZYMwROMO4CO2jZc9Ijd7gBhQP8aMP7wF4AO0/LeZZcDjeOxtG0OeUM5z6g0ciyvLhLcDIYRvK8yK9SBK7iCqq3XqZfGZegWNfXxZf62VTMnnjT32Qw+JsZgJNtBshuMkCuIwNM7D9nkFwvkoeO4MPZ0xOsyycI/zKaYiZnLRu07OfoEegoemRSCBjrcp/DeHAnhQuy0GQPZNnK7r5pL5Wpl2ivjZe+aa9wPs1eoT/Vyh7Or9n7junPR71m71vz+aE5PrD8BdK0DzB+XY/xaPrQsg+teoSmvRIYb+tPCdO/onrq9hhv60+5GK8uB+Z417Kn+mv+qN6arCw91VuTPXM9FNVf11vx0npo8fhmfRStR7s+ah/tdRnz0ewDa35aH82/tT4qMNdXheb3oULze1OhWS/PMevrOWZ9PNoPmt5aP4/WT5fNenquuZ88F/Np8/ck6jV7a794Ut9fsEkFbdULokdEXaKnsJN5I4m+JeoQ9YgOyWZA9JzoIVFF1CebfewF/6hb/A/hTKVPB1/X4/3Q/BvNrDdlAzgw9kZFmccZnCWjOr9Kyq0MJzlbF9nlui5v4nlymTzE84pFm8uErjGwFfkwoKwovmbpqsvDVmWA6WJVlEmnCkE85F5whaoOV1dFeW3FdB9nmZkL3bMMaHMUG1BVwjmryXFZFvcGksfV0gC0W4XhKVlZxaxiM8T4S2zNlrfleOqxB0YvNCW4B/64dr3WaxeukfPa2ulrC4c+76L8Tq9plTbc0XEA/U7T0bRd+Av9RdPa+E4zwWB3+wmgHS0FULurALTbWADc6S2AvdBe0KvdYTAqu8ngVDt9BqfSW82UpfNlmseLON/7Cf5WCWy9vS32M5v1vgE=",
            "config": {"ichimagam": True},
        },
        {
            "data": "m=edit&p=7VXfb+I4EH7nr0B+ulUtXZyEkES6B0qh2y6ltAWxBSEU0gBpE9zND8oG8b93bOBiB1rtPuyJh5PJaOabH56xk4/4R+pEHrZgaSZWMIGlmQp/TJ39lN3q+kng2WVcS5M5jUDB+LbZxFMniD18/Thv1Wnt7aL2fWkmgwG5VNIrpf/cfD67D79d+VpEmm2zc9O58dVZ7Wv9/M5onBmdNO4l3vIuJOfPvUF32unPLPVnoz3Qs8GtUrkeTP9e1nr/lIa7HkaldWbZWQ1nl/YQqQjvnhHO7ux1dmNnbZw9gAthMsIoTIPEd2lAI7THshZoBGEV1Eau9rmfafUtSBTQ21vdAPURVNeP3MAbt7aFOvYw62LE9j7n2UxFIV16bDNI47ZLw4nPgImTwPHFc/8VYQ0ccfpEX9JdKBltcFbbTtD4xQmgyH4Cpm4nYNqfmsB7mnmrI81bo80G7uUe2h/bQzZJL1fNXH2w1yDb9hoRswK5BBsY8qEcMU3ZtlSwVcGugq39a6uKIsWrCosXbML8QjzRZL8q76dqhXqaIedrLF6w9UK8TqR+VV0v+C2w9dyuFOIr7DwE22D5QrzB8oV61UJ8tVDfYvMK/Vpsnjxf4+eX52sK20+05fk1RTwvuETCr/KRyyaXKpdduGmcaVxecKlwWeGyxWMaXPa5rHOpc2nwmCp7V37rbfoP2hmqJudFcVVOCxmVhqgBH2i5TaPQCeDbbafhxIv2NjAnimkwjtNo6rje2Fs5boLsLXmLHglb8BoSFFD6GviLYxX2Lgn0ZwsaeUddDGSk8kEp5jpSakKjp0JPb04QyLPwPzUJ2lKfBCUR8JpgO1FE3yQkdJK5BAgsLlXyFoXDTBy5RefFKewW5sexKaEV4g98dCq7zP//5k7zb47dkXJq9HRq7fDXm0afcE3uLMJHGAfQT0hH8B7DP+AXwVvED8iENXvIJ4AeoRRAi6wC0CGxAHjALYB9QC+sapFhWFdFkmFbHfAM20qkmiHy3bkfOjMnXJX/ciMax/5iVt6DX9Co9A4=",
            "config": {"ichimagax": True},
        },
        {"url": "https://puzz.link/p?ichimaga/14/10/cdlcicdehcg2ddkbhddgdhbjbhcbcj8bg6bbjdhbgcgbbi6cgcbc", "test": False},
    ]
    parameters = {
        "ichimagam": {"name": "Magnetic", "type": "checkbox", "default": False},
        "ichimagax": {"name": "Crossing", "type": "checkbox", "default": False},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="intersect"))
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="white", crossing=bool(puzzle.param["ichimagax"])))
        self.add_program_line(route_turning(color="white"))
        self.add_program_line(convert_line_to_edge())
        self.add_program_line(limit_turning(color="white"))

        if puzzle.param["ichimagax"]:
            self.add_program_line(route_crossing(color="not intersect"))
            self.add_program_line(crossing_route_connected(color="white"))
        else:
            self.add_program_line(grid_color_connected(color="white", adj_type="line"))

        if puzzle.param["ichimagam"]:
            self.add_program_line(avoid_magnetic(color="white"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            self.add_program_line(f"pass_by_route({r}, {c}).")
            self.add_program_line(f"intersect({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_edges_around_vertex(num, (r, c)))
                if puzzle.param["ichimagam"]:
                    self.add_program_line(f"number({r}, {c}, {num}).")
                    self.add_program_line(bulb_src_color_connected(color="white", src_cell=(r, c)))
            else:
                self.add_program_line(count_edges_around_vertex(("gt", 0), (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
