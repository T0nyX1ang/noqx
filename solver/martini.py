"""The Martini solver."""

from typing import List, Optional, Tuple, Union

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode, target_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import area_color_connected, grid_color_connected, grid_src_color_connected
from noqx.solution import solver


def count_reachable_src_white_circle(
    target: Union[int, Tuple[str, int]],
    src_cell: Tuple[int, int],
    color: Optional[str] = "black",
    adj_type: Union[int, str] = 4,
):
    """
    Generate a constraint to count the reachable white circles starting from a source.

    A grid_src_color_connected or bulb_src_color_connected should be defined first.
    """

    src_r, src_c = src_cell

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    rop, num = target_encode(target)

    return f":- #count{{ R, C: {tag}({src_r}, {src_c}, R, C), white_circle(R, C) }} {rop} {num}."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(grid_color_connected(color="gray", adj_type=8))
    solver.add_program_line(area_color_connected(color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        for r, c in ar:
            for dr, dc in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                r1, c1 = r + dr, c + dc
                if not (r1, c1) in ar and (r, c) < (r1, c1):
                    solver.add_program_line(f":- gray({r}, {c}), gray({r1}, {c1}).")

    for (r, c, d), symbol_name in puzzle.symbol.items():
        assert symbol_name in ["circle_L__1", "circle_L__2"], f"Invalid symbol name '{symbol_name}'."
        if symbol_name == "circle_L__2":
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")
            solver.add_program_line(f"white_circle({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        solver.add_program_line(grid_src_color_connected(src_cell=(r, c), color="not gray"))
        solver.add_program_line(count_reachable_src_white_circle(target=num, src_cell=(r, c), color="not gray"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Martini",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7ZRPa9tAEMXv+hRlz3vQ/tE60S11415ct6ldTBAiOK5CRG2UWlYpa/zd82a0rowtKA2U5lCExj+PRrNv32q3/t4sNoV0uMyFjKXCpZ3jW1nLdxyuWbldFekbedVsH6sNQMqPo5F8WKzqIspCVR7t/GXqb6R/n2ZCCSk0biVy6W/Snf+Q+on0UzwSUiE3bos08LrDOT8nGrZJFYMngYG3wGW5Wa6Ku3Gb+ZRmfiYFjfOW3yYU6+pHIYIO+r+s1vclJe4XW0ymfiyfwpO6+Vp9a0KtyvfSX7Vypz1yTSeXsJVL1COXZvGX5V7m+z1s/wzBd2lG2r90eNHhNN0hTtKd0JZexcqodm2E1ZQwXcK5k8SAK2hynEAjxe1uqR0909B7PMd2EFSfZAd9WUO1Zx1Y1VmtNb21/R1oGufZXg1Jr17XOxrbc1bLHp1kYdGIjdIcZ1gK6Q3HdxxjjgnHMddcw1KltFTkK4bGr1QmsAGTL5zHdj2u0dDKbMCYDTM2MbnL7/KGbpk2N82YOAG7Q576hz4WfQ719K5JAidgOECscFDowBp8yBs6QAJbYnhO7KDZBc0OY5G/zBjroMGRnjCWw1jkNjP6DIhh0pytGnK0HB1bOKBv/Y92w/Gn/LLV+q2cjFbn14UZvZTzKBPTZvOwWBY4CYbV+qmqy20hcOzuI/FT8J3BSmn/n8T/6CSmJYhf2xf42uRgT+TRMw==",
        },
        {
            "data": "m=edit&p=7ZdNb9tGEIbv/hUFz3sguR8kdUvduBfXbWoXQSAIgeMqiFEbSv1RFDL83/PM7kt9B0ULFMkhEMR5OBoO39kd7lL3fz5e3s1dk1zjne9d7Ro+KSQXfeuaph/Kodbn4vrhZj75zr14fPiwuAOc+/nkxL2/vLmfH00VNTt6Wg6T5Su3/HEyrZrKVS3fppq55avJ0/KnyfLMLc/5qXINvtMS1IIv1/g6/250XJxNDZ+JwTfg1fXd1c387Wnx/DKZLi9cZff5Pl9tWN0u/ppX0mHnV4vbd9fmeHf5QDH3H64/6pf7x98Xfzwqtpk9u+WLIvf8gFy/lmtY5BodkGtV/M9yh9nzM8P+K4LfTqam/bc19ms8nzxxPJs8VaG1S5mZpsxNldJYuhxd2HH0+ZINR9PuhjTtsOsZdq9q03YMgpos680oC//WWFUh4m13vVnxXmxXH/Sa0j1vrmjPO3SHvKXYA26rZt+dy95zt/XBSsqQ7EdnfTvRDNRJHq42Hy+YWLf0+fhDPtb5GPPxNMe8ZGB9CjzhlEA6rAt1YawLVppx67c5+MKh3eAGRtd4rVWUOcLMSOYEM4p2r9RxX3HfrfxY7iVujXtxT36x5WyVvzXeyD9yMJ3SHNBjvZKZ+DDGEG/dYpzgXtwbSwPaorRhYWkIaEuKoZaQNvyjzmCamcLMgwuRHszx+HvF9P0qJ9ZF1Yt1ccxj8dYKmcnTi1mCY10Y62JT8mPhRtzAZV6wsOYr1i7YM2HcwYN4MC7XYld5ckw3MnPdaa47esCaOsdb/sKeeK+cWBekDeuCF3t4HBPzj/dCc1AeLCzN7EbBi72x5tczv1EcjTXXnrkeuYF9YT/AjbiL6By5haWfWrY0eLFH24qtFmlmYwxR/mg8jjM6O3FnLJ0dOjtpQ0Po1HsdvdepryxmUPwQGNvCWDZiMbVH1YWFS57I5h0b9a3x6PdwFEdY98W6OIiH5FJTGOvSKqcnT6kFSx4xNUaNP5acYupdM72hcYj0D+frPre1MjM9rN7AwuphxpwXDzF5NM4x4t9k9WfOrx6O9Dm/rVk9jyVGTH8m9SeWeuW3F56gMeS5Hp9HLCzNPNdRzybWRT2b2K38Kz32TKnHsLDGZGCsNNdYWHNKr67mhZxJzzt2pTnaGjLel7WCczGatS5l1poWWd/WTH6te5H1n3MxerQvpJqXv7poxsJFMxYeYwJcrsXC6h/W5KT1EwsXPViXxrWut5wak8SY2P6WxxZOY5/A2l8iGjhfs/RgYY0heqL0YGHVyP4VtWdhyS9OVq/YYrTfYWHlYa+J2kcie8oWJ8Wzn8YkfyJe+0vupZEZk6h9CgtrLtjvxn4LNi/jHkoezsWsCcqf9zXdN/SsSxq3wBhusWrE4hczv0Hzi1V+Xgpe51eD43wM+ZjyK0Nnb4r/6l1y8wXuv72d/KOcKR1if00+/4nffv+Sv8+OptX54937y6s5/0+OF7cfF/fXD/OKP4PPR9XfVf5OPaHh2//DL/T/0Kag/tqe7K9NDmvN7OgT",
        },
    ],
}
