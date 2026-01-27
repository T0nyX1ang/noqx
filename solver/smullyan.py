"""The Smullyanic Dynasty solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected


class SmullyanicDynastySolver(Solver):
    """The Smullyanic Dynasty solver."""

    name = "Smullyanic Dynasty"
    category = "shade"
    aliases = ["smullyanicdynasty"]
    examples = [
        {
            "data": "m=edit&p=7ZZfb9s2EMDf/SkKvpbARFJ/bAHD4KRx1y5xnDpBFguCoThKrFSKMllyOhn+7j2e4pmklKAbsG4PhS3i/DvyeH+sI1d/VFERUybkV/SpRRl8HMHxYbaNj/X8OU/KNPbf0GFVLvMCBEpPRyN6G6WrmH68Wh4f5sOnd8Pf1/1yNmPvreqDdXk/un/7KfvtQyIKNhr3JyeTk4TfDX89PDhzj966k2p1Ucbrs4wd3F/Mzm8nl3cD/ufReGbXs1PL+Ti7/Wk9vPi5Fzz7EPY29cCvh7R+7weEEUo4PIyEtD7zN/WJX49pPQUVoXZISValZbLI07wgyBjMO24WchCP9uIl6qV02EBmgTx+lkG8AnGRFIs0nh83ZOIH9Tklcu8DXC1FkuXrWG4mfZO/F3l2nUhwHZWQvtUyeSRUgGJV3eSfq+epLNzSethEMN1FAN68FgEY2UUgxSYCKXVEIAP7dyMYhNstFOcTxDD3AxnOxV7s78Wpv4Fx7G+IcOVSAa40FSS2JQEU9C8gJLAUYC5xbAmcPXAR2HvgsV2KdwCNKjY8xwS4i7rEM2b0ESiODUzHmDUwjDCG4alzGPqmEdM5xtCyshXjuEpJE+PcCJpxTMMvKkE72hwzKiZaHgqzAszG3TXS8tk2i8BsM8fMxt3V/Dg4R43L6Zur3FbGXIxd9cfFSFU7Lu6lEg9XaaS1e6vqzEN/1Lg8rLI6Z2DWgltmvXir7py1VrX+CZyZOeTM/Bvypu6qHYFEXWWbsfOmOhrBSFXi6KvgHWb4Jl/hOMKR43gOLzqtBY7vcLRwdHA8xjlHOF7ieIijjaOLczzZKr6xmWAb6VMiIBccGgKkjTcN5ju4GAgXT8yuj/ND8080YS8g06q4jRYxnD/jKruOizfjvMiilMDpT1Z5Ol81+nn8JVqUxG8uIKpGYw9oQ0Npnj+myUOXhZ1Kg8ndQ17EnSoJ45u7l0xJVYep67y4MXx6itJUjwUvZxpqjm8NlQWczcrvqCjyJ41kUbnUgHKOa5biByOZZaS7GH2OjN2yfTq2PfKF4BMICpfHH1e1//VVTRbK+lsXtv++5QeQcOi49Sklj9U8mkOyMV+dHMLu5PBnQ+4Z3Gm4I7rtw5XqWxUi/O55w5cxL17pjHuliTv6I9BXWqSi7eIvdENFa/JW65POtrsf0I4GCNTsgYDabRBgqxMCe6EZSqtmP5RemS1RbtXqinIrtTEGYe8r",
        },
        {
            "url": "https://pzplus.tck.mn/p.html?smullyan/14/14/0222212212111121323232333112233322333233221313333133232221312213133231233323243222321332331223213222222334322231222023222332212310123433332123313333231311223234343331322323233331323202121222122221",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(avoid_same_color_adjacent(color="gray", adj_type=4))
        self.add_program_line(grid_color_connected(color="not gray", adj_type=4))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if isinstance(num, int):
                self.add_program_line(
                    count_adjacent(num, (r, c), color="gray", adj_type=8).replace(":-", f":- not gray({r}, {c}),")
                )
                self.add_program_line(
                    count_adjacent(("ne", num - 1), (r, c), color="gray", adj_type=8).replace(":-", f":- gray({r}, {c}),")
                )

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
