"""The Gokigen (Slant) solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, fill_line, grid
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.route import convert_line_to_edge


def slant_rule() -> str:
    """Generate slant rules."""
    rule = f':- grid(R, C), line_io(R, C, "{Direction.TOP_LEFT}"), not line_io(R - 1, C - 1, "{Direction.BOTTOM_RIGHT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.TOP_RIGHT}"), not line_io(R - 1, C + 1, "{Direction.BOTTOM_LEFT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.BOTTOM_LEFT}"), not line_io(R + 1, C - 1, "{Direction.TOP_RIGHT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.BOTTOM_RIGHT}"), not line_io(R + 1, C + 1, "{Direction.TOP_LEFT}").\n'

    rule += "grid_direc_num(R, C, D, 0) :- grid(R, C), direction(D), not line_io(R, C, D).\n"
    rule += "grid_direc_num(R, C, D, 1) :- line_io(R, C, D).\n"
    rule += f':- grid(R, C), grid(R + 1, C + 1), {{ line_io(R, C, "{Direction.BOTTOM_RIGHT}"); line_io(R, C + 1, "{Direction.BOTTOM_LEFT}") }} != 1.'
    return rule


def no_loop() -> str:
    """Ensure there is no loop in the grid."""
    rule = "reachable(R, C) :- grid(R, C), not grid(R - 1, C - 1).\n"
    rule += "reachable(R, C) :- grid(R, C), not grid(R + 1, C + 1).\n"
    rule += f'reachable(R, C) :- grid(R, C), reachable(R - 1, C - 1), not line_io(R, C - 1, "{Direction.TOP_RIGHT}").\n'
    rule += f'reachable(R, C) :- grid(R, C), reachable(R - 1, C + 1), not line_io(R, C + 1, "{Direction.TOP_LEFT}").\n'
    rule += f'reachable(R, C) :- grid(R, C), reachable(R + 1, C - 1), not line_io(R, C - 1, "{Direction.BOTTOM_RIGHT}").\n'
    rule += f'reachable(R, C) :- grid(R, C), reachable(R + 1, C + 1), not line_io(R, C + 1, "{Direction.BOTTOM_LEFT}").\n'
    rule += ":- grid(R, C), not reachable(R, C).\n"
    return rule


class GokigenSolver(Solver):
    """The Gokigen (Slant) solver."""

    name = "Gokigen"
    category = "var"
    aliases = ["slant"]
    examples = [
        {
            "data": "m=edit&p=7VZdT+M4F77vr0C+2tVY2jix0yTSalWgzM4slDIDYmmFqlBCCSQ1myYwbxD/fc5xuhPbDYzYWe28F6MoR+fL58vOE6/+quIioUxQxqkXUIcyeHwnoKLv0IAL9Trr5zgtsyTaooOqvJYFMJQejuhVnK0S+v7sen9HDh52B3/eB+Vkwt461Tvn9Gbv5s2H/I93qVewvVEwPhgfpO5i8PvO9pE/fOOPq9VJmdwf5Wz75mRyfDU+XYTu/4ajCa8nh454P7n65X5w8mtvimXBc957rMOoHtD6bTQlLqHr95zWR9FjfRDVI1p/BBMBX1rvA8cIdYEdNv7Inio7cjuNnTnAjxreB/YM2HlazLNktt8EGkfT+pgSzLOtViNLcnmfkGaZkucyv0hRcRGXMKnVdXq3tqyqS3lbrX0hIMmrrEznMpMFKlH3ROtB08KwowWvbQHZpgXkvk8LYXcLT7A9H6CJWTTFfk5aNmjZj9Ej0FH0SLygv47nU6AQ0wsC0MAJ/CKHphxyQ+YOs2QPZE+T0d/VZGHKzDH9GcbT7a4pu5bdxXhaftesn3u4XpM55tNlKz7HeFo93LfsGF+XzflwYdUnrHoE+mt2H/Nr+Xycn2638vWxfl3GeNr6ANdr+QKcP/HaHeaBtQPNGfhN98CcWswQZ6DFDHGFFiE0ZyDUmWjtwjoDwjHXC8daz8yZC4b+bT2CmTMR1pkQrjkDYZ0R4Vr5Pcvumf0LdWY0f27l41Z/HONr8QTatXjC3AEhrHp885sQ1hkRvlVv3/wmRd+K37fqCcxvQKgzo/mrM6PJofmNi9DyV5igy9Z+heZ++Y45T98x+/PVeWnz+cyWzfPiu/o3DtDGFMCdKbqnqKvoMeAfrT1FdxV1FBWK7iufoaKniu4oyhX1lU8fEfRVGPvt5QAGe1Thqod4jDzsh/fVKqd+c5noevo/LM9bzntTMrxcJFu7abyQyziDH/Coyi+SYmskixxkuAWRlcxmq6q4iufJLPkUz0sSNRcx3WLoliqGocqkvMvSZVeEv02GMl0sZZF0mlCZQNXPhEJTR6gLWVxaNT3EWWb2ou6ohqq52RiqsoBriybHRSEfDE0el9eGQrviGJGSpTXMMjZLjG9jK1vejuOpRz4R9QKmMMp/XFn/z6+suFXO6y6uL18Bvv8vYAob8gWraX1IyV01i2fQOaEw9f/C7IIZdv4fmvk3mZv/1Wsr/5f/m1/fQ4UcsngBxlujre4Ac9C+gOeatUv/DHRrVlu/gdNY7CZUg7YDrUFrAzaoNjEblBuwDbpnkBuj2uCNVdn4jak2IBxT6Sg+JassXpZbPy3kbbpIlj+T895n",
        },
        {
            "url": "http://pzv.jp/p.html?gokigen/40/25/hbg1bha6ah66bcbh7c98d8cdjdk672817chc717die62b8dcg8c26di32ck3d287271617262bg31222c88e2bddcc3bkdeg87dc777228ddg1cehdch6cb2cb122b73d3c26b31377c7e71cc8clbg8bh317677c6d7b63716eh26d2b8c9ch31c7ddj28277d77bg732cg27c61cg83268871ci626b8681cieicg2ddjdi6277226ch8d3d7dgec2cg73dd63622d3cb172b62667cc1c66d37226263c7cdg8d7bg7273cg78cb9c77cg22dg061661668dge71b778c76bgcg717c7cd376677173bgdg81b9dc8dgch231ch8ce897cg7b631682cgcckcjdg318277cg4ceh6166cgb6cc268173cgeg2173c27d367328cgc267di6bi7bg77dg769cg78d8d22ba656776bgb1bibajb",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(
            fill_line(
                directions=(
                    f"{Direction.TOP_LEFT}",
                    f"{Direction.TOP_RIGHT}",
                    f"{Direction.BOTTOM_LEFT}",
                    f"{Direction.BOTTOM_RIGHT}",
                ),
                color="grid",
            )
        )
        self.add_program_line(slant_rule())
        self.add_program_line(no_loop())
        self.add_program_line(convert_line_to_edge(diagonal=True))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(f":- #count{{ D: line_io({r}, {c}, D) }} != {num}.")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
