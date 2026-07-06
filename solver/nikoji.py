"""The NIKOJI solver."""

from typing import Dict, List, Set, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src
from noqx.rule.shape import get_variant_shape, normalize_shape


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


def small_polyominoes(max_size: int) -> Tuple[Tuple[Tuple[int, int], ...], ...]:
    """Generate free polyominoes up to a given size."""
    by_size = {1: {normalize_shape(((0, 0),))}}
    for size in range(2, max_size + 1):
        next_shapes: Set[Tuple[Tuple[int, int], ...]] = set()
        for shape in by_size[size - 1]:
            cells = set(shape)
            for r, c in cells:
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    candidate = (r + dr, c + dc)
                    if candidate not in cells:
                        new_shape = normalize_shape(tuple(cells | {candidate}))
                        next_shapes.add(min(get_variant_shape(new_shape, allow_rotations=True, allow_reflections=True)))

        by_size[size] = next_shapes

    return tuple({shape for size in range(1, max_size + 1) for shape in sorted(by_size[size])})


def small_shape_templates(src_cells: List[Tuple[int, int]], rows: int, cols: int, max_size: int = 4) -> str:
    """Generate template matches for small free polyominoes."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    shapes = small_polyominoes(max_size)
    rules = [
        f"bad_template(SR, SC, S, P) :- valid_template(SR, SC, S, P), template_in(S, P, DR, DC), not {tag}(SR, SC, SR + DR, SC + DC).",
        f"bad_template(SR, SC, S, P) :- valid_template(SR, SC, S, P), template_out(S, P, DR, DC), grid(SR + DR, SC + DC), {tag}(SR, SC, SR + DR, SC + DC).",
        "small_shape(SR, SC, S) :- valid_template(SR, SC, S, P), not bad_template(SR, SC, S, P).",
    ]
    placements = []
    for shape_id, shape in enumerate(shapes):
        placement_id = 0
        for orientation in get_variant_shape(shape, allow_rotations=True, allow_reflections=True):
            shape_cells = set(orientation)
            boundary = set()
            for dr, dc in orientation:
                for nr, nc in ((dr - 1, dc), (dr + 1, dc), (dr, dc - 1), (dr, dc + 1)):
                    if (nr, nc) not in shape_cells:
                        boundary.add((nr, nc))

            for anchor_r, anchor_c in orientation:
                inside = tuple((dr - anchor_r, dc - anchor_c) for dr, dc in orientation)
                placements.append((shape_id, placement_id, inside))
                for dr, dc in orientation:
                    rules.append(f"template_in({shape_id}, {placement_id}, {dr - anchor_r}, {dc - anchor_c}).")
                for br, bc in sorted(boundary):
                    rules.append(f"template_out({shape_id}, {placement_id}, {br - anchor_r}, {bc - anchor_c}).")
                placement_id += 1

    for r, c in src_cells:
        for shape_id, placement_id, inside in placements:
            if all(0 <= r + dr < rows and 0 <= c + dc < cols for dr, dc in inside):
                rules.append(f"valid_template({r}, {c}, {shape_id}, {placement_id}).")
        rules.append(f"small_region({r}, {c}) :- small_shape({r}, {c}, _).")
    return "\n".join(rules)


def avoid_congruent_shapes(src_pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> str:
    """Generate rules to forbid congruent bare shapes between leader pairs."""
    rules = ""
    for (r0, c0), (r1, c1) in src_pairs:
        rules += f"different_leader({r0}, {c0}, {r1}, {c1}).\n"

    rules += ":- different_leader(R0, C0, R1, C1), small_shape(R0, C0, S), small_shape(R1, C1, S).\n"
    rules += "compare_pair(R0, C0, R1, C1) :- different_leader(R0, C0, R1, C1), not small_region(R0, C0).\n"
    rules += "compare_pair(R0, C0, R1, C1) :- different_leader(R0, C0, R1, C1), not small_region(R1, C1).\n"
    rules += "same_size(R0, C0, R1, C1) :- compare_pair(R0, C0, R1, C1), region_size(R0, C0, N), region_size(R1, C1, N).\n"
    rules += "misshape_k(R0, C0, R1, C1, K) :- compare_pair(R0, C0, R1, C1), same_size(R0, C0, R1, C1), K = 0..7, t_offset(R0, C0, DR, DC, 0), not t_offset(R1, C1, DR, DC, K).\n"
    rules += ":- compare_pair(R0, C0, R1, C1), same_size(R0, C0, R1, C1), K = 0..7, not misshape_k(R0, C0, R1, C1, K)."
    return rules


def partition_src_regions(src_cells: List[Tuple[int, int]]) -> str:
    """Require source reachability to describe an exact edge-separated partition."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    rules = f":- grid(R, C), 2 <= #count {{ SR, SC : {tag}(SR, SC, R, C) }}.\n"
    for r0, c0 in src_cells:
        for r1, c1 in src_cells:
            if (r0, c0) != (r1, c1):
                rules += f"different_src({r0}, {c0}, {r1}, {c1}).\n"
                rules += f"different_src({r1}, {c1}, {r0}, {c0}).\n"

    rules += f':- {tag}(SR, SC, R, C), {tag}(SR1, SC1, R, C + 1), different_src(SR, SC, SR1, SC1), not edge(R, C + 1, "{Direction.LEFT}").\n'
    rules += f':- {tag}(SR, SC, R, C), {tag}(SR1, SC1, R + 1, C), different_src(SR, SC, SR1, SC1), not edge(R + 1, C, "{Direction.TOP}").'
    return rules


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
    offsets = [(r - r0, c - c0, r, c) for r, c in member_cells]

    def _valid(r: int, c: int) -> bool:
        if (r, c) in clue_set and (r, c) != src_cell:
            return False
        for dr, dc, mr, mc in offsets:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                return False
            if (nr, nc) in clue_set and (nr, nc) != (mr, mc):
                return False
        return True

    rules = [f"allowed_src({r0}, {c0}, {r}, {c})." for r in range(rows) for c in range(cols) if _valid(r, c)]
    rules.append(f"{tag}({r0}, {c0}, {r0}, {c0}).")
    rules.append(
        f"{tag}({r0}, {c0}, R, C) :- {tag}({r0}, {c0}, R1, C1), allowed_src({r0}, {c0}, R, C), adj_edge(R, C, R1, C1)."
    )
    rules.append(f':- {tag}({r0}, {c0}, R, C), {tag}({r0}, {c0}, R, C + 1), edge(R, C + 1, "{Direction.LEFT}").')
    rules.append(f':- {tag}({r0}, {c0}, R, C), {tag}({r0}, {c0}, R + 1, C), edge(R + 1, C, "{Direction.TOP}").')
    return "\n".join(rules)


def translate_identical_shape(src_cell: Tuple[int, int], dst_cell: Tuple[int, int]) -> str:
    """Generate a translated copy of a leader clue region for a same-letter clue."""
    r0, c0 = src_cell
    r1, c1 = dst_cell
    dr, dc = r1 - r0, c1 - c0
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)

    rule = f"{tag}({r1}, {c1}, R + {dr}, C + {dc}) :- {tag}({r0}, {c0}, R, C), grid(R + {dr}, C + {dc}).\n"
    rule += f":- {tag}({r0}, {c0}, R, C), not grid(R + {dr}, C + {dc}).\n"
    rule += f':- {tag}({r1}, {c1}, R, C), {tag}({r1}, {c1}, R, C + 1), edge(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- {tag}({r1}, {c1}, R, C), {tag}({r1}, {c1}, R + 1, C), edge(R + 1, C, "{Direction.TOP}").\n'
    rule += f":- {tag}({r1}, {c1}, R1, C1), grid(R, C), adj_edge(R, C, R1, C1), not {tag}({r1}, {c1}, R, C)."
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
            "url": "https://puzz.link/p?nikoji/14/13/1k2j3g4g5r67j8h9iaj4bicdh66en2kf-10m-11g9g5g1peq3hf-12g8n-13g7idi-14bhcieh-15o-14-11ejah-12k-10k-13-15h",
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

        for cells in locations.values():
            leader = cells[0]
            self.add_program_line(region_profile(leader))
            self.add_program_line(restricted_src_connected(cells[0], cells[1:], all_src, puzzle.row, puzzle.col))
            for member in cells[1:]:
                self.add_program_line(translate_identical_shape(leader, member))

        leader_cells = [cells[0] for cells in locations.values()]
        self.add_program_line(small_shape_templates(leader_cells, puzzle.row, puzzle.col, 2))

        location_keys = tuple(locations.keys())
        leader_pairs = []
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                leader1 = locations[location_keys[i]][0]
                leader2 = locations[location_keys[j]][0]
                leader_pairs.append((leader1, leader2))
        self.add_program_line(avoid_congruent_shapes(leader_pairs))
        self.add_program_line(partition_src_regions(all_src))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
