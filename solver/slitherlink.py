"""The Slitherlink solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import direction, display, fill_path, grid, shade_c
from noqx.rule.loop import separate_item_from_loop, single_loop
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def convert_direction_to_edge() -> str:
    """Convert grid direction fact to edge fact."""
    rule = 'edge_top(R, C) :- grid_direction(R, C, "r").\n'
    rule += 'edge_left(R, C) :- grid_direction(R, C, "d").\n'
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="slither"))
    solver.add_program_line(fill_path(color="slither"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="slither", adj_type="loop"))
    solver.add_program_line(single_loop(color="slither"))
    solver.add_program_line(convert_direction_to_edge())
    solver.add_program_line(adjacent(_type="edge"))

    flag = False
    for (r, c), clue in puzzle.text.items():
        if clue == "W":
            flag = True
            solver.add_program_line(f"wolf({r}, {c}).")
        elif clue == "S":
            flag = True
            solver.add_program_line(f"sheep({r}, {c}).")
        else:
            assert isinstance(clue, int), "Clue should be an integer or wolf/sheep."
            solver.add_program_line(count_adjacent_edges(int(clue), (r, c)))

    if flag:
        solver.add_program_line(separate_item_from_loop(inside_item="sheep", outside_item="wolf"))

    solver.add_program_line(display(item="edge_top", size=2))
    solver.add_program_line(display(item="edge_left", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Slitherlink",
    "category": "loop",
    "aliases": ["slither"],
    "examples": [
        {
            "data": "m=edit&p=7VTLbtswELzrKwKeedCDevHmpnIvrvqIiyAQhEB22FqIVLWSFQQ0/O/ZXcmgCfhStAhyKGgOZrmz1PBhDr/Hqlc8hiZC7nIPWhC51Kffqa3rfaPkFV+M+13XA+H803LJv1fNoJxiVpXOQadSL7j+IAsWMM486D4ruf4iD/qj1DnXN5Bi3IOxFTAQ+EAzQ28pj+x6GvRc4PnMgd4B3db9tlH3q2nksyz0mjP8zjuqRsra7kmxqYzibdduahzYVHtYzLCrf82ZYXzoHsdZ65VHrheT3eyC3cDYRTrZRXbBLq7ir+2qhx/q+ZLTtDweYce/gtd7WaDtb4Ymht7IA2AuD8wPoTSAQ4ZymM1PIcQzn8IAs74JIwjxTsxhbGftWuFaYuFZYoG1Rhza2QinMq7iwA4xa8QJfshMleBURpxg7VlW2KG9/BRrTTY9Xz5smEfbdke4JPQJ17CrXAeE7wldwpBwRZqM8JbwmlAQRqSJ8Vz+6ORewU7hC/r/n1r476PSKVgGt/kq7/q2auBO52O7Uf0phvfj6LBnRp0OSvx/Ul7/ScHdd9/a9XxrduAPw4am3u9U39Q/H1npvAA=",
        },
        {
            "data": "m=edit&p=7VZRT9swEH7vr0B+9oPtJG2SN8bKXlg3BhNCUYXSEqAirZmbDJSq/53zJR32pbCHadOkTWlOly93n8/nfHbX3+rcFDyBK4y44BKuMBJ4x6H9ie46X1RlkR7ww7q60wYczj8dH/ObvFwXg6yLmg42TZI2p7z5kGYsYJxJuBWb8uY03TQf02bCmzN4xbgE7AQ8CAjAHbeuAvcC31vwqI0U4E7a9zbrEtz5wszL4uqkzficZs05Z3aYd5hiXbbU3wvWpuHzXC9nCwvM8grmsr5bPHRv1vW1vq+7WDnd8uawrXb8drXWfataW9svV1tc3xZP+wpNptst9PsLlHqVZrbqry/uWboBO0k3TMU2HtZC2tUAEpXsZtoBgbTAGePxDggoENGUIQFC5FAOoCxwYRuyQ5DVzRlRAEv1crBWp/iIVhJhJW4EsrokEdI6tUXI6oYMBQkZ0vkMkdbpybBHMqIkI+yBC2ALvBycj0MbY44zwTikEXTGCV2uBEndYRK6Xgn2xAV605GCfhdS0BWTgn5dUvSJJDZGOEESqf0g2iwpcV4egtwuopDaI1J06aSiH41U2A8/rTe3oFdRKwwPoesnA/qhyIAKToZ+Q0CpEvV6ifYYrUJ7DnLmTYD2PVqBNkJ7gjFjtBdoj9CGaIcYM0Ib77aG17eMHyHO7vHbK9sOMhXjseNe0d+FTAcZG8M2fDDRZpmXsBlP6uWsMLtnOPbYWpdX69rc5HPYxvFUhO0asBVGelCp9UO5WPlxi9uVNsXeVxa0pwBLK1N74TNtrgn5Y16WHtAe8R7UnkceVBk4bJzn3Bj96CHLvLrzAOcY9ZiKVeUXUOV+ifl9TkZbvkx5O2BPDO9McRXByfr/P8Uf/k9hmy9+/s/in961WsFrs1fzAO+RPaB75d3hrcJ9vCdmO2Bfz4DukTSgVNUA9YUNYE/bgL0ib8tKFW6roiK3Q/V0bodypZ5NB88=",
        },
        {
            "url": "http://pzv.jp/p.html?slither/25/15/i5di5di6bg3ad13dc13bd3cg5bi7ci7dhai6bi6ci7b02bd33cc23d8ci8ai6cibh6di6bi7dg1ca31ab10dc3dg6bi6ai6chai7ci7ci8d33dc33cc20d8bi7di7cidh8di5ci6cg3dd03cb02ad3dg6bi7ci6bg",
            "test": False,
        },
    ],
}
