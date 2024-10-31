"""The Binario solver."""

from typing import List

from .core.common import count, display, grid, shade_c
from .core.helper import extract_two_symbols
from .core.penpa import Puzzle, Solution
from .core.shape import avoid_rect
from .core.solution import solver


def unique_linecolor(colors: List[str], _type: str = "row") -> str:
    """
    Generates a constraint for unique row / column in a grid.
    At least one pair of cells in the same row / column should have different colors.

    A grid rule should be defined first.
    """
    if _type == "row":
        colors_row = ", ".join(
            f"#count {{ C : grid(R1, C), grid(R2, C), {color}(R1, C), not {color}(R2, C) }} = 0" for color in colors
        ).replace("not not ", "")
        return f":- grid(R1, _), grid(R2, _), R1 < R2, {colors_row}."

    if _type == "col":
        colors_col = ", ".join(
            f"#count {{ R : grid(R, C1), grid(R, C2), {color}(R, C1), not {color}(R, C2) }} = 0" for color in colors
        ).replace("not not ", "")
        return f":- grid(_, C1), grid(_, C2), C1 < C2, {colors_col}."

    raise AssertionError("Invalid line type, must be one of 'row', 'col'.")


def solve(puzzle: Puzzle) -> List[Solution]:
    if not (puzzle.row % 2 == 0 and puzzle.col % 2 == 0):
        raise AssertionError("# rows and # columns must both be even!")

    symbol_1, symbol_2 = extract_two_symbols(set(puzzle.symbol.values()))

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color=symbol_1))
    solver.add_program_line(f"{symbol_2}(R, C) :- grid(R, C), not {symbol_1}(R, C).")
    solver.add_program_line(count(puzzle.row // 2, color=symbol_1, _type="row"))
    solver.add_program_line(count(puzzle.col // 2, color=symbol_1, _type="col"))
    solver.add_program_line(unique_linecolor(colors=[symbol_1, f"not {symbol_1}"], _type="row"))
    solver.add_program_line(unique_linecolor(colors=[symbol_1, f"not {symbol_1}"], _type="col"))
    solver.add_program_line(avoid_rect(1, 3, color=symbol_1))
    solver.add_program_line(avoid_rect(1, 3, color=f"not {symbol_1}"))
    solver.add_program_line(avoid_rect(3, 1, color=symbol_1))
    solver.add_program_line(avoid_rect(3, 1, color=f"not {symbol_1}"))

    for (r, c), symbol_name in puzzle.symbol.items():
        if symbol_name == symbol_1:
            solver.add_program_line(f"{symbol_1}({r}, {c}).")
        else:
            solver.add_program_line(f"not {symbol_1}({r}, {c}).")

    solver.add_program_line(display(item=symbol_1))
    solver.add_program_line(display(item=symbol_2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Binairo",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VfRa9s+EH7PXzH0rAfrdLJlv2VZu5e222/NKMWY0nYeDUvnrUm24ZD/vdLZLPDTVwpjG4UVx8fl85fTJ92dIq++bi7vWk1Z/FivM23CVZRebu+M3Nl4zRfrZVu90NPN+qa7C47Wbw4P9cfL5aqd1COrmWz7suqnun9d1coorSjcRjW6/6/a9seVuu5urxZK96fhudImPDgamBTcg717Js+jNxtAkwX/ZPSDex7cdft5vRq+vq3qfq5VHOml/DS66rb71qpRSfw+jB6Aq+X3mxFbbT50nzYjyzQ73U8fkWr3UqM7SI0ekBpnEKVeL+6ul+3F8W9VWza7XVjxd0HvRVVH6e/3rt+7p9U22BOxRux5tVV5EcJQGOantCBW5WVAzf/RwiFu4SEXRvCEIniG3KgsQcsYN4lgMoPhGBnAcNImg5qNibEBbDGMY1Ocecq2GWRbOHdjsUDGQ3JMTAo7PKTDS+VyDOPYOcyvyXHsIsZOpyOlk7JLHKSMRZkEISkIAD/AhjVMuCAIZ54ILizRA2yYNCK4sGTxdBh2DklBABhPBxcEOZgGKiI7DSJ7A4CxEo+H9DhICSdvM7iwVpo7hQ0sNouTZnG7WkkagGHSLE6alS5O2Qx7x0qKAQxzaXG72gJuj1YaMIX9AzBsEuuxkhIG4QwuLONcMm5Xxg3IOJdMcPJMsCDYwlwyzg5zVAJgHBv3JePNlHNYPow3Uy6wwAIvFW5XxgXB+G+bPZ48Lh+WLk5gh7deJ3+jAIbF5iTFAIYCHYHJh+PQoRyKSOw8nJl0b8W+EpuJdWKPhHMg9kzsTCyLzYVTxFPXL5/L/pCc2g3n+8cv98x75v17vGZSq1l3+6VbLdatCm+yu4n6oeSubSDw88vt33+5jaufPbWt9KnJCZt7M7kH",
        },
    ],
}
