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
            "data": "m=edit&p=7VXbattAEH3XV4R9noe96P7mOHZacJ22cQlBCCM7aiMqoVS2Slmjf8/syLZckUtNqOlDWXY4OrPDzpllRqsfdVKl4ONSPnAQuJQtaUse0ObbNcvWeRqewaBe35cVAoCr8Ri+JvkqBSvaHoutjQ5CPQB9GUZMMqAtWAz6U7jRH0I9BX2NLgYiBlbU+TpblnlZsR2nJ4gEA4lw1MEb8hs0bEnBEU+3GOEtwmVWLfN0PmmZj2GkZ8DM3ecUbSAryp8pa8Poe1kWi8wQi2SNClf32QMDhY5VfVd+r9nuhgb0oFUw+kMFqlOg9grU0wrkX1cQxE2Dj/MZNczDyMj50kG/g9fhpjFpbZgKTOgAU2lfkNncEOcHhOoTtiGGHeGIPuEa4qIjXMcQ4wOCTlx2hOcZ4t0B4RvifUf4Xi/TQPZuCYJepoLzXozgfTWC/y4H6yKoOrdkx2Ql2RkWD7Qie0GWk3XITujMiOwN2SFZm6xLZzxT/qMe6O3pMCWw+oGP6jzsfR8LoAzGSeBjBdWr6UbSpaHRLee037EVsdHdt/RsWlZFkmNHTOtikVa7b5xHjcV+MdqRAmlC/o+of3hEmYfiJ+6Dt7ZlhAXftxDoK2AP9TyZY80Z/hLBuG1sqiMdgXukQ9niWIdwnnbsh8Bzbl++IPZ598kfDmdUbD0C",
        },
        {
            "data": "m=edit&p=7ZTJTsMwEIbveQrk8xwSu0uSW+nCVsLSIlRFEWpLgIhEgbRByFXenZlJi3PgAAdQD8jyr9+f7XjGdrx6LedFDC4W5YINDhbVklyl7XG1t2WarNPYP4BeuX7KCzQAF6MRPMzTVQxWuB0WWRvt+boH+sgPhRTA1RER6Ct/o899HYCeYJcAJwKRlek6WeZpXogd02N0jgCJdmjsLfeT69fQsdEHW492hnaZFMs0vhvX5NIP9RQErX3Is8mKLH+LRT2N28s8WyQEFvM1Zrh6Sl4EKOxYlff5cyl2K1Sge3UGw29moEwG6jMD9XUG8tcz8KKqwsO5xhzu/JDSuTHWNXbibyoKayNkh6b2MJT6BIVyCBw2gEug3wAegYEBLZvAsAEUgZEBbf7oUQPwiOMGaBE4MaAjCZw2AMdxZkCXwdgAt0vgvAF4RGCAx+DCAMfmZS53BHfF4b2ZsY5YJesUtw60Yh2w2qxt1jGPGbLesvZZW6wdHtOlzf/R8fxBOKHs8JNgSvtv25GFd+f+MT4I8iKbp3jfgzJbxMWuja9NZYl3wTVUIGnK/wO0xw8QHZS9b/d838LBPy+yPgA=",
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
