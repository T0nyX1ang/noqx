"""The Onsen-Meguri solver."""

from typing import Iterable, List, Tuple, Union

from .core.common import area, count, direction, display, fill_path, grid, shade_c
from .core.helper import full_bfs
from .core.loop import single_loop
from .core.neighbor import adjacent
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def area_border(_id: int, ar: Iterable[Tuple[int, int]]) -> str:
    """Generates a fact for the border of an area."""
    borders = []
    for r, c in ar:
        for dr, dc, d in ((0, -1, "l"), (-1, 0, "u"), (0, 1, "r"), (1, 0, "d")):
            r1, c1 = r + dr, c + dc
            if (r1, c1) not in ar:
                borders.append(f'area_border({_id}, {r}, {c}, "{d}").')
    rule = "\n".join(borders)
    return rule


def onsen_rule(target: Union[int, str], _id: int, area_id: int, r: int, c: int) -> str:
    """
    Generates a rule for an Onsen-Meguri puzzle.

    An area fact, a grid direction fact and an area border fact should be defined first.
    """
    rule = f"onsen({_id}, {r}, {c}).\n"
    rule += f"onsen({_id}, R, C) :- grid(R, C), adj_loop(R, C, R1, C1), onsen({_id}, R1, C1).\n"

    if target != "?":
        num = int(target)
        rule += f":- area(A, R, C), onsen({_id}, R, C), #count {{ R1, C1: area(A, R1, C1), onsen({_id}, R1, C1) }} != {num}."
    else:
        anch = f"#count {{ R1, C1: area({area_id}, R1, C1), onsen({_id}, R1, C1) }} = N"  # set anchor number for clue
        rule += (
            f":- area(A, R, C), onsen({_id}, R, C), {anch}, #count {{ R1, C1: area(A, R1, C1), onsen({_id}, R1, C1) }} != N."
        )

    rule += ":- onsen_loop(R, C), not onsen(_, R, C).\n"
    return rule.strip()


def onsen_global_rule() -> str:
    """Generates global rules for an Onsen-Meguri puzzle."""
    # any area, any onsen area, go through border at most twice
    rule = ":- area(A, _, _), onsen(O, _, _), #count { R, C, D: onsen(O, R, C), area_border(A, R, C, D), grid_direction(R, C, D) } > 2.\n"

    # two different onsen loops cannot be connected
    rule += ":- onsen(O1, R, C), onsen(O2, R, C), O1 != O2.\n"

    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="onsen_loop"))
    solver.add_program_line(fill_path(color="onsen_loop"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(single_loop(color="onsen_loop"))

    onsen_id = 0
    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(area_border(i, ar))
        solver.add_program_line(count(("gt", 0), _id=i, color="onsen_loop", _type="area"))

        for rc in ar:
            if rc in puzzle.text:
                r, c = rc
                data = puzzle.text[rc]
                solver.add_program_line(f"onsen_loop({r}, {c}).")
                solver.add_program_line(onsen_rule(data if isinstance(data, int) else "?", onsen_id, i, r, c))

                onsen_id += 1  # fix multiple onsen clues in an area, onsen_id and area_id may be different now

    solver.add_program_line(onsen_global_rule())
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Onsen-Meguri",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VTLbtswELz7Kwye9yDqwYdubur24rqPuAgCQQjsRG2M2lFrx0Ugw/+eWWpV6RCgKPpADgWt9XA5XO0sl9p/Oyx3FVmMxFFEGiOJ0vCYiH/dWKzvN1U+psnh/rbeARC9ndOn5WZfjQohlaNj4/NmQs3rvFCxovBoVVLzPj82b/JmSs05lhRp+GZAWlEMOO3hRVhndNY6dQQ8b7EBvAS8Xu+uN9XVrA30Li+aBSl+z4uwm6Ha1t8r1W4L8+t6u1qzY7W8h5b97fqrrOwPN/WXg3B1eaJm0qY7eyLdpE+XYZsuo7+V7mZ9Vz08lakvTydU/ANyvcoLTvtjD10Pz/Mj7Dw/qjTCVpxseyjK8FSNkac4HDsSmWKPDjsvg30VbBzsAoGpSYJ9GWwUbBbsLHCmeJ9OLOnUqTxGxDQjnRnB8Ged3wH7FmdoQaMFg2OEk3nSFskxRlNqKxyDhrWxYHBYAGMLjhOORXwn8S04XjgOHC8cFwMngj3FkXC8Bpb4PgYWjk+Bs4CxTrEWP2tMO40G2PZ6uzqwxqzTOKgJ6+1qwnr5dIIuxDESxwxqYqDLdLoGdWC9VvwOfid+1ug6jQlwKloGdYDGH3WARu1bjdr3NQl6pQ74B27j4F9qgsO/CC1wFmwarAmtYbkjf6lnf78Lf5pOEUPpYOBM/vSsHBVqhns8nte77XKD2zy9+TyYzQ/bVbXr5viOnkbqQYUH91FT+v/T+u8/rVz96Lk163NLB9dH1Xf76k6Vo0c=",
        },
        {
            "url": "http://pzv.jp/p.html?onsen/10/10/akkh92j6mt9pjvfti91svv1vvovv3g3f04ti3m2n1j1x1zq2v3n3",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?onsen/15/15/9018m2kqm9jbr3a9f853qcfj996k6esa8alac2v892cvv0sj4086g5lb4a6qqeh7q2404c5nvq8cvi30m098zzzzzzj.u..zzzzi",
            "test": False,
        },
    ],
}
