"""The Aquapelago solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import count_reachable_src, grid_color_connected, grid_src_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="x"))
    solver.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
    solver.add_program_line(avoid_rect(2, 2, color="not black"))
    solver.add_program_line(grid_color_connected(color="not black", adj_type=4, grid_size=(puzzle.row, puzzle.col)))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(grid_src_color_connected((r, c), color="black", adj_type="x"))
        solver.add_program_line(count_reachable_src(num, (r, c), color="black", adj_type="x"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Aquapelago",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VZRa9swEH7Pryj3fA+WJTuO37Ku2UuWbktHKcIEJ3NpqDNnTjyGQv57706mrlnGCoM8jGLru8t3J+k7ScjZ/WjyukAV86sTDFDRE5tYWpSMpAXtc7Pel0V6geNm/1DV5CBeTyZ4n5e7YmDbrGxwcKPUjdF9SC0oQAipKcjQfU4P7mPqZujmFAI0xE19UkjuVefeSpy9S0+qgPyZ97nbHbmrdb0qi8WUosR8Sq27QeB53klvdmFT/Syg1cG/V9VmuWZime+pmN3DettGds236rFpc1V2RDf2cucn5OpOLrteLnsn5HIV/y633FanhI6y45EW/AtJXaSWVX/t3KRz5+kBTAipQTBDMVEkJonFjJQYpXxQDX1UjbTYMPBpYWi8TfxYOki8VT5PGx/XURuPeDyaf9bOT6J5B/2BECl+S1uCRfUIlmfBdAQLtTDsCJHc6yPiLR+7Z4bLoJwXlFTUVyPF9fpJmRZ0x0jBfYZL780vi9AbR5bDQvSSEdXP49ASqfRAeCc4EQwFb2gH0WnB94KBYCQ4lZwrwVvBS0EjGEvOkM/Aq08JlRMixLyhfuPOoM2aUG6ePz/RW/x/jmcDC/Omvs9XBV1zs2azLOqLWVVv8hLoi3IcwC+QZjWlm7ePzNk/Mrz4wSsvkbPdG3+RY2ldY43uGmHbLPLFqiqB/qEg8+Z3/uzq6eKD7029fsyXBWSDJw==",
        }
    ],
}
