"""The Dosun-Fuwari solver."""

from typing import Set, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction


def dosufuwa_gravity(float_color: str = "white", drown_color: str = "black") -> str:
    """Generates a constraint to fill the colors according to gravity."""
    rule = f":- grid(R, C), {float_color}(R, C), grid(R - 1, C), not {float_color}(R - 1, C).\n"
    rule += f":- grid(R, C), {drown_color}(R, C), grid(R + 1, C), not {drown_color}(R + 1, C).\n"

    return rule.strip()


class DosuFuwaSolver(Solver):
    """The Dosun-Fuwari solver."""

    name = "Dosun-Fuwari"
    category = "var"
    aliases = ["dosunfuwari"]
    examples = [
        {
            "data": "m=edit&p=7ZRNj9MwEIbv+RWrOc/BM07Z1LdSWi5l+WhXaBVFq242y0YkMqQNIFf574wdL1UlJPYC6gE5fvVkMn7jsePsvvbbrsKJNJ2hQpLGnIWeKn89tU29bypzgbN+/2g7AcS3yyU+bJtdhUke04rk4KbGzdC9NjkQILB0ggLde3Nwb4xboFvLI8C0QGj7Zl+XtrEdhBhJ3mocyIKLI34Mzz3NxyAp4avIgjeCZd2VTXW7GiPvTO42CP7dL8Noj9DabxXEufn70rZ3tQ/cNd8fAbWEdv29/dzDk/eAbhbmHnOfWYA+FqB/FaB/XwD/xQKmxTDIrnyQEm5N7qu5PmJ2xLU5DH5CXinoTdBlUA66kVR0OuiroCroJOgq5CzMAUhNkUiBYdl8RaesODIL68haOI2cCk9GpkzGTiOLJ0cfolOm6EniSdGTxJOiJ19KfhZZPDl6snjq6MN0yhw9WTw1jax9jo8Pfkd9ufOgadAXYRku/Xr+4xX/43RyHg+3b5PnUZHksO67h21Zyae2uP9UXVzZrt02cje37Re7q/cVyIkfEvgBoeca+f9P4Fx/An6H1Ll9mOc2HTkqRfIT",
        },
        {
            "data": "m=edit&p=7VXbbtNAEH3PV1T7vA979e76rZSUl16AFqHKiqI0dWmEI5dcADnKv3N2PY5TgdSqoggk5HjmZH1mPDfvLr+sJ4uSSxF/2nNoXEb6dCufpVvQdTlbVWV+wA/Xq7t6AcD5+fExv51Uy5IPCqKNBpsm5M0hb97kBZOMM4VbshFv3uWb5jRvhry5wCPGzYiz+bpazaZ1VS9YWpPgnbSGCnDYw4/peURH7aIUwGeEAa8Ap7PFtCrHJ+3K27xoLjmL736VrCNk8/prySi2+H9az69nceG6+nbHuMbScn1Tf16zzveWN4cpduI+MQHdJ6B3CehfJ6BeMIEw2m7RlfdIYZwXMZsPPfQ9vMg3TCuWG86MTyqzSXnZKpdUaClSaNItV0rTai1abVq6zCJvGzPdQMokr5I8TlIleYkYeKOTfJ2kSNImeZI4QwSolOVKZSxXmCyFCVWOsAP2LZamxwqTbFSLjeLKkq2FrSVbC1tLfAu+DcS3PdYSfiz5B1/Lfl2Tfw3/WhPWwIYw4tG2x4beZfCujGwz2DqKzdk9DL4jWwefjnzaAKx7jief3nMtWp/QXMvWDzSwI+yAPXHMDquAbUCYHVZBEh8+KUdorg35NPBpyCdqq6m2GjXXVPOEVSAc4EeQH7yLagjd+zfA1hIfcZouBg0/rsfSEI7xE1/IHVYetkL2dfPUa4d++Y6DOgfqb0BsgmITYs8WfEc9cmqv5qiPI04WeyGoL/CZdfMDW8pFGfAplzS3puMjNtv11PT84Pdiw7wFv8NadjURPRaIX1L8KtaK6qNQH9XV0wJ38xBr1fUo9rHrS9jDse+hx7brkdjriyKf27jFxc/0KEmTZJY+Xxc3mCduQT/vFCyOTCF5tzmepu2SxeEp1MPV520qj0Ze6PZofHjZf29tNCjYxXpxO5mWODyGN5/Kg7N6MZ9U+HdUz+/r5WxVMpzh2wH7ztJdYD7/H+t/67EeOySe/WW90OfySDhFc4XtlTfnnN2vx5MxyswwYfy3rssnr//x6mA/GQ1+AA==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_cc(colors=["circle_M__1", "circle_M__2", "white"]))
        self.add_program_line(dosufuwa_gravity(float_color="circle_M__1", drown_color="circle_M__2"))

        exclude: Set[Tuple[int, int]] = set()
        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")
            exclude.add((r, c))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, exclude=exclude)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(1, color="circle_M__1", _type="area", _id=i))
            self.add_program_line(count(1, color="circle_M__2", _type="area", _id=i))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__1":
                self.add_program_line(f"circle_M__1({r}, {c}).")
                self.add_program_line(f"not white({r}, {c}).")

            if symbol_name == "circle_M__2":
                self.add_program_line(f"circle_M__2({r}, {c}).")
                self.add_program_line(f"not white({r}, {c}).")

        self.add_program_line(display(item="circle_M__1"))
        self.add_program_line(display(item="circle_M__2"))

        return self.program
