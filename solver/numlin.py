"""The Numberlink solver."""

from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import direction, display, fill_path, grid, shade_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def no_2x2_path() -> str:
    """
    Generate a rule that no 2x2 path is allowed.

    A reachable path rule should be defined first.
    """

    points = ((0, 0), (0, 1), (1, 0), (1, 1))
    tag = tag_encode("reachable", "grid", "src", "adj", "loop", "numlin")
    cells = [f"{tag}(R0, C0, R + {r}, C + {c})" for r, c in points]
    return f":- grid(R, C), grid(R + 1, C + 1), clue(R0, C0), {', '.join(cells)}.\n"


class NumlinSolver(Solver):
    """The Numberlink solver."""

    name = "Numberlink"
    category = "loop"
    aliases = ["numberlink", "arukone", "flowfree"]
    examples = [
        {
            "data": "m=edit&p=7VPBbptAEL3zFdae58Cy2Ia9EcfuhZK2cRVFK4SwSxVUXFJsqmgt/3tmBizcyJVSJfKpWvP09s0svB3PbH+1eVPAFJcKwAWJS7k+PxOXfse1LHdVoUcQtbuHukECcLNYwPe82haO6bNSZ29DbSOwH7QRUoDw8JEiBftZ7+1HbROwtxgSIFGLuyQP6XygdxwnNutE6SJPeo70Hum6bNZVkcWd8kkbuwRB37ni00TFpv5diN4H7df1ZlWSsMp3eJntQ/nYR7btt/pH2+fK9AA26uzGZ+yqwS7Rzi6xM3bpFm+2W5U/i6dzTsP0cMCKf0GvmTZk++tAg4He6j1iovfCm9LRCG10f4tQExKuBsF3SZifCAEJ14Mw4YzZIExZOMkI5It3hJxx8tnQe/GOUP3hA+1KNn3PuGD0GJd4J7CK8ZrRZRwzxpwzZ7xjnDH6jBPOmVJV/qlub7Ej/DHeLQywTiFQIdQrDRrP53k8rvH771LHiBi7a5TUzSavsMeSdrMqmuMe5/ngiCfBj1F4xP8/4pcfcaq+e7GGfZ/5MVjYvuPB3oB4bLM8W9fYY1g7CuJY/C3gvz5w8VvjXKbOMw==",
            "config": {"visit_all": False, "no_2x2": False},
        },
        {
            "data": "m=edit&p=7VRNi9swEL37Vyw662DJX7Ju6XbTi+t+bMqyGLM4qcuatdetE5dFIf89M2MbOSU9lMKSw+Lo8Z5mhJ5Gymx/9UVXchHgz1Pc5QK+0FU0hAINY/pW1a4u9RVf9LvHtgPC+aflkv8o6m3pZGNW7uxNrM2Cmw86Y4JxJmEIlnPzRe/NR21Sbm4hxLiAuWRIkkBvLL2jOLLrYVK4wNORA70Huqm6TV0+JMPMZ52ZFWe4zztajZQ17e+SjT5Qb9pmXeHEutjBYbaP1c8xsu2/t0/9mCvyAzeLwW5yxq5n7SId7CI7YxdP8d926+q5fDnnNM4PB6j4V/D6oDO0/c1SZemt3gOmes8iCUvxmulSmHJBSis9kJ6VPkjfyhgkPJZRCjcAHVrthaAjq32Mz3SIe8PDmnSE8Ximcb3dXdD2s7jCfIGvdJyI1YkBKSjBnk7K0wPIABPscWUk/lhAFuY6Ot1SUsHsGaRCC1NNoMaCKn1PuCSUhCu4CG48wveELmFAmFDODeEd4TWhTxhSToRX+U+X/Qp2Mn9oGn/7sDJv0YuO5k7GEmgwV2nbNUUNbSbtm3XZTRpa+sFhL4wG/T39ty7/+l0eq+9e2t//0uxAQ2LP9HqhmE8sd44=",
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

        all_src = []
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

        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))

        if puzzle.param["visit_all"]:
            self.add_program_line("numlin(R, C) :- grid(R, C).")
        else:
            self.add_program_line(shade_c(color="numlin"))

        self.add_program_line(fill_path(color="numlin"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(single_loop(color="numlin", path=True))

        for n, pair in locations.items():
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
            self.add_program_line(f"numlin({r0}, {c0}).")
            self.add_program_line(f"numlin({r1}, {c1}).")
            self.add_program_line(
                grid_src_color_connected(
                    src_cell=(r0, c0), include_cells=[(r1, c1)], exclude_cells=excluded, adj_type="loop", color="numlin"
                )
            )

        self.add_program_line(avoid_unknown_src(color="numlin", adj_type="loop"))

        if puzzle.param["no_2x2"]:
            self.add_program_line(no_2x2_path())

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
