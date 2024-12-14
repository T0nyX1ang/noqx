"""The Hinge solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, edge, grid, shade_c
from noqx.rule.helper import Direction, full_bfs
from noqx.rule.neighbor import adjacent
from noqx.solution import solver


def symmetry_hinge(color: str = "black") -> str:
    """
    Generate the symmetry rule of Hinge.
    """
    rule = f'symmetry(R, C, "H", R0, C0) :- grid(R, C), {color}(R, C), {color}(R - 1, C), edge_top(R, C), symmetry_axis("H", R, C, R0, C0).\n'
    rule += f'symmetry(R, C, "V", R0, C0) :- grid(R, C), {color}(R, C), {color}(R, C - 1), edge_left(R, C), symmetry_axis("V", R, C, R0, C0).\n'
    rule += f"symmetry(R, C, D, R0, C0) :- grid(R, C), {color}(R, C), adj_4(R, C, R1, C1), symmetry(R1, C1, D, R0, C0).\n"

    rule += f":- grid(R, C), {color}(R, C), symmetry(R, C, D0, R0, C0), symmetry(R, C, D1, R1, C1), (D0, R0, C0) != (D1, R1, C1).\n"
    rule += f":- grid(R, C), {color}(R, C), not symmetry(R, C, _, _, _)."

    rule += ':- symmetry(R, C, "H", R0, C0), not symmetry(R0 * 2 - 1 - R, C, "H", R0, C0).\n'
    rule += ':- symmetry(R, C, "V", R0, C0), not symmetry(R, C0 * 2 - 1 - C, "v", R0, C0).\n'
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent())
    solver.add_program_line(symmetry_hinge(color="gray"))

    # Decode of edge only contain directions TOP and LEFT
    # Horizontal symmetry axis
    for r in range(1, puzzle.row):
        c = 0
        while c < puzzle.col:
            if (r, c, Direction.TOP) in puzzle.edge:
                c0 = c
                while c < puzzle.col and (r, c, Direction.TOP) in puzzle.edge:
                    solver.add_program_line(f"edge_top({r}, {c}).")
                    solver.add_program_line(f'symmetry_axis("H", {r}, {c}, {r}, {c0}).')
                    c += 1
            c += 1
    # Vertical symmetry axis
    for c in range(1, puzzle.col):
        r = 0
        while r < puzzle.row:
            if (r, c, Direction.LEFT) in puzzle.edge:
                r0 = r
                while r < puzzle.row and (r, c, Direction.LEFT) in puzzle.edge:
                    solver.add_program_line(f"edge_left({r}, {c}).")
                    solver.add_program_line(f'symmetry_axis("V", {r}, {c}, {r0}, {c}).')
                    r += 1
            r += 1

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            num = puzzle.text[rc]
            solver.add_program_line(count(num, color="gray", _type="area", _id=i))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))
    print(solver.program)
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Hinge",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7ZNPa9tAEMXv+hRlz3PQruRE2lvqxr24blK7hCBEUFSFiNoo1Z9SVvi7581ojS6BtpTSHMp6Hz/Pzs4+jVbdt6FoK1pgRAmFpDGMSWTGIf9OY1f3+8q+oYuhf2xaANHH1Yoein1XBZnPyoPRpdZdk3tvM6UVKYOpVU7u2o7ug3UbclssKdKIrackA7yc8UbWmZZTUIfgjWfgLbCs23Jf3a2nyJXN3I4Un/NWdjOqQ/O9Ut4H/y+bw33Ngfuix8N0j/WTX+mGL83Xwefq/EjuYrK7fcFuNNtlnOwyvWCXn+Iv203z4xFt/wTDdzZj759nTGbc2hG6saMyhrfG8DK9GxWfc+DsFECaluRb0ZWoEd2hFrlI9J1oKLoQXUvOJY5II7QBxxgUDA048oy49nGNuNETG1y9E+sUHHpOkJ/O+drX0Vwn9nu5jo8zR75OhMsccx14uhFnS9FY9Ewcn3Nvfqt7f96cn9rJuBt+LH6N8iBT26F9KMoKd2TZHJ6aru4rhQ/yGKgfSmaGplH8/xv9R98ov4Lwtd2112YHtz8PngE=",
        },
        {
            "data": "m=edit&p=7VZPaxs/EL37UxSd5yCtpNVqb2ma/C5p2tQpIRgTHNchpglO/aeUNf7ueSONssUESijll0Mwlt5KT09vZlayVz82k+WMjCNTkW1Ik8HHB00uOnJVlb5aPufz9d2sfUcHm/XtYglA9On4mG4md6vZYCSs8WDbxbY7o+6/dqSMIlXha9SYurN2231su1PqhphSZDB2kkkV4FEPL9I8o8M8aDTwqWDAS8DpfDm9m12d5JHP7ag7J8X7vE+rGar7xc+ZEh/8PF3cX8954HqyRjCr2/mDzKw23xbfN8I14x11B9nu8Bm7trfLMNtl9IxdjuIf243j3Q5p/wLDV+2IvX/tYdPDYbtFe9pulW14qbMwk4ujQhpBrcpAo3mg7geMNnsUY+w+x7p9jq33OXXY59RxnxPT7k8c2DbJ/GVqj1NbpfYcsVFnU/shtTq1PrUniXPEIeuGbAUzFSn0ZB2sMnYO2Av2wIUDfsFGYy0ylHAga4VvwfdIAmNvgUXTQ9MXDvgFm4i1CB/YQ8eLjouR8NxjjfCZozUw0p6wB85+0JOv8l6uCeSa7A09MJLJ2OP0ijfnDXAl2JILWRN9zw/gB+EH5og+YsFcxraGjowb7MXFZQyfeM4xNtAR/4xtI/lpkJ9G8tMgP03JOfJTC66Rz8LncSeajmuRfaJHPkXfoy4+x4IeOPtMHH7NkiZ0yl6NhzeJUSPGSvJQIQ9W8sAxSo3QA0tucT/2nEjOZQ/ogUWHNbXkRyNvWuqL2jmpHXpg0dfQ1xIj6mWDxIUb2EpN0f+2FjqV+K+wV9nXcX1L3eEtiH6AfhQP7N+LjoeHUt8An1HqG1G7KPoR+lE4/GtQdFi/lthrxF6LhxoeatHBmXrCOGt4Fv/wUM5gxNoSO949PAtGHeV9S3ko7yrrh/KuwkMs5wX6Txj5iayPQ3+Rjv5hal1q63QlBL4MX3Rd/v3t80c7I1SHf3uf//i3uZfOjQcjNdwsbybTGX4yDxf3D4vVfD1T+H+yG6hfKn1HFlT39pflf/rLwiXQr+0kvjY7uBvGg0c=",
        },
    ],
}
