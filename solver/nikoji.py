"""The NIKOJI solver."""

from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def region_profile(src_cell: Tuple[int, int]) -> str:
    """Generate reusable anchor, and transformed offset predicates for a shape with source cell."""
    r, c = src_cell
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    rules = f"region_size({r}, {c}, N) :- N = #count {{ R, C : {tag}({r}, {c}, R, C) }}.\n"

    # construct a bounding box to enclose the shape and get the anchor efficiently
    rules += f"bbox_Mr({r}, {c}, Mr) :- Mr = #min {{ R : {tag}({r}, {c}, R, _) }}.\n"
    rules += f"bbox_MR({r}, {c}, MR) :- MR = #max {{ R : {tag}({r}, {c}, R, _) }}.\n"
    rules += f"bbox_Mc({r}, {c}, Mc) :- Mc = #min {{ C : {tag}({r}, {c}, _, C) }}.\n"
    rules += f"bbox_MC({r}, {c}, MC) :- MC = #max {{ C : {tag}({r}, {c}, _, C) }}.\n"

    # make transformed offset predicates
    transforms = [
        ("R - Mr", "C - Mc", "Mr", "Mc"),
        ("-R + MR", "C - Mc", "MR", "Mc"),
        ("R - Mr", "-C + MC", "Mr", "MC"),
        ("-R + MR", "-C + MC", "MR", "MC"),
        ("C - Mc", "R - Mr", "Mc", "Mr"),
        ("-C + MC", "R - Mr", "MC", "Mr"),
        ("C - Mc", "-R + MR", "Mc", "MR"),
        ("-C + MC", "-R + MR", "MC", "MR"),
    ]
    for k, (dr, dc, vr, vc) in enumerate(transforms):
        rules += f"t_offset({r}, {c}, {dr}, {dc}, {k}) :- {tag}({r}, {c}, R, C), bbox_{vr}({r}, {c}, {vr}), bbox_{vc}({r}, {c}, {vc}).\n"

    return rules.strip()


def avoid_congruent_shape(src_cell: Tuple[int, int], dst_cell: Tuple[int, int]) -> str:
    """Generate a rule to check if two cells have identical shapes and letter position."""
    r0, c0 = src_cell
    r1, c1 = dst_cell
    rule = f"same_size({r0}, {c0}, {r1}, {c1}) :- region_size({r0}, {c0}, N), region_size({r1}, {c1}, N).\n"
    rule += f"mismatch({r0}, {c0}, {r1}, {c1}) :- not same_size({r0}, {c0}, {r1}, {c1}).\n"
    rule += f"misshape_k({r0}, {c0}, {r1}, {c1}, K) :- same_size({r0}, {c0}, {r1}, {c1}), K = 0..7, t_offset({r0}, {c0}, DR, DC, 0), not t_offset({r1}, {c1}, DR, DC, K).\n"
    rule += f"same_shape_k({r0}, {c0}, {r1}, {c1}, K) :- same_size({r0}, {c0}, {r1}, {c1}), K = 0..7, not misshape_k({r0}, {c0}, {r1}, {c1}, K).\n"
    rule += f"mismatch({r0}, {c0}, {r1}, {c1}) :- same_size({r0}, {c0}, {r1}, {c1}), not same_shape_k({r0}, {c0}, {r1}, {c1}, _).\n"
    rule += f":- not mismatch({r0}, {c0}, {r1}, {c1}).\n"
    return rule


def check_identical_shape(src_cell: Tuple[int, int], dst_cell: Tuple[int, int]) -> str:
    """Generate a rule to check if two cells have identical shapes and letter position."""
    r0, c0 = src_cell
    r1, c1 = dst_cell
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)

    rule = f"same_place({r0}, {c0}, {r1}, {c1}, R, C) :- {tag}({r0}, {c0}, R, C), {tag}({r1}, {c1}, R + {r1 - r0}, C + {c1 - c0}).\n"
    rule += f":- {tag}({r0}, {c0}, R, C), not same_place({r0}, {c0}, {r1}, {c1}, R, C).\n"
    rule += f":- {tag}({r1}, {c1}, R + {r1 - r0}, C + {c1 - c0}), not same_place({r0}, {c0}, {r1}, {c1}, R, C).\n"
    return rule


class NikojiSolver(Solver):
    """The NIKOJI solver."""

    name = "NIKOJI"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7ZZLb+JIEMfvfIqor2lp3DYP29IcDIE8lhCSgNhgIWSIASc2nTU2yRjx3VNdQPzAZBZFG81hZXWp/Kt+VFWLv1n8E1q+TVV4FJVKlMGjFGUcsqThkLZPxwlcWz+hRhjMuA8OpTeNBp1Y7sKmVw+zZo0br2fG30s16PfZuRReSr2nxtPpnffXpaP4rNFS29fta0eeGhe16m25flpuh4tuYC9vPVZ96vY7k3Zvqsm/6q1+MerfSKWr/uTH0uj+LJjbHAaFVaTpkUGjc90kMqE4GBnQ6FZfRdd61KLRPYQIZQNKvNANnDF3uU92LGqCxwiVwa3Hbg/jwqttIJPAb219cB/AHTv+2LWHzQ1p62bUoUScXcXVwiUeX9riMFiG72PujRwBRlYA7VvMnBdCFQgswkf+HG6nssGaRsamgvq/rAA22VUg3E0FwsupQBT231agDdZruJw7qGGom6KcbuyqsXuvr8C29BVRNLHUgFQ2N0iKkgDVBFCyoChALQYllgVlAc5iUC4J0EgAnHEeg0pFgIsEUAW4jIGKMxKZanLmFA1rSWTKJCwmsYZJ2WqYlC4H+sKwOw9oG2hltB1oHo0UtGdoJbQltE2cU0fbQ1tDW0RbxjkV0f6jLujr6RCFQfc1FaqrgLCo0ABF+CAzKnRQ+W26plxGRYqf0ve+DwomqT9O7ZMW9z3LhV9EK/RGtr97Bz0iC+4OF6E/scb20H6zxgHRN5KYjKTYHPdIIZfzF9eZ5+2wC6WgM51z384NCWhDzge2EqGcrUbcf8zk9Gq5broW/Fik0EZQUijwQS0S75bv89cU8axglgIJZUntZM8zzQysdIrWs5U5zYvbsS6QN4LDVKgsLvP/j8cf/PEQFyV9s0J9VTBNaPiHuNHohpKXcGgNoecE/qxQES6C3B0Z0MpHBpQiOzbASvmBD3k+FFbhl3Sw2MPhb784VAPufyLNcTCLcwQa6CcanYjm8QNynIhm+Z72imT35RdojgIDzYowoH0dBrgnxcAOqLHYNSvIIqusJouj9mRZHJVUZnNQeAc=",
        },
        {
            "data": "m=edit&p=7ZVNb+JMDMfvfIpqrh1p8wIUIj0HoNA3SKEFsQUhFGiAtAnTnSS0TxDfvbYB5QVa7R626mEVxXJ+nnhsT/SP/yu0pM1LcOklrnAVLj2v0a0pZbqV3dV1Atc2TnglDBZCgsP5baPBZ5br2/z6YdGsicrreeXnqhQMBuqFEl4p/afG0+mdd3Pl6FJtmKV2q91ytHnlslbtFOunxXbo9wJ71fHU6lNv0J21+/Oy9n/dHOSjwa1SuB7Mfqwqvf9yw10No9w6KhtRh0cXxpBpjNOtshGPOsY6ahmRyaN7CDGujjjzQjdwpsIVku1Z1ARPZVwDtx67fYqjV9tCVQHf3PngPoA7deTUtcfNLWkbw6jLGe5dpbfRZZ5Y2bgZvEbPU+FNHAQTK4Dx+QvnhXEdAn74KJ7D3VJ1tOFRZdtB/Tc7gCT7DtDddoDekQ6wsb/bQXm02cDh3EEPY2OI7fRitxS798YarGmsmVbEVytQyvYEma4iqCZACUEtAcoIzmOQVxDUE0BH0IhBgZJeJACtuEyAPIKrGBQ1BNcJQHXcxOCMAE5xB0pnCFoJQCvMGJQJ3MZAVWib9p7AVFSazQPZBlmNbBdGxyOd7DlZhWyBbJPW1Mn2ydbI5skWac0ZDv+PjucLyhlqRdKb+Cp87fMoB9/O49w+MYX0LBe+dzP0JrbcP4PaMF+4Yz+UM2tqj+03axowYyt4yUiKLSlHCrlCvLjO8liGfSgFnflSSPtoCKENNX+QCkNHUk2EfMzU9Gq5broX+hWk0FYuUiiQoAWJZ0tK8ZoinhUsUiChG6lM9jIzzMBKl2g9W5ndvHgcmxx7Y3QPda7hYf77NXzjXwMelPLdFOi7lUPfuJCfCE4czOIjsgP0E+VJRI/xD0QmEc3yA0XBYg9FBegRXQGalRZAh+oC8EBggH2gMZg1KzNYVVZpcKsDscGtknozHOXeAQ==",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

        all_src: List[Tuple[int, int]] = []
        locations: Dict[Union[int, str], List[Tuple[int, int]]] = {}
        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            locations.setdefault(clue, [])
            locations[clue].append((r, c))
            all_src.append((r, c))

        for (r, c, _, _), _ in puzzle.text.items():
            current_excluded = [src for src in all_src if src != (r, c)]
            self.add_program_line(
                grid_src_color_connected((r, c), exclude_cells=current_excluded, color=None, adj_type="edge")
            )

        for clue in locations:
            cells = locations[clue]
            leader = cells[0]
            self.add_program_line(region_profile(leader))
            for member in cells[1:]:
                self.add_program_line(check_identical_shape(leader, member))

        location_keys = tuple(locations.keys())
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                leader1 = locations[location_keys[i]][0]
                leader2 = locations[location_keys[j]][0]
                self.add_program_line(avoid_congruent_shape(leader1, leader2))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
