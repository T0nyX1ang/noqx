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
            "data": "m=edit&p=7Vbfb9s2EH73X1HomQ/iT5F6y7JkL1m6LRmKQjAMx3XXYAncOfEwKMj/3u+OR4sRBnTD0A4DBtvkp8/fne6OR0oPvx3W+63Smr42qlYBKecD/7Q2/Gvlc337eLftX6mTw+OH3R5Aqdfn5+r9+u5huxg0W7fLxdOY+vFEjd/1Q6Mb1Rj8dLNU44/90/h9P56p8Qp/NUqDu8giA3g2wTf8P6HTTOoW+FIw4FvAze1+c7ddXWTmh34Yr1VD9/mGrQk297vft43EQdeb3f3NLRE360ck8/Dh9qP883B4t/v1IFq9fFbjSQ73qoQbp3DtFC7BHC6hPwmXsvjC4abl8zPK/hMCXvUDxf7zBOMEr/onjJf9U2MtmTrEktemsY4IWxF+rghzopubRCJ8RaQZ4VoiUkXoucIQ0VXE/C6BFVUcHSvQZYVIrKic6nYu0WbuRed0aivPmlgxgTVVdDqy5pgRyqu5yG95POfR8HiNNVCj5fFbHlsePY8XrDnD0pjYKRNRSoOtEyMwqki4cy9xhxUiHNoJx6RMQpEJp1bZNvOYgbGAzGOrF9wF6LEGjD38CB8MMJJlHvFQSdnWwDbzmIElzmQn3CHmhP4qtl3RwOeRh6aTXALlUvKi+NGKrAefSl7IseCAOGPJEThJzFFPOCCvKHklylFygd7qbIsZOGswA5ccHXLJ8WBW1uR4MANLPQ38mHwvti3YBGWppwk78NTOxZZ2A2ELn7QRWIMYjnpgL/49/HvxiZPYeqm5h58gfgL8RIktgo9iG2EbxTbCNla2tf9OYuhw32JL9+okno4eCZMf12Yes3K68B589oMZfIkB90oSZ4ovsNO5BxyeLAXbhF5KuU9sRI/JejGOoonosZIv1vSooTWVdbfoE1xPWHoAM7CsBfSu9ACtddFTD0vvWepz6VWLvWBDwdAE0aBvrfStRT+/wMVWIy8tebWwFUz7GtfSD/BP5zFjaJzoHTSu9AzuVWM6nbmvkGPBmnpV8mqh0aWHqZ8rvZGatKhhwQb1oQOe/VO/Ce+pJyscxA/2oA2ix1471pkwHZKMkXuQXDzVrcJeauiRuy+5Q09HLsdDNanOGTquGaMmRvQGfsrexLvLtL+A2ScO1Dd8rJ7y6HgMfNx29ED8i4/MRhaEeiDm5+c/P+Y/G9uA5aeXsZcfvJT917jlYmiuDvv3680W7y5n737Zvrrc7e/Xd7i6PNzfbPflGq+Oz4vmj4Z/g6U30f/fJv+lt0lagvZvvVN+hT3xmXAGVBcH9PhaNR8Pq/Vqs0OPoXbEYzfN+a8ePTb1cvEJ",
        },
    ],
}
