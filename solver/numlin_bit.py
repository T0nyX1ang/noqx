"""The Numberlink solver (bit version)."""

from math import log2
from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c, shade_cc
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.route import single_route


def no_2x2_path_bit() -> str:
    """Generate a rule that no 2x2 path (bit version) is allowed."""
    points = ((0, 0), (0, 1), (1, 0), (1, 1))
    tag = tag_encode("reachable", "grid", "bit", "adj", "line", "white")
    same_str = ", ".join(f"{tag}(R + {r}, C + {c}, B)" for r, c in points)
    no_str = ", ".join(f"not {tag}(R + {r}, C + {c}, B)" for r, c in points)

    rule = f"bit_same(R, C, B) :- grid(R, C), bit_range(B), {same_str}.\n"
    rule += f"bit_no(R, C, B) :- grid(R, C), bit_range(B), {no_str}.\n"
    rule += "bit_same(R, C, B) :- bit_no(R, C, B).\n"
    rule += "no_2x2(R, C) :- grid(R, C), bit_range(B), not bit_same(R, C, B).\n"
    rule += "no_empty(R, C) :- grid(R, C), bit_range(B), not bit_no(R, C, B).\n"
    rule += ":- grid(R, C), no_empty(R, C), not no_2x2(R, C).\n"
    return rule


def clue_bit(r: int, c: int, _id: int, nbit: int) -> str:
    """Assign clues with bit ids instead of numerical ids."""
    rule = f"clue({r}, {c}).\n"
    for i in range(nbit):
        if _id >> i & 1:
            rule += f"clue_bit({r}, {c}, {i}).\n"
    return rule


def num_binary_range(num: int) -> Tuple[str, int]:
    """Generate a rule restricting number represented by bits between 0 and num."""
    nbit = int(log2(num)) + 1
    rule = f"bit_range(0..{nbit - 1}).\n"
    return rule, nbit


def grid_bit_color_connected(color: str = "black", adj_type: Union[int, str] = "line") -> str:
    """Generate a constraint to check the reachability of {color} cells starting from a source (bit version)."""
    validate_type(adj_type, (4, 8, "x", "line", "line_directed"))

    tag = tag_encode("reachable", "grid", "bit", "adj", adj_type, color)
    rule = f"{tag}(R, C, B) :- clue_bit(R, C, B).\n"
    rule += f"not {tag}(R, C, B) :- grid(R, C), {color}(R, C), bit_range(B), clue(R, C), not clue_bit(R, C, B).\n"
    rule += f"{tag}(R, C, B) :- {tag}(R1, C1, B), grid(R, C), bit_range(B), {color}(R, C), adj_{adj_type}(R, C, R1, C1).\n"
    rule += f"not {tag}(R, C, B) :- not {tag}(R1, C1, B), grid(R, C), grid(R1, C1), bit_range(B), {color}(R, C), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1).\n"
    return rule


def avoid_unknown_src_bit(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """
    Generate a constraint to avoid cells starting from unknown source (bit version).

    Use this constraint with grid_bit_color_connected, and adj_type cannot be "edge".
    """
    tag = tag_encode("reachable", "grid", "bit", "adj", adj_type, color)
    return f":- grid(R, C), {color}(R, C), not {tag}(R, C, _)."


class NumlinVBitSolver(Solver):
    """The Numberlink solver (bit version)."""

    name = "Numberlink (Bit Ver)"
    category = "route"
    aliases = ["numberlink", "arukone", "flowfree"]
    examples = [
        {
            "data": "m=edit&p=7VNNb4JAEL3zK8ye57CwqMDNz16ottXGGEIMWhpJsViUxqzhv3d2wNIam9jUeGrWfXn7ZpZ9O+5s3rIgDaGJQ1jAQcchuEmzwdXvMMbRNg6dGrSy7TJJkQAM+314DuJNqHlllq/tpe3IFsgbx2M6A2bg1JkP8t7Zy1tHDkCOMMRAR80tkgykvYpOKK5YpxB1jnxQcqRTpIsoXcThzC2UO8eTY2DqnDbtVpStkveQlT7UepGs5pES5sEWL7NZRusyssmekpeMHY7IQbYKu+4Ju6KyKz7titN2jUvYjaPXcHfKqe3nOVb8Ab3OHE/ZfqyoVdGRs8+VpT0zmmprC20UfwsTDSW0K8HkSuh9ESwldCuhQRmdSmjyowxLP/qGzY+OtY2jb9jimw+0q5PpKWGf0CAc451ACsIuISesE7qU0yOcEHYITcIG5TRVVX5Vt7/YYWYd72ZbWCcbVCHEmQY9w6R+PIz65Ve+5jEXX1dtkKSrIMY3NshW8zA9rLGfc43tGE1P4Bbzv8Wv3+Kq+vxqD/Yy/eNhYcsXD3IIbJ3NgtkiwTeGtVNBbIufAub5gavfGvvS1z4A",
            "config": {"visit_all": False, "no_2x2": False},
        },
        {
            "data": "m=edit&p=7VRLa8MwDL7nVxSffbCdl5Nb9+guWffqKCOE0nYZDUuXLW1Gccl/n6y0czK6w2CMHoZj8X2WjD5LRKu3alqmlLv6syVllMPymMTNJcO9X6Nsnadhj/ar9aIoAVB6NRjQp2m+Sq14F5VYWxWEqk/VRRgTTigRsDlJqLoJt+oyVEOq7sBFKIezqAkSAM8NHKNfo9PmkDPAwx0G+ABwnpXzPJ1Ezcl1GKsRJTrPCd7WkCyL95TsdGg+L5azTB/Mpmt4zGqRve48q+qxeK7IPkVNVb+RGx2Qaxu59qdc+7Bc8Rty8+wl3RxSGiR1DRW/Ba2TMNay7w2UBt6F21pL2hJfwFXdZmwKkQyoMNQGahvqAHUMDYC6n5QzF7hnuO0B9w133C73dG5puK/9QYt7newc07f8UsdzZg4C2REgOAaY1wnRfYBw3c5zhc+/XEAJbe53UwosmGxx2aoJ1JhjpR/QDtAKtCNoBFU22jO0DK2LNsKYc7RjtKdoHbQexvi6lT9q9h/IiZ1maHy33H/vsXsTKyYRDJjesCiX0xzGzLBaztJyz2Gk1xbZENz4ezr/U/7vp7yuPju23//Y5MBASqwP",
        },
        {
            "url": "https://puzz.link/p?numlin_bit/26/26/zz-15gdx-12nfs-16j8x4v-11zxes9kfs8zg4lbm6k5ubv2r-14n1q-10z5v7zeq3n3r1v-13u9k-11mdl6zgas2k-10sczxav-16x7jcs-15n-13x-14g-12zz",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?numlin_bit/14/9/zh-15h6heh3fe6-15-1354g4ci7g9u2zg3g9g-1351ch2i7g1j8of8n",
            "test": False,
            "config": {"visit_all": True, "no_2x2": False},
        },
    ]
    parameters = {
        "visit_all": {"name": "Visit all cells", "type": "checkbox", "default": True},
        "no_2x2": {"name": "No 2x2 path", "type": "checkbox", "default": True},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        locations: Dict[Union[int, str], List[Tuple[int, int]]] = {}
        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            locations.setdefault(clue, [])
            locations[clue].append((r, c))

        fail_false(len(locations) > 0, "No clues found.")
        for n, pair in locations.items():
            fail_false(len(pair) == 2, f"Element {n} is unmatched.")

        self.add_program_line(grid(puzzle.row, puzzle.col))

        rule, nbit = num_binary_range(len(locations))
        self.add_program_line(rule)

        if puzzle.param["no_2x2"]:
            self.add_program_line(no_2x2_path_bit())

        self.add_program_line(shade_cc(["white"]) if puzzle.param["visit_all"] else shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="white", path=True))

        for _id, (_, pair) in enumerate(locations.items()):
            r0, c0 = pair[0]
            r1, c1 = pair[1]
            self.add_program_line(clue_bit(r0, c0, _id + 1, nbit))
            self.add_program_line(clue_bit(r1, c1, _id + 1, nbit))

        self.add_program_line("white(R, C) :- clue(R, C).")
        self.add_program_line("dead_end(R, C) :- clue(R, C).")
        self.add_program_line(grid_bit_color_connected(adj_type="line", color="white"))
        self.add_program_line(avoid_unknown_src_bit(adj_type="line", color="white"))

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
