"""The Onsen-Meguri solver."""

from typing import Iterable, List, Tuple, Union

from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, count, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.solution import solver


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


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
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

        for r, c in ar:
            if Point(r, c, Direction.CENTER, "normal") in puzzle.text:
                num = puzzle.text[Point(r, c, Direction.CENTER, "normal")]
                solver.add_program_line(f"onsen_loop({r}, {c}).")
                solver.add_program_line(onsen_rule(num if isinstance(num, int) else "?", onsen_id, i, r, c))

                onsen_id += 1  # fix multiple onsen clues in an area, onsen_id and area_id may be different now

    assert onsen_id > 0, "No onsen clues found."
    solver.add_program_line(onsen_global_rule())

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Onsen-Meguri",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VRJb9s8EL37Vxg8z0HUQpG6uan9XVx3iYsgEITAdtTGqG199VIEMvzf84YaVToEKIouyKGgNX4cPo7mDYc6fD0t9iWlGJGlgDRGFMT+MQH/2jFfHzdlNqTR6fhQ7QGI3k4m9GmxOZSDXFjF4Fy7rB5R/V+Wq1CRf7QqqH6fnes3WT2m+hpLijR8UyCtKAQcd/DGrzO6apw6AJ412ADeAq7W+9WmvJs2gd5leT0nxe955XczVNvqW6mabX6+qrbLNTuWiyPEHB7W/8vK4XRffTkJVxcXqkdNutNn0o26dBk26TL6U+lu1rvy8blMXXG5oOIfkOtdlnPaHztoO3idnWFn2VnFAbbiaJtDUYanaog8xWHZEckUe7TfeevtxNvQ2zkCUx15+9rbwNvE26nnjPE+HaWkY6uyEBHjhHRiBMOftH4L7BqcoAeNFgyOEU7iSKdIjjG6UqfCMejYNBQMDgtgnIJjhZMivpX4KThOOBYcJxwbAkeCHYWBcJwGlvguBBaOi4ETj7FOoRY/a4xbjQY47fS2dWCNSauxVxPW29aE9fLpeF2IYySO6dXEQJdpdfXqwHpT8Vv4rfhZo201RsCxaOnVARq/1wEatWs0atfVxOuVOuAfuImDf6kJDv/Gt8CVt7G3xrdGyh35Uz376134w3TyEEp7A2fyu2fFIFdT3OPhrNpvFxvc5vH9595sdtouy307x3f0MlCPyj+4j5rif5/Wv/9p5eoHL61ZX1o6uD6q2h3KnSoGTw==",
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
