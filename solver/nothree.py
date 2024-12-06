"""The No Three solver."""

from typing import List

from noqx.penpa import Direction, Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def no_consecutive_same_distance(color: str = "black") -> str:
    """Generate a rule to avoid consecutive black cells with the same distance."""
    min_r = f"MinR = #max {{ R0: grid(R0, C), {color}(R0, C), R0 < R }}"
    max_r = f"MaxR = #min {{ R0: grid(R0, C), {color}(R0, C), R0 > R }}"
    min_c = f"MinC = #max {{ C0: grid(R, C0), {color}(R, C0), C0 < C }}"
    max_c = f"MaxC = #min {{ C0: grid(R, C0), {color}(R, C0), C0 > C }}"
    rule = f":- grid(R, C), black(R, C), {min_r}, {max_r}, grid(MinR, C), grid(MaxR, C), R - MinR = MaxR - R.\n"
    rule += f":- grid(R, C), black(R, C), {min_c}, {max_c}, grid(R, MinC), grid(R, MaxC), C - MinC = MaxC - C."
    return rule


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color(color="black"))
    solver.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(no_consecutive_same_distance(color="black"))

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert symbol_name.startswith("circle_SS"), "Invalid symbol type."

        if d == Direction.CENTER:
            solver.add_program_line(f"black({r}, {c}).")

        if d == Direction.TOP:
            solver.add_program_line(f":- {{ black({r - 1}, {c}); black({r}, {c}) }} != 1.")

        if d == Direction.LEFT:
            solver.add_program_line(f":- {{ black({r}, {c}); black({r}, {c - 1}) }} != 1.")

        if d == Direction.TOP_LEFT:
            solver.add_program_line(
                f":- {{ black({r}, {c}); black({r - 1}, {c}); black({r}, {c - 1}); black({r - 1}, {c - 1}) }} != 1."
            )

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "No Three",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VXRbpswFH3nK6b7fB+wDaz1W9Z1e+nSbWSKIoQih7oNGhUZhKlylH/v9YUp2gbS1mnry2T56OT4GA7XcNN+6UxjMaGhzjBEQUMmCU8RRTzDYSzKfWX1C5x1+23dEEG8nuOtqVobZIMpDw7uXLsZurc6AwnIU0CO7oM+uHfardCltAQYkXZFTABKopcnuuR1zy56UYTE5wMnuiJalE1R2XWa9tJ7nbkFgr/RK97uKdzXXy30+/h3Ud9vSi9szJ4ept2Wu2Gl7W7qz93gFfkR3azPm37L6/MMedUpr6d9Xs9G8vptf57X3tzZttuMhT3Pj0eq+keKu9aZT/7pRM9ONNUHwjmjYFzpAyQRXUbQnb6LByKKJ/RkXI8n/PGEPxn3Sznul7Gc0NWoruSErsavo9SYn2r0hislGRdUSHSK8TVjyBgzXrHnknHJeMEYMSbseemP4hcPi2oBWvpooKOfT+4vZcuk5CbQj/jpPA8ySLvm1hSW3tp0a3YWqDscA3gAnpkiW/S/YTxPw/AnED65bTzPh5FRbZVCd42w69ZmXdQV0F8Osi5/T6fX/Ef9nz8tfW3Q7srGVHemMg+lbSEPHgE=",
        },
        {"url": "https://puzz.link/p?nothree/10/10/genceemeienei6eiemeeemeiemenemeiemeeemei6eieneiemecene", "test": False},
    ],
}