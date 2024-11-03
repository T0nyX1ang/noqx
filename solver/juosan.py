"""The Juosan solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.solution import solver


def jousan_constraint():
    """Constrain consecutive lines."""
    # black for horizontal, not black for vertical
    rule = ":- grid(R, C), grid(R + 2, C), black(R, C), black(R + 1, C), black(R + 2, C).\n"
    rule += ":- grid(R, C), grid(R, C + 2), not black(R, C), not black(R, C + 1), not black(R, C + 2).\n"
    rule += 'content(R, C, "——") :- grid(R, C), black(R, C).\n'
    rule += 'content(R, C, "|") :- grid(R, C), not black(R, C).'
    return rule


def count_lines(area_id: int, num1: int, num2: int = 0):
    """Limit the number of horizontal or vertical lines."""
    rule = f"count_area({area_id}, N) :- #count{{ R, C: area({area_id}, R, C), black(R, C) }} = N.\n"
    rule += f":- not count_area({area_id}, {num1}), not count_area({area_id}, {num2})."
    return rule


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c())
    solver.add_program_line(jousan_constraint())

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.sudoku)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.sudoku[rc][0]
            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count_lines(i, data, len(ar) - data))

    solver.add_program_line(display(item="content", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Juosan",
    "category": "draw",
    "examples": [
        {
            "data": "m=edit&p=7VbdbyM1HHzPX3Hysx/WH2t7960cLS8lfFzR6RRFp7QXuEJLIGkQ2qr/+83v53G2ICEkEOKQUBLvrD1rjz1jZw8/Hzf7rXWdfEOxuOITXdGfL0l/HT9Xtw932/GFPTs+vN/tAaz94uLCfru5O2wXK7LWi8dpGKczO302row3Vn/OrO301fg4fT5OSzu9QpOxDnWXQM5YD3g+w9faLuhlrXQd8BI41MfeAN7c7m/utm8va82X42q6skbG+USfFmjud79sTe1C729299e3UnG9ecBkDu9vf2LL4fhu98ORXLd+stPZH8sNs1yBVa6g38vlfP5hucP66QnL/jUEvx1Xov2bGZYZvhofUS61dOOjGbqIHoIIMoPzwLBfsO/m+iD1njgBx4qTPFsUu85JQ33YdV5aKst1+kjmTZSWRovlGa2fR3HOS0sd3jkdp7UMswDno6hMvMnPFHil8SboJNlB0FnymaCDsreQpLd2U55NIerk2EHUybWb09pgQd/osl5o6bW8wqrbKWj5qZadlr2Wl8o5hw3eBet9NqPHZnE98ECcrQ+OGPtRhlM8AIeKPfaoLITg0AFDn2IH3BN7YExCMcaKHCuC35Mfwe/Jj+D0jROB4YdijCXLpBjaErVFaEvU1oOfyO8xl8S59OBn8nvwc+NjLplzSdCTqSdBT6aeBP3ir2I5l/hsRn1hfYbmQs0ZGgo1ZGgo1JChf6D+Av5AfgF/IL9kGzrqLAWYY5UBmDoHHJaSKmC02yABURyAa59oB659Buds8HUuAV4Heg2uDfQXXOA6FrjAVTPabaCPqLOhrxoC/Ar0K8CvQL/ABeZ8JRstVx7rL/tKMdawZcxLllp+gFuWJA+Rc4+SH85d8tByJXk4ZQn9y45ueYjNd+CmJ0lmyEniO8fK4jvXXLxrvotfuXkkXlODeCc7tHlXyC/iNfMwAMsxoFh8Zz8D9AzUM4inVQOuJ99xPfmuPnZc5w58R778YbrmHfhysCiWPNAj8doxJ07y0DIAj1pmvOSBHA9Oy4lkwDdOmjMDHwN9xBWYOYGPgT7iOudK8tNyhXMg8NzQLNFrXIHJl1zRd1yBW96gk2cLrswkDrDXeoy91DJqmfR4y/KX8xf+lP7OSfqnclZYGXnD+e2n/+/VrRcrc/7uu+2L5W5/v7nDS8HyeH+93bd7vIU9LcyvRn/yV2rj/y9m/9KLmVjQfWw74WOTg71pvj/uDpsfzXrxAQ==",
        },
        {
            "url": "https://puzz.link/p?juosan/21/12/4ql08qtg9qt59ul5bunltnn9tntd72ta72h636h5b641bm04vmcvjo0fu1vo3s6fhuv1u0gf7fvpjo0fvjro0fs3vu0tvvgg33g42554342h553444g2g24211g121g2221341225h121g252442224465g25g1g2425g273",
            "test": False,
        },
    ],
}
