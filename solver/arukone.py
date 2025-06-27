"""The Arukone solver."""

from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


class ArukoneSolver(Solver):
    """The Arukone solver."""

    name = "Arukone"
    category = "loop"
    examples = [
        {
            "data": "m=edit&p=7ZhrT+PGF8bf8ylWfrtT1XNxbEfqi3BdthBgAVESRZEJBsI6mDoJUCO++545BsWXx1T/7eVfqVWUyfg3nnmO5ziPZzz/dRllsQiFNEIHQvmu+EEKKTxf07Gm34C/7uvnZLpI4u4H0VsubtKMKkIc9MVVlMxj8fn8Zm8j7T1u9n55CBaDgdxxl7vu2e327ccvs593pzqT2/3gcP9wf6que5821o86Wx87h8v56SJ+OJrJ9dvTwcnV4dl1qH7b6g9MPjhwvc+Dqx8feqc/rQ1fQxitPedhN++JfKc7dLQjHEVf6YxEftR9zve7eV/kx9TkCDMSzmyZLKaTNEkzh5mk8/aoJh2hqLq1qp5xu61tUI0GlS7V+/YEt+h3TvViwsbHBTnsDnNPOFZ8nbvbqjNLH2KrRgPz8SSdXUwtSKZ38dMrnC8v06/L19Pk6EXkvSL8vbfwSeC98PUqfFstwre1RvjFVdnoJ9NsksTjvT83+nD08kJZ+ULxj7tDeymnq2qwqh53n6nsd58dbWxXGwalzrUDGt+SzRLxOpasl0hHWrJdIr6u9wq411aJhKz1qUy8unoYWmKT+kak61p0WkGBRb0yop9akFKqRkfFgZeDkopjKF+L1NyxHKgs5qkSl+aJ2q0gjqtfRoaHPygjj4OoIr7sygV1+IIqw3d4kncqiOPaKKOAFStnFbkon6VcHmsVKt0Pku+Kc7orVMfOgKK7q/wnI2w7AWyDANgGArANBmA7nQDbKQXYTlgT+1jSx5I+lvSxpI8lA5sngG2SAcYTG2DJAEuGWDLEkiGWDHEu+U8KMJxY7UJJ7UJJzfccwFBSuy2SMJfahbnU7BRNLLGkxJISS0osKVskYS61grnUbFQAY0mFJRWW1FhSY0k2Q4BxLtknm9hgSYMlDZY0WNK0SOJcGpxLfuo1sYclPSzpYUl+fgLcIolzyU+IJuanBMBYEnusxh6rscdqH0v6OJc+ziWvFwDGkthjNfZYjT2WFtEY41zyUxRgPLHYYzX2WI09Vrd4bNgiiXMZ4lzyuqqBDfZYgz3WYI812GONiyV5oQYwzKXhNRzAWBJ7rMEea7DHGoUlFcylUTCXhleVNUyLq21eYikuT2gtLnLN5SaXLpcel3t8zhaXZ1xucGm47PA5vl3N/0/r/fIq7y8KZ6gCWlNWP96/hYzWaDtDu7MP/TSbRQnt0frL2UWcrY6Pb6L72KG9szNPk/F8mV1Fk3gcP0WThdMttu/llgq747EqKEnTe7sdBCO8NVXg9PouzWLYZGF8ed02lG0CQ12k2WUtpscoSarXwn+CCir2vxW0yGhzWzqOsix9rJBZtLipgItoQW9B5jfT++pI8V1tMhdRNcToa1RTm62m42XNeXL4O9RC2aT+96Ljn/iiw2bI/W77oy0weXR+8P9x5SFNOkVghI1C5AfCuV+OozHNu0Nv1gQ3y1C91/zHesuQ7IqWLe80k0C7Nv0zvrv5dwZvDe3vfpQVHp1m79j0qrGOgVkTfcevS62It1hzqbXOGz5sg21aMVHgxkTrhkyo6ckEG7ZMrMWZ7ah1c7ZR1f3ZSjUs2kqVXXo4WvsG",
        }
    ]

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
        self.add_program_line(direction("lurd"))

        self.add_program_line("arukone(R, C) :- grid(R, C).")
        self.add_program_line(fill_path(color="arukone"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(single_loop(color="arukone", path=True))

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
            self.add_program_line(f"arukone({r0}, {c0}).")
            self.add_program_line(f"arukone({r1}, {c1}).")
            self.add_program_line(
                grid_src_color_connected(
                    src_cell=(r0, c0), include_cells=[(r1, c1)], exclude_cells=excluded, adj_type="loop", color="arukone"
                )
            )

        self.add_program_line(avoid_unknown_src(adj_type="loop", color="arukone"))

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
