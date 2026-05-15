"""The Kurotto solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import count_reachable_src, grid_src_color_connected


class KurottoSolver(Solver):
    """The Kurotto solver."""

    name = "Kurotto"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZNj9owEL3zK5DPPnhsx/m40e3SC2XbQrVaRREKNKtFDQoNpKqM+O8dTxBes3toD6WXlfFo3njG8zwMNrsfXdlWHKT7qIQLDjh0qmmqOKIpTmO+3tdVNuSjbv/UtKhwfjce88ey3lWD/ORVDA42zeyI2w9ZzoBxJnECK7j9nB3sx8xOuZ3hEuMabZPeSaJ669V7WnfaTW8Egfq01w2qD6iu1u2qrhYTXEXLpyy3c85cnncU7VS2aX5W7MTD4VWzWa6dYVnu8TC7p/X2tLLrvjXfu5MvFEduRz3d2St0laerznTVv6Rbb5vXiKbF8YgF/4JUF1nuWH/1auLVWXY4OkYHpjSGRtz03wnTAqHwMEKozjAChImHLlafoXGx4ION8449NEGmWARbxzJwTlSQKTFBptTtzIbMG1w0gMdJkAtEyBTABNsDxBc4DcoAUobxMgrXlQjjlblYd/t5eqDTcD+qpHmGTVANMCo8H1Ax1TPsDpx6HIe1hzQKEkghLrAMMYiLCktQQQYZlAibCailHkiOSUqSc+w4bhXJ9yQFyYjkhHxuSd6TvCGpSRryiV3P/mFXM40Hl9i4eB7dt/gVuOVK0035ckRvdjeKQc5mXftYriq8tqbdZlm1w2nTbsqa4QtxHLBfjCb2ND44b4/G1R8NV3zxV0/H///N51hXDdzecbbtFuVi1dQM/3FwsssX9quzx4uhGPwG",
        },
        {
            "url": "https://puzz.link/p?kurotto/17/13/7i4i-1ai4iay1i6ibi0y3ibi9i-14iay4i7i-10i4y-11iei6ici3y1ibi7i2y-10i8i0i4i1",  # probably TLE (with 1.8 GHz CPU)
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c())
        self.add_program_line(adjacent())

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"not black({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color="black"))
                self.add_program_line(count_reachable_src(num + 1, (r, c), color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
