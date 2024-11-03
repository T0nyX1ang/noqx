"""The Aquarium solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.solution import solver


def area_gravity(color: str = "black") -> str:
    """
    Generates a constraint to fill the {color} areas according to gravity.

    A grid rule should be defined first.
    """
    target = f":- area(A, R, C), area(A, R1, C1), R1 >= R, {color}(R, C), not {color}(R1, C1)."
    return target.replace("not not ", "")


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(area_gravity(color="gray"))

    for (r, c), num in filter(lambda x: x[0][0] == -1 and x[0][1] >= 0, puzzle.text.items()):  # filter top number
        assert isinstance(num, int), "TOP clue must be an integer."
        solver.add_program_line(count(num, color="gray", _type="col", _id=c))

    for (r, c), num in filter(lambda x: x[0][1] == -1 and x[0][0] >= 0, puzzle.text.items()):  # filter left number
        assert isinstance(num, int), "LEFT clue must be an integer."
        solver.add_program_line(count(num, color="gray", _type="row", _id=r))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Aquarium",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VZNb+M2EL37Vyx05kH8FKlbunV6SbNtk2KxMIyF49V2gyZw68RFocD/fd8MhxYtFCiKougWKGyRT89vRjPDIa2nXw+b/aC0pq+NqlVAyvnAl9aGr1Y+t/fPD0P/Sl0cnj/t9gBKvbm8VB83D0/DYqXZul0vXsbUjxdq/KZfNbpRjcGlm7Uav+9fxm/7canGG/zUKA3uKosM4HKCb/l3Qq8zqVvga8GA7wC39/vtw/D+KjPf9avxVjX0nK/YmmDzuPttaCQOut/uHu/uibjbPCOZp0/3v8gvT4cPu58PotXroxovcrg3Jdw4hWuncAnmcAn9QbiUxT8cblofjyj7Dwj4fb+i2H+cYJzgTf+C8bp/aawlU4dY8to01hFhK8LPFWFOdHOTSISviDQjXEtEqgg9VxgiuoqYPyWwooqjYwW6rBCJFZVT3c4l2sy96JxObeVZEysmsKaKTkfWnDJCeTUX+R2PlzwaHm+xBmq0PH7NY8uj5/GKNUssjYmdMhGlNNg6MQKjioQ7d447rBDh0E44JmUSikw4tcq2mccMjAVkHlu94C5AjzVg7OFH+GCAkSzziIdKyrYGtpnHDCxxJjvhDjEn9Fex7YoGPk88NJ3kEiiXkhfFj1ZkPfhU8kKOBQfEGUuOwElijnrCAXlFyStRjpIL9FZnW8zAWYMZuOTokEuOB7OyJseDGVjqaeDH5GexbcEmKEs9TdiBp3YutrQbCFv4pI3AGsRw0gN78e/h34tPnMTWS809/ATxE+AnSmwRfBTbCNsothG2sbKt/XcSQ4fnFlt6VifxdPSXMPlxbeYxK6cL78FnP5jBlxjwrCRxpniGnc494PDPUrBN6KWU+8RG9JisF+MomogeK/liTU8aWlNZd4s+wf2EpQcwA8taQO9KD9BaFz31sPSepT6XXrXYCzYUDE0QDfrWSt9a9PMZLrYaeWnJq4WtYNrXuJd+gH86jxlD40TvoHGlZ/CsGtPpzH2FHAvW1KuSVwuNLj1M/VzpjdSkRQ0LNqgPHfDsn/pNeE89WeEgfrAHbRA99tqpzoTpkGSM3IPk4qluFfZSQ4/cfckdejpyOR6qSXXO0HHNGDUxojfwU/Ym3l2m/QXMPnGgvuVj9TWPjsfAx21Hf4h/6S/z75/sfxrOCitO71/nH7yH/de49WLV3Bz2HzfbAa8ryw8/Da+ud/vHzQPurg+Pd8O+3ONt8bhofm/4Wll6+fz/BfJfeoGkJWi/tD3xpYWDXbpefAY=",
        },
    ],
}
