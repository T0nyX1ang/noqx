"""The Mukkonn Enn solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.loop import loop_turning, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected


def mukkonn_constraint(r: int, c: int, pos: str, num: int) -> str:
    """
    Generate a mukkonn constraint.

    A loop_straight rule, a loop_turning rule, and an adjacent rule should be defined first.
    """

    rule = ""
    if pos == "sudoku_4":
        max_u = f"#max {{ R0: grid(R0, {c}), turning(R0, {c}), R0 < {r} }}"
        rule += f':- grid_direction({r}, {c}, "u"), R = {max_u}, grid(R, _), {r} - R != {num}.\n'

    if pos == "sudoku_5":
        min_r = f"#min {{ C0: grid({r}, C0), turning({r}, C0), C0 > {c} }}"
        rule += f':- grid_direction({r}, {c}, "r"), C = {min_r}, grid(_, C), C - {c} != {num}.\n'

    if pos == "sudoku_6":
        max_l = f"#max {{ C0: grid({r}, C0), turning({r}, C0), C0 < {c} }}"
        rule += f':- grid_direction({r}, {c}, "l"), C = {max_l}, grid(_, C), {c} - C != {num}.\n'

    if pos == "sudoku_7":
        min_d = f"#min {{ R0: grid(R0, {c}), turning(R0, {c}), R0 > {r} }}"
        rule += f':- grid_direction({r}, {c}, "d"), R = {min_d}, grid(R, _), R - {r} != {num}.\n'

    return rule.strip()


class MukkonnSolver(Solver):
    """The Mukkonn Enn solver."""

    name = "Mukkonn Enn"
    category = "loop"
    aliases = ["mukkonnenn"]
    examples = [
        {
            "data": "m=edit&p=7VZbT+NIE33Pr0D9Oi19vl3alvYhMGR2ZkMIA4glEYqcYEgYB+fzBWaN+O9TVU5il21Gs9rVaB5WTlpVp7q6T5Xdx07/nwdJKD24TCU1qcNlKo3+ysKftr0uVlkU+geyn2fLOAFDytPBQN4FURrKT9fL4VHcf37f//NJZZOJ/kHLP2pXD4OHd5/Xf3xcmYk+GKnxyfhkZdz3fz86PHOO3znjPL3MwqeztX74cDm5uBtf3XvGX8ejiVVMTjX70+Tuf0/9y9960y2Hm95L4flFXxYf/KnQhRQG/HVxI4sz/6U48YtrWZxDSEgLsGE5yQDzuDKvKI7WUQnqGtgjsD2wwbwGcxGvN0GalsDYnxYXUuA2h5SMpljHT6HY0kAfUuYrBOZBBp1Kl6vNNpLmt/GXfDsXFhTrPMpWiziKEwQRe5VFv6xg2FGBWVWAZlkBWh0VYGH/tILw9j5M83kXfa+b/ivcmc9QwMyfYi2Xlakq89x/EcoSvgX2yH+BUQdEt5SG6xyUvQFX564BrrFzzMqxXYzsJ9ouxsydA/vUYzZzPYe7LncVd71qT8dkmY6JmfsY5u0dzKomEtddjJjWYoyrw7k62LF9pmrEOBtVZ6M4AY812fGod3B8ti6tu3Ndjd0CV2ONdjVG39WI/j6Xd8jlfXAtWnk/2WI0lME6r0zGWZmMlTKJhrlzbcZK2aypymaNUzaRtHaux3M9nls2p3Ipl/aFR/gaHmETq9DpAO3PnKAdm6CDJTRBtwukQ9ECkWcL7NpIYSebID3nTVA3unbSDayyhdLN5Sj0YECH2aDxAs66LEwa39Oo0WjTOKQ5xzRe0XhEo0WjQ3NcVIsf1JO6kpQ34+/SETbW5Cl4lyiJT6dJlgGPrfmDVKcwH9+b9cv+tZCb3lSc58ldsAhB1Yerx/BgFCfrIAJvlK/nYVL558tgEwp414o0jmZpmTULvwaLTPjl674eYdgjrcWgKI43EWzYscIuxMDV/WOchJ0hBPHd9MZSGOpYah4ntw1Oz0EU8VroM4hBi1WyiDiUJfB6rPlBksTPDFkH2ZIBtY8BtlL42GhmFnCKwZegsdu6asdrT3wV9McXnrT/+zD6dT+M8C5pP03O/h11nUK3t3ooi1MpNvksmEFhAr7B5S4IEtkdBEVtBX56gXRk4uQ7+lUFm3CHigH6HSGrRbvwNzSrFm3iLYFCsm2NArRDpgBtKhVAbbECsKVXgL0hWbhqU7WQVVO4cKuWduFWdfmqjuFN7xs=",
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

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, ("sudoku_4", "sudoku_5", "sudoku_6", "sudoku_7"))
            if pos and isinstance(num, int) and num > 0:
                self.add_program_line(mukkonn_constraint(r, c, pos, num))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"black({r}, {c}).")

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
