"""The Cocktail Lamp solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, avoid_area_adjacent
from noqx.rule.reachable import area_color_connected, grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(avoid_area_adjacent(color="gray"))
    solver.add_program_line(grid_color_connected(color="gray", adj_type=8, grid_size=(puzzle.row, puzzle.col)))
    solver.add_program_line(avoid_rect(2, 2, color="gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.text[rc]

            if data == "?":
                continue

            assert isinstance(data, int), "Clue must be an integer."
            solver.add_program_line(count(data, color="gray", _type="area", _id=i))

    solver.add_program_line(area_color_connected(color="gray", adj_type=4))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Cocktail Lamp",
    "category": "shade",
    "aliases": ["cocktaillamp"],
    "examples": [
        {
            "data": "m=edit&p=7ZfNb9tGEMXv+isCnvdA7ge51M1N7V5c98MugkAQAtlRGqM23MhWUcjw/57fzA5F0TBQFEXbHAJJ3Dck583M7rwldf9pu9qsXRPlG7KrXcMndbX+Ytfqr7bPxfXDzXr+yh1tHz7ebQDO/XBy4j6sbu7Xs4XdtZw97vr57sjtvpsvqqZylefXVEu3+2n+uPt+vjt2u3MuVS5z7rTc5IHHI3yj1wW9LiebGnxmGPgWeHW9ubpZvzstZ36cL3YXrpI436i3wOr27o91ZXmIfXV3e3ktJy5XDxRz//H6d7tyv31/99vW7m2WT253VNI9fyHdMKYrsKQr6IV0pYp/Od1++fTEtP9Mwu/mC8n9lxHmEZ7PHzmezR+rWOMqa60rU8WA6UeznV7tMcPeTNOrqcOkgcxshfnAFOYDU3wPTGGWpitm04hzOrCbye1NE5/Z09iNnwZvovgf8LVper3NU7t7Fq+bxvO18I/5+kbyP7ju/TN7Gs/7aTyvMztOpU8S78DW+Ie21Duuk8+ST2s2S9voAr/V44kevR4vWH+3C3r8Vo+1HpMeT/WeY9oixOSCLJl34BZMAoozmLUTnGowhShuwBSh2LvQkZBitpOOyRDccl4SVQx/Nv4WzmycHTzZeDp8e/PNxOotVg4u1iyQYnam2nLLPZiJEdx7F6WJFGdw4ccPXPjxc1EWSnEHZpEEN+x4skCK4Q+FHz9w4cfPRdGO4gQuteAHtlgB/mT8Af5k/BH+ZPyRWtpSC35gi8UcRptD/MDGn+DvjL+lls5qaYmVLZbs2Nn4O/h745ddvDf+jlp6qyV7l6ShFWew8fc8AWrj76NLjfH3HbjUgh+4xMLPJV/48QMXfvxcCoUfP3CpBT9wiYWfS7Hw4wc2/gB/NP4QXEqlFvzAFivCL7uNYvitb/EDGz/9maw/8eOpZrFaecIZfwt/Nv4W/mz8LbVkq6UjVm+xmMNkc5joz2T9mZjP1uYTDrDFygk89Lzo5UAXg9bIYa811hSdjHoZdEduobU+b7tRg6KjQYPkvNcg/YCuRn0NeqSWYH3FCLa4orvO4lLjoNnI2u11JLqQTVcxvW09wDjqS/QiG7HqQjRlfejp20F3oiM/aIdetf5hHPUo+vIW1xPX+opx1KloJ9p5fWMZel40MuhCNGWxRBdWLyPYYnWiNYulbz0DJ7GsTxhH3YmOhvmhB6L1D+Nej6mmJ01T2udWFyN4OC/asV6S/re6GMHWt55+G3QkugiDFujtYLGCaM36X/RiexcjeNCUaNDiio5sT1Nd2B6VErEGTUnP27wl5mGvF+YBDYxasHlQLQw6Yh7Qw14XyfZ8xlFfaARt7DWS7FnAOOouE9f2NEawxWXP3+uxFw1KXB5ib/RR9lqPUY+tPuI6eQH6W69I//xp+pfpLHjjlof7yx95bfl67T+5tpwtqvPt5sPqas3r9fH7X9evzu42t6sbrLPt7eV6M9j8u3maVX9W+tN34vj1D8//9IdHlqD+0jT9paXDLlOtPm3W1XL2GQ==",
        },
        {
            "url": "https://puzz.link/p?cocktail/17/35/0gf1sfdrdfrvnar28dkkmpab4k3i4jt99ugkvdo7nd5n6irjmdpn6sr36c1jj09tqgctc0ve8tb9b9qapr5as8be6dr575jbcphpc5cidpitt9h41fhj2poh2g2l29f0e70e8041h0t3hpk01u01n1o0hh76003hvc08000gs080e7s0oue607v0o7ha2dd1dte8371ji01o610ao6180ca790dt5fkg42rck531h314h56g28j2g6h4g2k1632g4i0h25h34111",
            "test": False,
        },
    ],
}
