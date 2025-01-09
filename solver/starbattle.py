"""The Star Battle solver."""

from typing import List

from noqx.puzzle import Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    assert puzzle.param["stars"].isdigit(), "Invalid star count."
    num_stars = int(puzzle.param["stars"])

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="star__2"))

    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_adjacent_color(color="star__2", adj_type=8))

    solver.add_program_line(count(num_stars, color="star__2", _type="row"))
    solver.add_program_line(count(num_stars, color="star__2", _type="col"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(count(num_stars, color="star__2", _type="area", _id=i))

    for (r, c, d, _), symbol_name in filter(lambda x: x[0][0] != -1, puzzle.symbol.items()):
        validate_direction(r, c, d)
        if symbol_name == "star__2":
            solver.add_program_line(f"star__2({r}, {c}).")
        if symbol_name == "star__0":
            solver.add_program_line(f"not star__2({r}, {c}).")

    solver.add_program_line(display(item="star__2"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Star Battle",
    "category": "var",
    "examples": [
        {
            "data": "m=edit&p=7VVda9swFH3Pryh61oO+bNl+67p0L127rR2lmBDcNFvDUtLlYwyH/Peee3U9UxZWWlhhMBzLJ5Lu0dE9uvbq+6ZZTrV19POFNtriCmXg28eMbyPXxWw9n1YH+nCzvl0sAbQ+Oz7WX5r5ajqoKRLXaLBty6o91O27qlZOab6tGun2Y7Vt31ftULfnGFKYq9sTIKu0Axz28JLHCR2lTmuATwUDXgFOZsvJfDo+ST0fqrq90IrWecPRBNXd4sdUpTD+P1ncXc+o47pZYzOr29m9jKw2N4tvG5lrRzvdHia5V3vk+l4uwSSX0B65tAuSu1o3yxdJTYG/iyxHux2S/Qkyx1VNij/3sOjhebVFe1ptVfAUCj8sO4Jey2NXNBYw5rAEr+Zo8JgHHbcX4NKt5/Ytt4bbjNsTnjMEjStxZqxVFai8ido7rEnYWuAoGHO8zHEeuBSM+aSRcQEMTYQ9YoPE+lL7LEs4IDaT2IDzmhvB4MmFJ6MzLGtliI0SmyM2SmwEfyH8kQqhEAzOUjipFkrhieAphaeIOhhZqyiARXNpgHPBqCkj/MhPkPwgDjhpQJwOLq2FOGAnGPySQ8QBJx7E6eCTBowDCw9yGCSHARUdMtFDXhjZl0FujezdYC9W9mhN7x35ZZMGPIE7H5E3K5wW+bGSB/LLdT6C0wunB2fndQ6cdxj8ufDn4O/8Ii+i9JMXsesnv2Rd8qXzkd9RkueYA3c+Yr+x8xHafnkNbYVoKzBffEfukVvxxVGeJf8efvnEjyewzPfIs0/8nOcu/zifIYiPAZxBOAM4g3AGJx6haC65dI64DdzmXFKRivdZ5f2onHPI7MsZbx1VUPGbvudlBf6k4jqTD8GjK/57faNBrYY3X6cHp4vlXTPHG/j8trmfKnzgdgP1U/Fde/pe/v/mveo3jxJvXlwaf+ncPyGnRk5RGe2ZVvebcTOeLHCikLE/9edxf3/hn8ezp//Vs4MXA5uazqAaDR4A",
        },
        {
            "url": "https://puzz.link/p?starbattle/15/15/3/31g94h1gk30glmiuum28c52kl8mh0i10o51gh4i1go2h84a4802gt5hah8la6046hc9aign1ga18424a42h8",
            "config": {"stars": 3},
            "test": False,
        },
    ],
    "parameters": {"stars": {"name": "Stars", "type": "number", "default": 2}},
}
