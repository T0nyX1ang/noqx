"""The Hitori solver."""

from typing import List

from .core.common import display, grid, shade_c, unique_num
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_color_connected
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(unique_num(color="not black", _type="row"))
    solver.add_program_line(unique_num(color="not black", _type="col"))
    solver.add_program_line(adjacent())
    solver.add_program_line(avoid_adjacent_color())
    solver.add_program_line(grid_color_connected(color="not black", grid_size=(puzzle.row, puzzle.col)))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Hitori",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VZPbxM/EL3nU1Q++7Dj/ffnVkrLpYQfpKiqoqhKw1aNSJQfmwShjfLd6ze7ZcZLLxyAIqEoo5m15/m9sT272y/7eVNbIkuRjQsbWe/ZJM1sQoVNKed/1P+ulrtVXZ3Y0/3uYdN4x9p3Fxf2fr7a1qNpP2s2OrRl1Z7a9k01NWSscf5PZmbb99WhfVu1Y9tO/JCxiX922U1y3j0X95rH4Z11Dyny/rj3vXvj3cWyWazq28vuyX/VtL2yBuu84my4Zr35WpueB+LFZn23xIO7+c6L2T4s/+9HtvtPm8/7fi7NjrY97ehOnqEbC124HV14z9CFil9Mt5wdj77sHzzh22oK7h/FLcSdVAdvx9XBxM6nOr/XvDMmjn2IU/AUJ4glTH2YS5iFo3mIVfgwlrAMRpPIh6mE5MNSQtBSo0AuJAyREyAr0imgMwlD6BTQgpWyYpz3PoZikZhCscKC4kRC8FIrZ8CW5AzYoiIDtNDOAC0FyQCtcofQ0KywoFl45ZAsWDkki8Y8pJUDWkTkQFa5QJbcAsiKRwFoEVEAWngUUKyS+fhIcQtI1mDQrLJBTHaqBLbKLnmrJAS4yCgZW0JAS71KQAvtMtRc8gn6HlIE0UKEIogWMIrATNAo4s1SMeCl4BQBX+ER8KVMRMAXKUThhhFBudSJCNJ1fngviSBe8aMBPzfg7wb4DvhSHnLAV/wd8NX6DviqPg761T6TQwHUhBgFUIJjFEAtyG1JLcCtRQNyc9EAWEBVYNBeiPuLWoAbjFKUoAI6n0+uWjBBCRSjJLyuxC1KLcBtRhHgPqPyuc/oceCrLeFOowl0vUbFgwqkgzOWoQIKMEMFVD73KnW7iDuOOgTccTRg2HKIe44iwE1HA3Lb0RPC+0t52A8pD28w5cMScON6YuBfYMSvsRu2F2wd2yv/lrNtzPY124htyvaS55yzvWZ7xjZhm/GcHO/Jn3qT/gY60xjn68cfTtFf/3Q2mprJvrmfL2r/ZTPer+/q5mS8adbzlfGfkseR+Wb4zycm+fd1+Ye+LrEF0Uu7GS+Njr+r5mG52zRLMxs9Ag==",
        }
    ],
}
