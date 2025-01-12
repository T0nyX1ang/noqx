"""The Martini solver."""

from typing import List, Tuple

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode, target_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_area_adjacent
from noqx.rule.reachable import area_color_connected, grid_color_connected, grid_src_color_connected
from noqx.solution import solver


def count_reachable_src_white_circle(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4):
    """
    Generate a constraint to count the reachable white circles starting from a source.

    A grid_src_color_connected should be defined first.
    """

    src_r, src_c = src_cell

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    rop, num = target_encode(target)

    return f":- #count{{ R, C: {tag}({src_r}, {src_c}, R, C), white_circle(R, C) }} {rop} {num}."


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(area_color_connected(color="gray", adj_type=4))
    solver.add_program_line(grid_color_connected(color="gray", adj_type=8))
    solver.add_program_line(avoid_area_adjacent(color="gray", adj_type=4))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        validate_direction(r, c, d)

        if symbol_name == "circle_L__1":
            solver.add_program_line(f"not gray({r}, {c}).")
            solver.add_program_line(f"white_circle({r}, {c}).")

        if symbol_name == "circle_L__2":
            solver.add_program_line(f"gray({r}, {c}).")

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        if isinstance(num, int):
            solver.add_program_line(grid_src_color_connected((r, c), color="not gray", adj_type=4))
            solver.add_program_line(count_reachable_src_white_circle(num, src_cell=(r, c), color="not gray"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Martini",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VRdb9owFH3nV1R+9gO2g6F56zrYC6PrYKqqKEKBpisaKF0g02TEf++5N86CSKpulda9TFack+Ob63OPP7bfiyRPpUUzA9mVCk1by48KAn66vs1Wu3UansmLYveQ5QBSXo1G8j5Zb9NO5KPizt6dh+5aug9hJJSQQuNRIpbuOty7j6GbSDfFkJADcOMySAMOa3jD44QuS1J1gScl7gPeAi5X+XKdzscYBfMpjNxMCprnHf9NUGyyH6nwOuh7mW0WKyIWyQ7FbB9Wj35kW9xl3wofq+KDdBel3GmLXFPLJVjKJdQil6r4y3LP48MBtn+G4HkYkfYvNRzUcBru0U/CvdAB/YqVUeXaiEATYWrC2hOizxFUHBNIpDjdLaWjMQ29xzWWkyD6hO23sYZiGxlYVSM2MK2x7RmojCbbqqHXqte2zsb2NGLZoxMWFo3YKM39DEshneH+Pfdd7nvcjzlmCEuV0lKRr5gab6mMxwaYfGEex/U4RkMrYwOMahjjEJO7/C8f6BLT4aaKCfeAbcVTfp8nQJ4qnv41PY97wHCAsMJFoT3WwBVv6ALxOCAMzwlbaLZes8Vc5C9jzFVpsKTHz2UxF7nNGHn6hGHSDVt1yX3AvWUL+7TXf/M0CG+YwWtQHo3jff26pXtRW0RL9auhvNfiuBOJaZHfJ8sU18Lw7mt6NsnyTbLG16TYLNK8+satfOiIn4KfCE7L4P9F/Y8ualqC7h9d12+wJ1+QE8Fd7Fp3JcVjMU/mywx7DN4xb57hn4k3zfg3rxaHMO48AQ==",
        },
        {
            "data": "m=edit&p=7ZdNb9tGEIbv/hUFz3sguR8kdUvduBfXbWoXQSAIgeMqiFEbSv1RFDL83/PM7kt9B0ULFMkhEMR5OBoO39kd7lL3fz5e3s1dk1zjne9d7Ro+KSQXfeuaph/Kodbn4vrhZj75zr14fPiwuAOc+/nkxL2/vLmfH00VNTt6Wg6T5Su3/HEyrZrKVS3fppq55avJ0/KnyfLMLc/5qXINvtMS1IIv1/g6/250XJxNDZ+JwTfg1fXd1c387Wnx/DKZLi9cZff5Pl9tWN0u/ppX0mHnV4vbd9fmeHf5QDH3H64/6pf7x98Xfzwqtpk9u+WLIvf8gFy/lmtY5BodkGtV/M9yh9nzM8P+K4LfTqam/bc19ms8nzxxPJs8VaG1S5mZpsxNldJYuhxd2HH0+ZINR9PuhjTtsOsZdq9q03YMgpos680oC//WWFUh4m13vVnxXmxXH/Sa0j1vrmjPO3SHvKXYA26rZt+dy95zt/XBSsqQ7EdnfTvRDNRJHq42Hy+YWLf0+fhDPtb5GPPxNMe8ZGB9CjzhlEA6rAt1YawLVppx67c5+MKh3eAGRtd4rVWUOcLMSOYEM4p2r9RxX3HfrfxY7iVujXtxT36x5WyVvzXeyD9yMJ3SHNBjvZKZ+DDGEG/dYpzgXtwbSwPaorRhYWkIaEuKoZaQNvyjzmCamcLMgwuRHszx+HvF9P0qJ9ZF1Yt1ccxj8dYKmcnTi1mCY10Y62JT8mPhRtzAZV6wsOYr1i7YM2HcwYN4MC7XYld5ckw3MnPdaa47esCaOsdb/sKeeK+cWBekDeuCF3t4HBPzj/dCc1AeLCzN7EbBi72x5tczv1EcjTXXnrkeuYF9YT/AjbiL6By5haWfWrY0eLFH24qtFmlmYwxR/mg8jjM6O3FnLJ0dOjtpQ0Po1HsdvdepryxmUPwQGNvCWDZiMbVH1YWFS57I5h0b9a3x6PdwFEdY98W6OIiH5FJTGOvSKqcnT6kFSx4xNUaNP5acYupdM72hcYj0D+frPre1MjM9rN7AwuphxpwXDzF5NM4x4t9k9WfOrx6O9Dm/rVk9jyVGTH8m9SeWeuW3F56gMeS5Hp9HLCzNPNdRzybWRT2b2K38Kz32TKnHsLDGZGCsNNdYWHNKr67mhZxJzzt2pTnaGjLel7WCczGatS5l1poWWd/WTH6te5H1n3MxerQvpJqXv7poxsJFMxYeYwJcrsXC6h/W5KT1EwsXPViXxrWut5wak8SY2P6WxxZOY5/A2l8iGjhfs/RgYY0heqL0YGHVyP4VtWdhyS9OVq/YYrTfYWHlYa+J2kcie8oWJ8Wzn8YkfyJe+0vupZEZk6h9CgtrLtjvxn4LNi/jHkoezsWsCcqf9zXdN/SsSxq3wBhusWrE4hczv0Hzi1V+Xgpe51eD43wM+ZjyK0Nnb4r/6l1y8wXuv72d/KOcKR1if00+/4nffv+Sv8+OptX54937y6s5/0+OF7cfF/fXD/OKP4PPR9XfVf5OPaHh2//DL/T/0Kag/tqe7K9NDmvN7OgT",
            "test": False,
        },
    ],
}
