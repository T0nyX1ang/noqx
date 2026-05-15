"""The Masyu solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c, shade_cc
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_straight, route_turning, single_route


def masyu_rule() -> str:
    """Generate a rule for black_clue masyu."""
    rule = ":- grid(R, C), black_clue(R, C), not turning(R, C).\n"
    rule += ":- grid(R, C), black_clue(R, C), turning(R, C), adj_line(R, C, R1, C1), not straight(R1, C1).\n"
    rule += ":- grid(R, C), white_clue(R, C), not straight(R, C).\n"
    rule += ":- grid(R, C), white_clue(R, C), straight(R, C), { turning(R1, C1): adj_line(R, C, R1, C1) } = 0.\n"
    return rule


class MasyuSolver(Solver):
    """The Masyu solver."""

    name = "Masyu"
    category = "route"
    aliases = ["mashu"]
    examples = [
        {
            "data": "m=edit&p=7VVRa9swEH7Pryh6vgedZTu237Ku2YvXbktGCcYEN/OImTNnSTyKgv/7TmevWekVtlECg6Ho8vk72fruuJP239piVwJq9zMR0D8NHyOeXhTy1MOYV4e6TC5g0h7WzY4AwM10Cp+Lel+OsmFVPjraOLETsG+STHkKeKLKwb5PjvZtYhdgZ+RSgMSlhFCBR/DqBG/Z79BlT6ImfD1ggguCq2q3qstl2jPvkszOQbl9XvHbDqpN871U/Wv8vGo2d5Uj7ooDBbNfV9vBs28/NV9a9XOLDuykl5sKcs1JrnmQa2S53kvIrauv5b2kNM67jjL+gbQuk8zJ/niC0QnOkmPnJDmLbBfJUflj+gzCY23KjyQ2QJH1RDaW2NCIrC+x40BkQ5EVd4u0yIoRR2LEsRhxLEaMWgwOtRgdalEGalEHopgMRDEbiGI60BPzgUYMEo0cpXG6vSe0Lwfvy8HLVYdS2VGdTrlaPbZzKmawhu1rtpptwDblNVdsb9lesvXZhrxm7NrhrxvmT+VQ01AK4ohqFHUP0DPAaTQuneEvOCAc9ljHQOsI/2Y8melP7scj+Pe4fJSplM66i+tmtylqOvFm62JbKrpVupG6Vzwz4y6p/xfN+S8al319tu55mWbOKLEPXQf2BtS2XRbLVUPVRdnr3UMjPuvue/M599Cusps6X3bQ2fDEcfbc0dmRj34A",
        },
        {
            "data": "m=edit&p=7VNNb4JAEL3zK8yc5wALfnRv1mov1H5oYwwhBi2NpFAsSGPW8N87O2hJGw6NaRMPzWZeHm9nd+ZlmfytCLIQO7TsHppo0RKdDoflOBzmYU2jbRzKFvaL7TrNiCDejkb4HMR5iIZ3SPONvbqQqo/qWnogADks8FHdy726kWqOakJbgJaPkBTxNlqlcZrBUVMuMQtQEB3WdMb7mg0q0TKJjw+c6JzoKspWcbhwK+VOemqKoGtf8mlNIUnfQ6iO8fcqTZaRFpbBlhzm62gDaNNGXjylLwUcK5So+pUD94cO7NqB/enAbnYgfsNBHL2Gu4bmL/yypHd5oPYX0tNOHmvaq+lE7kvdkUaLcS73IBy6xsKvrYFjN6pdUsV3td14Q7dBpZIjLiwYp9QXKpvxitFkbDO6nDNknDEOGB3GDud0tbOTvf9RO54QPGrVap/OfcMDlx69NU6zJIjpf5isg00INIWlATvg8GwUOvV/MM9zMPUbmef2i55bOzQ0vvEB",
            "config": {"visit_all": True},
        },
        {
            "url": "https://puzz.link/p?masyu/21/15/000a0l2943300030l00200i10j0063c60091000670303010606j3600133013ia16l0110000600306b2063000300020960ai301030",
            "test": False,
        },
    ]
    parameters = {"visit_all": {"name": "Visit all cells", "type": "checkbox", "default": False}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black_clue"))
        self.add_program_line(defined(item="white_clue"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(["white"]) if puzzle.param["visit_all"] else shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_straight(color="white"))
        self.add_program_line(route_turning(color="white"))
        self.add_program_line(masyu_rule())

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            self.add_program_line(f"white({r}, {c}).")
            if symbol_name == "circle_L__1":
                self.add_program_line(f"white_clue({r}, {c}).")
            if symbol_name == "circle_L__2":
                self.add_program_line(f"black_clue({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
