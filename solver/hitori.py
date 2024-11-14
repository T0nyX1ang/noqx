"""The Hitori solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, grid, shade_c, unique_num
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


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
            "data": "m=edit&p=7VdNb9s4EL37VwQ886CRqM9bmk32knW2dYogMAzDcR3EWBtO/VEUMvzfM2/kdEZKDttDExQoDBEzIufxvSE5lDdfd5P1zBN5inxS+Miz5UOa+UCFTymXJzr+rufbxaw68ae77cNqzYb3VxcX/n6y2Mx6w+OoUW9fl1V96uu/q6Ej513MD7mRrz9W+/qfqu77esBdzgd+d9kMitk8V/NG+mGdNS8pYrt/tNm8ZXM6X08Xs/Fl8+bfalhfe4d5Pkg0TLdcfZu5Iw/409Xybo4Xd5Mti9k8zB+PPZvdl9V/u+NYGh18fdrQHbxCN1G6MBu6sF6hCxW/mG45Ohw47Z+Y8LgagvtnNQs1B9We2361d0nMoTGvtayMSxJ2sQue/QBf3ZTdXN2s3Zu3sQp2E3XLVm+I2E3VJXZLdUHL9AK5ULeNHIBsSKeAztRtQ6eAVqxUFGO/H30oVokpFBssKA7qgpeZOQO2BmfAVhUZoJV2BmhNSAZoE9uFhmaDBc3KK4dkxcohWTXmbVo5oFVEDmQTC2SNLYBseBSAVhEFoJVHAcUmWLaPJreAZAsGzSYaxHSlSmCb6FKWSl2Aq4xSsNUFtOarBLTSLtuaS9lBP1yKIFqJUATRCkYRmCkaRbJYxge8Jpwi4Bs8Ar6miQj4KoWovWBEUK55IoJ0G98+l0QQb/hRh1/c4R938GPga3ooBr7hHwPfzB8D3+Qnhn6zzhQjAWZAggQYwQkSYCaUsmQmkNJiAaW4WABMYDLQKS8k9cVMIAXGKArIgI2XnWsmDEiBYRTax5WkRJkJpMwYAlJnTLzUGdsPfLMkUmksgabWGL+TgbSzxzJkwABmyICJl1plThdJxTGbQCqOBWyXHJKaYwhI0bGAUnbsgPb5pbxdDylvn2DKuymQwvXMgC8wkmvsVtoLaWNpr/mW83Ui7V/SRtKm0l7KmHNpb6Q9kzZIm8mYHPfk/7xJ5Q4Nza0UN9fqG3AbJthsL3/YUr/921Fv6Aa79f1kOuPPnP5ueTdbn/RX6+Vk4fi78tBz3508sn3Cn0/Nd/rUxBJEP/XB+f6ndsjZ5bNTX3n3uBtPxtPVwvG/FY/3oXjx/s3Z89F2D/Ptaj13o94T",
        }
    ],
}
