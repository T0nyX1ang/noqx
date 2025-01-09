"""The N Cells solver."""

from typing import List

from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    assert puzzle.row * puzzle.col % 5 == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.register_puzzle(puzzle)
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
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(count_adjacent_edges(num, (r, c)))

    for (r, c, d, _), draw in puzzle.edge.items():
        assert d is not None, f"Direction in ({r}, {c}) is not defined."
        solver.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "FiveCells",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VbPb9pKEL7zV0R73oNn18Ze39I80kseaZtUUWQhRIhfgwpyCqGqjPjfMzM2YRmzqqqo0TtE4NHn+bXfzqzHXv1YT5alhoT+NtORBvz1o4wvyPAer93vevY0L/MTfbp+eqiWCLS+PD/X/03mq7JXtF6j3qZ2eX2q6495oYzSfIEa6fpzvqn/zeuhrq/QpDSg7gIRKG0QDvbwhu2EzholRIiHLUZ4i3A6W07n5fii0XzKi/paK1rnA0cTVIvqZ6maML6fVou7GSnuJk+4mdXD7LG1rNb31fd16wujra5PG7qDI3Ttni7Bhi6hv0Z3/lgdI+pG2y0W/AtSHecFsf66h9keXuUblMN8o/rRbo9NV1QfSIFNelEYqbCksJ4iJkXkKRLp0ZerpNIjkx5OeKTM1OORSqapZJpyDk/hOMRL6nhZzwNAFgRAcgXDeX0fKzcIcSdPzIsfaJiwnznm2vp8Yi7ugYY5+1GJrDcksnrQ6Ro0PfD5pLyW75N26pMxZ6/ZkPHe/SjXWcvJGppItsJEvAtvLQOyPgZknU3TnYMoeZQMyHNgjDxMxsi9G9th2HTH27tJOI+vaR4XP6pzkk0mT67JZE9N1uHsOpyb4+zv1MlHwHR6YZx8XI2T58e4Tp27HWyenQMfuVMbHXLGoQM8em5ZnrM0LK9xMunasvyHZcQyYXnBPgOWNyzPWMYs++yT0mz7o+n3ejoqpafIZThr6DEgkGVYTQIuwkIziFuTS7AZDGhCMqCZxYDqSwAiOuOMYBeHaGc1NGxb1OYAa/ZoF2FtmxhRuyjY9MWatvniKNUxBdnfFraIm8+B0A8/Gt6t/2/rqFeowf238mRYLReTOX5BDNeLu3K5u8ePtW1P/VJ8FRZD4vfvtzf/fqPiR288x147VgusK45CXV9q9bgeT8bTCo8Xlo0MNMiClkAMjtPjBhyvgVw4Go9bcBAHQwLJcGQHQnDYBkJCuWgqB0JcqGI4qgMWfD0EYwLZ8LUTCrEmEJIGDPQ6OW55eZd0zG9+VvFlNeo9Aw==",
        },
    ],
}
