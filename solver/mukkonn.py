"""The Mukkonn Enn solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.loop import loop_turning, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected


def mukkonn_constraint(r: int, c: int, label: str, num: int) -> str:
    """
    Generate a mukkonn constraint.

    A loop_straight rule, a loop_turning rule, and an adjacent rule should be defined first.
    """

    rule = ""
    if label == "corner_top":
        max_u = f"#max {{ R0: grid(R0, {c}), turning(R0, {c}), R0 < {r} }}"
        rule += f':- grid_direction({r}, {c}, "u"), R = {max_u}, grid(R, _), {r} - R != {num}.\n'

    if label == "corner_right":
        min_r = f"#min {{ C0: grid({r}, C0), turning({r}, C0), C0 > {c} }}"
        rule += f':- grid_direction({r}, {c}, "r"), C = {min_r}, grid(_, C), C - {c} != {num}.\n'

    if label == "corner_left":
        max_l = f"#max {{ C0: grid({r}, C0), turning({r}, C0), C0 < {c} }}"
        rule += f':- grid_direction({r}, {c}, "l"), C = {max_l}, grid(_, C), {c} - C != {num}.\n'

    if label == "corner_bottom":
        min_d = f"#min {{ R0: grid(R0, {c}), turning(R0, {c}), R0 > {r} }}"
        rule += f':- grid_direction({r}, {c}, "d"), R = {min_d}, grid(R, _), R - {r} != {num}.\n'

    return rule


class MukkonnSolver(Solver):
    """The Mukkonn Enn solver."""

    name = "Mukkonn Enn"
    category = "loop"
    aliases = ["mukkonnenn"]
    examples = [
        {
            "data": "m=edit&p=7VZbT+NIE33Pr0D9Oi2tb5e2pX0IDJmd+UIIA4glEYqcYEgYB2d9gVkj/vtUlZPYZZvRrHY1modPTlpVp1zdp8ru007/yoMklB5cppKa1OEylUZ/ZeFP214XqywK/QPZz7NlnIAh5elgIO+CKA3lp+vl8CjuP7/v//mksslE/6DlH7Wrh8HDu8/r/31cmYk+GKnxyfhkZdz3/zg6PHOO3znjPL3MwqeztX74cDm5uBtf3XvG38ejiVVMTjX70+Tut6f+5e+96ZbDTe+l8PyiL4sP/lQYQtJfFzeyOPNfihO/uJbFOYSEtAAbgqULaYB5XJlXFEfrqAR1DewR2B7YYF6DuYjXmyBNS2DsT4sLKXCZQ0pGU6zjp1CUM5APKfMVAvMgg06ly9VmG0nz2/hLvr0XJhTrPMpWiziKEwQRe5VFv6xg2FGBWVWAZlkBWh0VYGH/toLw9j5M83kXfa+b/is8mc9QwMyfYi2Xlakq89x/EcoSvgX2yH+BUQdEt5SG8xyUvQFX564BrrFzzMqxXYzsb7RdjJk7B9apx2zmeg53Xe4q7nrVmo7JMh0TM/cxzNs7mFXdSFx3MWJaizGuDufqYMf2maoR42xUnY3iBDzWZMej3sH22bo07851NfYIXI012tUYfVcj+vtc3iGX98G1aOb9zRajoQzWeWUyzspkrJRJNMydazNWymZNVTZrnLKJpLVzPZ7r8dyyOZVLubQuvMLX8AqbWIVOG2i/5wSt2AQdLKEJul0gbYoWiDxbYNdCCjvZBOk9b4K60bWSbmCVLZQeLkehBwPazAaNF7DXZWHS+J5GjUabxiHdc0zjFY1HNFo0OnSPi2rxg3pSV5LyYfxTOsLGmjwFZ4mS+HaaZBnw2po/SHUK9+O5Wb/sXwu56U3FeZ7cBYsQVH24egwPRnGyDiLwRvl6HiaVf74MNqGAs1akcTRLy6xZ+DVYZMIvj/t6hGGPNBeDojjeRLBgxwy7EANX949xEnaGEMSz6Y2pMNQx1TxObhucnoMo4rXQZxCDFqtkEXEoS+B4rPlBksTPDFkH2ZIBtY8BNlP42GhmFnCKwZegsdq6asdrT3wV9McDT9r//zD6dT+M8ClpP03O/ht1nUK3t3ooi1MpNvksmEFhAr7B5S4IEtkdBEVtBX56gbRl4uQ7+lUFm3CHigH6HSGrRbvwNzSrFm3iLYFCsm2NArRDpgBtKhVAbbECsKVXgL0hWThrU7WQVVO4cKmWduFSdfmqtuFN7xs=",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line("mukkonn(R, C) :- grid(R, C), not black(R, C).")

        self.add_program_line(fill_path(color="mukkonn"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="mukkonn", adj_type="loop"))
        self.add_program_line(single_loop(color="mukkonn"))
        self.add_program_line(loop_turning(color="mukkonn"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, ("corner_top", "corner_right", "corner_left", "corner_bottom"))
            if label and isinstance(num, int) and num > 0:
                self.add_program_line(mukkonn_constraint(r, c, label, num))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"black({r}, {c}).")

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
