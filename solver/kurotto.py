"""The Kurotto solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.reachable import count_reachable_src, grid_src_color_connected
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(adjacent())

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(f"not black({r}, {c}).")
        if isinstance(num, int):
            solver.add_program_line(grid_src_color_connected((r, c), color="black"))
            solver.add_program_line(count_reachable_src(num + 1, (r, c), color="black"))

    solver.add_program_line(display())
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Kurotto",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VU9b9swEN31KwzOHHSkvjc3jbu46oddBIEgBLKrIEZkKJWtoqDh/567kxpSbZYODTIENA/v8T74eKbNw4++6moJij46kb4EHEEa8NRxyNMfx3p3bOpsJuf98a7tEEj5abGQt1VzqL1ijCq9k0kzM5fmQ1YIEFIonCBKab5kJ/MxM7k0K3QJGeDacghSCC8tvGI/oYthEXzE+YAjhNcIt7tu29Q3S/TiyuesMGspaJ93nE1Q7NuftRh1EN+2+82OFjbVEQ9zuNs9jJ5D/72978dYKM/SzAe5q2fkaiuX4CCX0H+T2zy0zwlNy/MZG/4Vpd5kBan+ZmFi4So7oc2zk9ABpoYyGr4TEfhIfUtDpPqJhoA0sZRygycaUS7Y5IiiY0ujyU4xRdvSsZoEJ3qyU0K5dqeUKosZNvP3AmUDWJ5M9gJ/qhSA6tnyAPEfPJ20ARTVd/IV9cXxazqMk6+pvuunelYeBMSdetzJyOGUb7sBEbXDOR9wM233IKIDp5bH095DSoLtBsonwS6nAzocyO92WAFJsDuoSYvwMgFfqWu2C7aK7RpvnDSa7Xu2PtuQ7ZJjLtlesb1gG7CNOCamO/tPt/oF5BQ64D/Hv0f4tk6j9Aqx6rvbalvjP1Xe7zd1N8vbbl81Ah+Fsyd+CZ54jfGNeXsnXvydoOb7r+139drk4C9d3Pddezy2ovQeAQ==",
        },
        {
            "url": "https://puzz.link/p?kurotto/17/13/7i4i-1ai4iay1i6ibi0y3ibi9i-14iay4i7i-10i4y-11iei6ici3y1ibi7i2y-10i8i0i4i1",  # this example will probably TLE
            "test": False,
        },
    ],
}
