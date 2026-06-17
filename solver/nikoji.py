"""The NIKOJI solver."""

from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src


def region_profile(src_cell: Tuple[int, int]) -> str:
    """Generate reusable anchor, and transformed offset predicates for a shape with source cell."""
    r, c = src_cell
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    rules = f"region_size({r}, {c}, N) :- N = #count {{ R, C : {tag}({r}, {c}, R, C) }}.\n"

    # Construct a bounding box to compare bare shapes independent of the clue position.
    rules += f"bbox_Mr({r}, {c}, Mr) :- Mr = #min {{ R : {tag}({r}, {c}, R, _) }}.\n"
    rules += f"bbox_MR({r}, {c}, MR) :- MR = #max {{ R : {tag}({r}, {c}, R, _) }}.\n"
    rules += f"bbox_Mc({r}, {c}, Mc) :- Mc = #min {{ C : {tag}({r}, {c}, _, C) }}.\n"
    rules += f"bbox_MC({r}, {c}, MC) :- MC = #max {{ C : {tag}({r}, {c}, _, C) }}.\n"

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
    """Generate a rule to forbid congruent bare shapes."""
    r0, c0 = src_cell
    r1, c1 = dst_cell
    rule = f"same_size({r0}, {c0}, {r1}, {c1}) :- region_size({r0}, {c0}, N), region_size({r1}, {c1}, N).\n"
    rule += f"mismatch({r0}, {c0}, {r1}, {c1}) :- not same_size({r0}, {c0}, {r1}, {c1}).\n"
    rule += f"misshape_k({r0}, {c0}, {r1}, {c1}, K) :- same_size({r0}, {c0}, {r1}, {c1}), K = 0..7, t_offset({r0}, {c0}, DR, DC, 0), not t_offset({r1}, {c1}, DR, DC, K).\n"
    rule += f"same_shape_k({r0}, {c0}, {r1}, {c1}, K) :- same_size({r0}, {c0}, {r1}, {c1}), K = 0..7, not misshape_k({r0}, {c0}, {r1}, {c1}, K).\n"
    rule += f"mismatch({r0}, {c0}, {r1}, {c1}) :- same_size({r0}, {c0}, {r1}, {c1}), not same_shape_k({r0}, {c0}, {r1}, {c1}, _).\n"
    rule += f":- not mismatch({r0}, {c0}, {r1}, {c1}).\n"
    return rule


def translate_identical_shape(src_cell: Tuple[int, int], dst_cell: Tuple[int, int], clue_cells: List[Tuple[int, int]]) -> str:
    """Generate a translated copy of a leader clue region for a same-letter clue."""
    r0, c0 = src_cell
    r1, c1 = dst_cell
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    dr, dc = r1 - r0, c1 - c0

    rule = f"{tag}({r1}, {c1}, R + {dr}, C + {dc}) :- {tag}({r0}, {c0}, R, C), grid(R + {dr}, C + {dc}).\n"
    rule += f":- {tag}({r0}, {c0}, R, C), not grid(R + {dr}, C + {dc}).\n"
    for exc_r, exc_c in clue_cells:
        if (exc_r, exc_c) != (r1, c1):
            rule += f":- {tag}({r1}, {c1}, {exc_r}, {exc_c}).\n"
    rule += f':- {tag}({r1}, {c1}, R, C), {tag}({r1}, {c1}, R, C + 1), edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- {tag}({r1}, {c1}, R, C), {tag}({r1}, {c1}, R + 1, C), edge(R + 1, C, "{Direction.TOP}").\n'
    rule += f":- {tag}({r1}, {c1}, R1, C1), grid(R, C), adj_edge(R, C, R1, C1), not {tag}({r1}, {c1}, R, C).\n"
    return rule


def restricted_src_connected(
    src_cell: Tuple[int, int],
    member_cells: List[Tuple[int, int]],
    clue_cells: List[Tuple[int, int]],
    rows: int,
    cols: int,
) -> str:
    """Generate source reachability with same-letter translation limits built into the domain."""
    r0, c0 = src_cell
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    clue_set = set(clue_cells)
    member_offsets = [(r - r0, c - c0, r, c) for r, c in member_cells]

    rules = []
    for r in range(rows):
        for c in range(cols):
            allowed = (r, c) not in clue_set or (r, c) == src_cell
            if allowed:
                for dr, dc, member_r, member_c in member_offsets:
                    shifted = (r + dr, c + dc)
                    if not (0 <= shifted[0] < rows and 0 <= shifted[1] < cols):
                        allowed = False
                        break
                    if shifted in clue_set and shifted != (member_r, member_c):
                        allowed = False
                        break

            if allowed:
                rules.append(f"allowed_src({r0}, {c0}, {r}, {c}).")

    rules.append(f"{tag}({r0}, {c0}, {r0}, {c0}).")
    rules.append(
        f"{tag}({r0}, {c0}, R, C) :- {tag}({r0}, {c0}, R1, C1), allowed_src({r0}, {c0}, R, C), adj_edge(R, C, R1, C1)."
    )
    rules.append(f':- {tag}({r0}, {c0}, R, C), {tag}({r0}, {c0}, R, C + 1), edge(R, C + 1, "{Direction.LEFT}").')
    rules.append(f':- {tag}({r0}, {c0}, R, C), {tag}({r0}, {c0}, R + 1, C), edge(R + 1, C, "{Direction.TOP}").')

    return "\n".join(rules)


def partition_src_regions() -> str:
    """Require source reachability to describe an exact edge-separated partition."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    rules = f":- grid(R, C), 2 <= #count {{ SR, SC : {tag}(SR, SC, R, C) }}.\n"
    rules += (
        f':- {tag}(SR, SC, R, C), {tag}(SR1, SC1, R, C + 1), SR != SR1, not edge(R, C + 1, "{Direction.LEFT}").\n'
    )
    rules += (
        f':- {tag}(SR, SC, R, C), {tag}(SR1, SC1, R, C + 1), SC != SC1, not edge(R, C + 1, "{Direction.LEFT}").\n'
    )
    rules += (
        f':- {tag}(SR, SC, R, C), {tag}(SR1, SC1, R + 1, C), SR != SR1, not edge(R + 1, C, "{Direction.TOP}").\n'
    )
    rules += (
        f':- {tag}(SR, SC, R, C), {tag}(SR1, SC1, R + 1, C), SC != SC1, not edge(R + 1, C, "{Direction.TOP}").'
    )
    return rules


class NikojiSolver(Solver):
    """The NIKOJI solver."""

    name = "NIKOJI"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VXbattAEH3XV4R9noe96P7mOHZacJ22cQlBCCM7aiMqoVS2Slmjf8/syLZckUtNqOlDWXY4OrPDzpllRqsfdVKl4ONSPnAQuJQtaUse0ObbNcvWeRqewaBe35cVAoCr8Ri+JvkqBSvaHoutjQ5CPQB9GUZMMqAtWAz6U7jRH0I9BX2NLgYiBlbU+TpblnlZsR2nJ4gEA4lw1MEb8hs0bEnBEU+3GOEtwmVWLfN0PmmZj2GkZ8DM3ecUbSAryp8pa8Poe1kWi8wQi2SNClf32QMDhY5VfVd+r9nuhgb0oFUw+kMFqlOg9grU0wrkX1cQxE2Dj/MZNczDyMj50kG/g9fhpjFpbZgKTOgAU2lfkNncEOcHhOoTtiGGHeGIPuEa4qIjXMcQ4wOCTlx2hOcZ4t0B4RvifUf4Xi/TQPZuCYJepoLzXozgfTWC/y4H6yKoOrdkx2Ql2RkWD7Qie0GWk3XITujMiOwN2SFZm6xLZzxT/qMe6O3pMCWw+oGP6jzsfR8LoAzGSeBjBdWr6UbSpaHRLee037EVsdHdt/RsWlZFkmNHTOtikVa7b5xHjcV+MdqRAmlC/o+of3hEmYfiJ+6Dt7ZlhAXftxDoK2AP9TyZY80Z/hLBuG1sqiMdgXukQ9niWIdwnnbsh8Bzbl++IPZ598kfDmdUbD0C",
        },
        {
            "url": "https://puzz.link/p?nikoji/14/13/1k2j3g4g5r67j8h9iaj4bicdh66en2kf-10m-11g9g5g1peq3hf-12g8n-13g7idi-14bhcieh-15o-14-11ejah-12k-10k-13-15h",
            "test": False,  # slow case
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

        for cells in locations.values():
            self.add_program_line(restricted_src_connected(cells[0], cells[1:], all_src, puzzle.row, puzzle.col))

        for clue in locations:
            cells = locations[clue]
            leader = cells[0]
            self.add_program_line(region_profile(leader))
            for member in cells[1:]:
                self.add_program_line(translate_identical_shape(leader, member, all_src))

        location_keys = tuple(locations.keys())
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                leader1 = locations[location_keys[i]][0]
                leader2 = locations[location_keys[j]][0]
                self.add_program_line(avoid_congruent_shape(leader1, leader2))

        self.add_program_line(partition_src_regions())

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
