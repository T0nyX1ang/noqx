"""The Numberlink solver."""

from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected
from noqx.rule.route import single_route


def no_2x2_path() -> str:
    """Generate a rule that no 2x2 path is allowed."""

    points = ((0, 0), (0, 1), (1, 0), (1, 1))
    tag = tag_encode("reachable", "grid", "src", "adj", "line", "white")
    cells = [f"{tag}(R0, C0, R + {r}, C + {c})" for r, c in points]
    return f":- grid(R, C), grid(R + 1, C + 1), clue(R0, C0), {', '.join(cells)}.\n"


class NumlinSolver(Solver):
    """The Numberlink solver."""

    name = "Numberlink"
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
            "url": "https://puzz.link/p?numlin/26/26/zz-15gdx-12nfs-16j8x4v-11zxes9kfs8zg4lbm6k5ubv2r-14n1q-10z5v7zeq3n3r1v-13u9k-11mdl6zgas2k-10sczxav-16x7jcs-15n-13x-14g-12zz",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?arukone/14/9/zh-15h6heh3fe6-15-1354g4ci7g9u2zg3g9g-1351ch2i7g1j8of8n",
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
        self.add_program_line(grid(puzzle.row, puzzle.col))

        if puzzle.param["visit_all"]:
            self.add_program_line("white(R, C) :- grid(R, C).")
        else:
            self.add_program_line(shade_c(color="white"))

        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="white", path=True))

        all_src: List[Tuple[int, int]] = []
        locations: Dict[Union[int, str], List[Tuple[int, int]]] = {}
        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            locations.setdefault(clue, [])
            locations[clue].append((r, c))
            all_src.append((r, c))

        fail_false(len(locations) > 0, "No clues found.")
        for n, pair in locations.items():
            fail_false(len(pair) == 2, f"Element {n} is unmatched.")
            r0, c0 = pair[0]
            r1, c1 = pair[1]

            excluded = []
            for n1, pair1 in locations.items():
                if n1 != n:
                    excluded.append(pair1[0])
                    excluded.append(pair1[1])

            self.add_program_line(f"clue({r0}, {c0}).")
            self.add_program_line(f"dead_end({r0}, {c0}).")
            self.add_program_line(f"dead_end({r1}, {c1}).")
            self.add_program_line(f"white({r0}, {c0}).")
            self.add_program_line(f"white({r1}, {c1}).")
            self.add_program_line(
                grid_src_color_connected(
                    src_cell=(r0, c0), include_cells=[(r1, c1)], exclude_cells=excluded, adj_type="line", color="white"
                )
            )

        self.add_program_line(avoid_unknown_src(color="white", adj_type="line"))

        if puzzle.param["no_2x2"]:
            self.add_program_line(no_2x2_path())

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
