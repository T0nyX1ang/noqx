"""The Fivecells solver."""

from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape
from noqx.solution import solver


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    fail_false(puzzle.row * puzzle.col % 5 == 0, "It's impossible to divide grid into regions of this size!")
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))

    for i, o_shape in enumerate(OMINOES[5].values()):
        solver.add_program_line(general_shape("omino_5", i, o_shape, color="grid", adj_type="edge"))

    solver.add_program_line(all_shapes("omino_5", color="grid"))
    solver.add_program_line(count_shape(target=puzzle.row * puzzle.col // 5, name="omino_5", color="grid"))

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        if isinstance(num, int):
            solver.add_program_line(count_adjacent_edges(num, (r, c)))

    for (r, c, d, _), draw in puzzle.edge.items():
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))

    return solver.program


__metadata__ = {
    "name": "FiveCells",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7Vbfb9pIEH7nr4j2eR88uzb2+uWUpuRecqR3SRVFFkKEuA0qyCmEqjLif8/M2IRlzKo6RY36EIFHn+fXfjuzHnv1fT1ZlhoS+ttMRxrw148yviDDe7x2v+vZ07zMT/Tp+umhWiLQ+vL8XH+ZzFdlr2i9Rr1N7fL6VNd/54UySvMFaqTrf/NN/U9eD3V9hSalAXUXiEBpg3CwhzdsJ3TWKCFCPGwxwluE09lyOi/HF43mU17U11rROh84mqBaVD9K1YTx/bRa3M1IcTd5ws2sHmaPrWW1vq++rVtfGG11fdrQHRyha/d0CTZ0Cf02uvPH6hhRN9puseD/IdVxXhDrz3uY7eFVvkE5zDeqH+322HRF9YEU2KQXhZEKSwrrKWJSRJ4ikR59uUoqPTLp4YRHykw9HqlkmkqmKefwFI5DvKSOl/U8AGRBACRXMJzX97FygxB38sS8+IGGCfuZY66tzyfm4h5omLMflch6QyKrB52uQdMDn0/Ka/k+aac+Ge/rL1/Du/DaDxlXw8/jOqs7WVUTyeaYiPflrW5AVsyArLxp+nUQJQ+XAXkyjJHHyxhZDWM7DJt+eXs3CefxNc0D5Ed1zrbJ5Fk2meyyyTqcXYdzc8D9nTr5UJhOL4yTD7Bx8kQZ16lzt4PN03TgI3dqo0POOIaAh9Ety3OWhuU1zipdW5YfWUYsE5YX7DNgecPyjGXMss8+KU27/zUPX09HpfRcuQynDz0GBLIMq0nARVhoBnFrcgk2gwHNTAY0xRhQfQlARGecEeziEO2shsZvi9ocYM0e7SKsbRMjahcFm75Y0zZfHKU6piD7y8IWcfOBEPrhZ8S79c+2jnqFGtx/LU+G1XIxmeM3xXC9uCuXu3v8fNv21E/FV2ExJH7/onvzLzoqfvTGc+y1Y7XAuuIo1PWlVo/r8WQ8rfB4YdnIQIMsaAnE4Dg9bsDxGsiFo/G4BQdxMCSQDEd2IASHbSAklIumciDEhSqGozpgwddDMCaQDV87oRBrAiFpwECvk+OWl3dJx/zmZxVfVqPeMw==",
        },
        {
            "url": "https://puzz.link/p?fivecells/10/10/a32213a32a1h22c31a3b3a3d3a23a2b2a2a23a1a1b2a22a2d2a3b3a31c11h3a22a21321a",
            "test": False,
        },
    ],
}
