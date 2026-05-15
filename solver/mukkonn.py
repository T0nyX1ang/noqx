"""The Mukkonn Enn solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import defined, display, fill_line, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_turning, single_route


def mukkonn_constraint(r: int, c: int, label: str, num: int) -> str:
    """Generate a grid constraint."""

    rule = ""
    if label == f"corner_{Direction.TOP}":
        max_u = f"#max {{ R0: grid(R0, {c}), turning(R0, {c}), R0 < {r} }}"
        rule += f':- line_io({r}, {c}, "{Direction.TOP}"), R = {max_u}, grid(R, _), {r} - R != {num}.\n'

    if label == f"corner_{Direction.RIGHT}":
        min_r = f"#min {{ C0: grid({r}, C0), turning({r}, C0), C0 > {c} }}"
        rule += f':- line_io({r}, {c}, "{Direction.RIGHT}"), C = {min_r}, grid(_, C), C - {c} != {num}.\n'

    if label == f"corner_{Direction.LEFT}":
        max_l = f"#max {{ C0: grid({r}, C0), turning({r}, C0), C0 < {c} }}"
        rule += f':- line_io({r}, {c}, "{Direction.LEFT}"), C = {max_l}, grid(_, C), {c} - C != {num}.\n'

    if label == f"corner_{Direction.BOTTOM}":
        min_d = f"#min {{ R0: grid(R0, {c}), turning(R0, {c}), R0 > {r} }}"
        rule += f':- line_io({r}, {c}, "{Direction.BOTTOM}"), R = {min_d}, grid(R, _), R - {r} != {num}.\n'

    return rule


class MukkonnSolver(Solver):
    """The Mukkonn Enn solver."""

    name = "Mukkonn Enn"
    category = "route"
    aliases = ["mukkonnenn"]
    examples = [
        {
            "data": "m=edit&p=7VZLj9owEL7zK5DPPsSPJE5udLv0Qtm27GqFIoQCmy2o0NCEVFUQ/73jSSAZyGErrVZ7qExG883Dnhl7bPJfRZwlPIChDHe4gKGMg5/R9ufU43693yRhnw+K/SrNgOH8bjjkz/EmT3gvqs1mvUMZhOWAl5/CiEnG8RNsxsuv4aH8HJZTXk5AxbgG2Qg4wbgE9rZhH1FvuZtKKBzgx8AHwAM7BXaZbndxnleCL2FU3nNml/mAzpZl2/R3wqoZEIPLYm0Fi3gPyeSr9a7W5MVT+qOobYV1LTb79TLdpBnD+cTsyMtBlcGoIwPVZKDOGajuDOQrZJA8fU/yYtEVftAd/hF25hskMA8jm8tDw5qGnYQHZjQL9dFGewAqQCK0cew8/ao2AAWFEqA8AdUA15dtQ9e3OnUCmupcAgOPQp9CQ2HQrOkp4ukpv60zbRAQQ7+VhYeRtnSaQhKrZyt29jQXOhqNaUdjaACBQyHWTp6h24a+Q7bAdySFikJNfGmFfFoHXwtirEkYRpLKG+VQKCjEMNQJuiQq42oKXQoxSH2CAfUNqG9AfavDo+q2ncIRVjYLwUnPMVzxUuiJDqHfJcSmuBKqLmHXQsZ0CPGcXwqF7FpJSK9Lqq6lUIMhNrNEeg+9zkuF9CNSB6mLdIQ2t0gfkd4g1Ug9tPHtbfHC+6R9k1Sb8a/hMNfmFBh4Swy3p1MhJ+HYqheGGoG9uBju+5LMehGbFNlzvEzgVh+tfyb9cZpt4w2gcbFdJFmDJ6t4lzB4a4899ofhZ69V7v5/ft/v82t3yXmzpnmdHo6g2nXX8fKOs10xj+eQGIN/evykhEbsVkLfXinePEFo/lnvLw==",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="grid", adj_type="line"))
        self.add_program_line(single_route(color="grid"))
        self.add_program_line(route_turning(color="grid"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            if label and isinstance(num, int) and num > 0:
                self.add_program_line(mukkonn_constraint(r, c, label, num))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
