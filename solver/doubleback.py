"""The Double back solver."""

from typing import List

from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import full_bfs
from noqx.rule.loop import count_area_pass, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="black"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("doubleback(R, C) :- grid(R, C), not black(R, C).")
    solver.add_program_line(fill_path(color="doubleback"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="doubleback", adj_type="loop"))
    solver.add_program_line(single_loop(color="doubleback"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")

            # enforce the black cells to have edges on all sides
            puzzle.edge[Point(r, c, Direction.TOP)] = True
            puzzle.edge[Point(r, c, Direction.LEFT)] = True
            puzzle.edge[Point(r + 1, c, Direction.TOP)] = True
            puzzle.edge[Point(r, c + 1, Direction.LEFT)] = True

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for ar in areas:
        arb = tuple(filter(lambda x: puzzle.surface.get(Point(*x)) is None or puzzle.surface[Point(*x)] not in Color.DARK, ar))
        if len(arb) == 0:
            continue  # drop black cells

        solver.add_program_line(count_area_pass(2, arb))

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Double Back",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7VVbaxs9EH33rwh61sPqttrdtzRN+uKmF6eEsJhgO5vGxKlbOy5hjf97zoxGcQuBFvrxkUKxVzqelecczdFl/W0zWXXaFPR1lUaPjzcVP7Yq+Snkcza/X3TNgT7c3N8sVwBavzs50deTxbobtDJqPNj2ddMf6v5N0yqrND9GjXX/odn2b5t+pPsRXintERsCGaUt4PEenvN7QkcpaArgU8GAF4Cz+Wq26C6HKfK+afszrYjnFf+boLpbfu9U+hv/ni3vpnMKTCf3mMz6Zv5V3qw3V8vbjYw1453uD5Pc4TNy3V4uwSSX0DNyaRZ/LHcx/9I9PKe0Hu92qPhHaL1sWpL9aQ+rPRw1W+UK1XitnEtdmbqau2hTF1JXcVcZ7ozx0sfU25TI2JTJhJTKhJTLlCmZKSkbyE+bLVrD7QW3J9xabs+gUPeO29fcFtwGboc85hjyrbHaWlBZrCnjgaGScQAGNeOorYNsxljCDlII2wIY02CMuJe4M8CQSdgjP02FMXLSdAgHcJXCFbAlIqbPGFxRuEINjHIQLsEVhatEzig5I7gq4YrIWUnOCly1cFVRu0JyVhWw6KxL7Yzw1hhjZEyNMSaPqYGTBuQATlzIAZw0uMIDJ17k0M7KGNTWSW2RAxhWMw7ASRti2vnEixiwcOHgcCFpcB7nSEhzx1hgye+RM0hODw1BNHjMq5R5WfJRakUeZU/Jo+yjQ92c1DA4eCR1Jo+EC/3eR/JLeNkv4UX/g7/wLmsgv8rsI8Zn3yN5KjUnH2m/MCZ/ZXyEnux7pHUivORvJXr4SJV4Tb5LHP7C1yd/4euTv3ltsKeyHtjTInuN2hZSc/K3yL7TekjzYn/z2iBP83rAHnEm+0teS9zBa5c9gqfZd/LRZ3/hnSfN2KDnvE2PuPXclrx9Ix0/v3lA/VcnxS/ltC5ddD9/wt8XGw9aNdqsriezDpfDEJfEwelydTdZ4Nfx1eenX7iUdwP1oPhpHd3x/+7p//+epuoXL20zvDQ52J7qarmZLrqD6WR2q8aDRw==",
        },
        {
            "url": "https://puzz.link/p?doubleback/23/9/051602u9ghhls666vh35bk1stt667e518hg0i48006800uuvnhvpge766m1oso0f3g3guvuu8e040000040000000000000000000000000000000000000",
            "test": False,
        },
    ],
}
