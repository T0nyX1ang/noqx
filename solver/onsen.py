"""The Onsen-Meguri solver."""

from typing import Union

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, count, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs, validate_type
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.route import single_route


def onsen_rule(target: Union[int, str], _id: int, area_id: int, r: int, c: int) -> str:
    """Generates a rule for an Onsen-Meguri puzzle."""
    rule = f"onsen({_id}, {r}, {c}).\n"
    rule += f"onsen({_id}, R, C) :- grid(R, C), adj_line(R, C, R1, C1), onsen({_id}, R1, C1).\n"

    if target != "?":
        num = int(target)
        rule += f":- area(A, R, C), onsen({_id}, R, C), #count {{ R1, C1: area(A, R1, C1), onsen({_id}, R1, C1) }} != {num}."
    else:
        anch = f"#count {{ R1, C1: area({area_id}, R1, C1), onsen({_id}, R1, C1) }} = N"  # set anchor number for clue
        rule += (
            f":- area(A, R, C), onsen({_id}, R, C), {anch}, #count {{ R1, C1: area(A, R1, C1), onsen({_id}, R1, C1) }} != N."
        )

    rule += ":- white(R, C), not onsen(_, R, C).\n"
    return rule


def onsen_global_rule() -> str:
    """Generates global rules for an Onsen-Meguri puzzle."""
    # any area, any onsen area, go through border at most twice
    rule = ":- area(A, _, _), onsen(O, _, _), #count { R, C, D: onsen(O, R, C), area_border(A, R, C, D), line_io(R, C, D) } > 2.\n"

    # two different onsen lines cannot be connected
    rule += ":- onsen(O1, R, C), onsen(O2, R, C), O1 != O2.\n"

    return rule


class OnsenSolver(Solver):
    """The Onsen-Meguri solver."""

    name = "Onsen-Meguri"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VRRb9owEH7nVyA/30McJ46dN9bRvTC6rUxVFUUIaLaiQdNBM1VB/Pd+di5LpFXqpm48TSaXz+fzcd/nc/bfq8WuoARDGQpIYqgg8o8O3K8ds/XDpkiHNKoebssdANHF+Tl9WWz2xSDjqHxwqG1aj6h+l2YiFOQfKXKqP6aH+n1aj6m+xJIgCd8ESAoKAccdvPLrDp01ThkATxusAa8BV+vdalPMJ02iD2lWz0i4/3njdzsotuWPQjTb/HxVbpdr51guHkBmf7u+55V9dVN+qzhW5keqR025k2fKVV25DjblOvSvyt2s74rH5yq1+fEIxT+h1nmaubI/d9B08DI9wE7Tg4gCbMXRNocitJuKIepkh3EOxVPskX7ntbfn3obezpCYauXtW28Db2NvJz5mjP+TKiEZGZGGyBjFJGPNGP649Rtg2+AYPaglY8RojoktyQTFOYyulAnHaHRsEjJGjCPgcIIYwzEJ8hvOnyDGcoxBjOUYEwIrxpbCgGOsBOb8NgTmGBsBxx5jnULJfscxajlq4KTj2+rgOMYtx54mjm+riePrTsfzQh7NeXRPEw1euuXV08HxTdhv4DfsdxxNy1EBR8ylpwM4/tQBHKVtOErbaeL5sg54Azd58GZNcPhXvgXOvI281b41EteRf9Szr+lCoQx0swbFxaQgs2r68sUCsxDcewOn9Ldn+SATE9zs4bTcbRcb3O/xzdfebFptl8WunePLehyIR+Ef3FBJ0f+P7ek/tk794GTt+5vN+kI5GYTl/qf6gsR9NV/MVyV6DNq9bhHX65eFk7PHbRXl3b64E/ngCQ==",
        },
        {"url": "http://pzv.jp/p.html?onsen/10/10/akkh92j6mt9pjvfti91svv1vvovv3g3f04ti3m2n1j1x1zq2v3n3", "test": False},
        {"url": "https://puzz.link/p?onsen/10/10/ebvsrdlpn5bmq7v7kcgj9ac41au4d36hn0bm.n.zzzz.n./", "test": False},
        {
            "url": "https://puzz.link/p?onsen/15/15/9018m2kqm9jbr3a9f853qcfj996k6esa8alac2v892cvv0sj4086g5lb4a6qqeh7q2404c5nvq8cvi30m098zzzzzzj.u..zzzzi",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="white"))

        onsen_id = 0
        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            self.add_program_line(count(("gt", 0), _id=i, color="white", _type="area"))

            for r, c in ar:
                if Point(r, c, Direction.CENTER, "normal") in puzzle.text:
                    num = puzzle.text[Point(r, c, Direction.CENTER, "normal")]
                    self.add_program_line(f"white({r}, {c}).")
                    self.add_program_line(onsen_rule(num if isinstance(num, int) else "?", onsen_id, i, r, c))

                    onsen_id += 1  # fix multiple onsen clues in an area, onsen_id and area_id may be different now

        fail_false(onsen_id > 0, "No onsen clues found.")
        self.add_program_line(onsen_global_rule())

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
