"""The Yajilin solver."""

from typing import List

from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.rule.variety import yaji_count
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Puzzle]:
    """Solve the puzzle."""
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(defined(item="gray"))
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
    solver.add_program_line(fill_path(color="white"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
    solver.add_program_line(grid_color_connected(color="white", adj_type="loop"))
    solver.add_program_line(single_loop(color="white"))

    for (r, c, d, pos), clue in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        solver.add_program_line(f"gray({r}, {c}).")

        # empty clue or space or question mark clue (for compatibility)
        if isinstance(clue, str) and (len(clue) == 0 or clue.isspace() or clue == "?"):
            continue

        fail_false(isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows.")
        num, d = clue.split("_")
        fail_false(num.isdigit() and d.isdigit(), f"Invalid arrow or number clue at ({r}, {c}).")
        solver.add_program_line(yaji_count(int(num), (r, c), int(d), color="black"))

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"black({r}, {c}).")

    for (r, c, _, d), draw in puzzle.line.items():
        solver.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

    solver.add_program_line(display(item="black"))
    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Yajilin",
    "category": "loop",
    "aliases": ["yajirin"],
    "examples": [
        {
            "data": "m=edit&p=7VRRb5tADH7Pr6j87AeOu1ByL1PWNXth6bZkqiqEEGFUZUtGR8LUXZT/Xp+PjEwlU6tKnSZN5JyPz/bx2Rxef2+yukDh2Z8Mkf7pUiLk5YcBL6+95uVmWegTHDebm6omgHgxmeB1tlwXg7iNSgZbM9JmjOatjkEAgk9LQILmg96ad9pM0czIBRgSF7kgn+B5By/Zb9GZI4VHeEqYNhMErwjmZZ0vizRyzHsdmzmCfc5rzrYQVtWPAlod9j6vVovSEotsQ8Wsb8rb1rNuPldfmzZWJDs0Yyc32stVnVzZybXQybWoR66t4tlyl+W34q5P6SjZ7ajjH0lrqmMr+1MHww7O9JbsVG9Bejb1Fcmwr4b2GwreK7W6WyqQlpKp7KiQ08QhNfJd1EGi8DjTT+172nNi+JCTba53wCnl4g65gHN/qaUaBFdyxXbC1mc7p0LRSLZv2Hpsh2wjjjlne8n2jK1iG3DMqW3VI5sJKgCtXEufIwqUT50YhdRzETqgFCqqWiJI+hYteqTyWLrv9/dr+O9xySCGWVNfZ3lBZz6is38yrepVtqS7abNaFPX+nqbNbgB3wCuWdnj9H0AvP4Bs970njaG//yHHZoYqQHOBcNukWZpXdLyobX/kT4/w4RP5Y/v0Pjfaz4QjTjcm+p00VfodNHceOF78DdHMgp/Zl5JOFySDew==",
        },
        {
            "url": "https://puzz.link/p?yajilin/19/13/g24g33f45o23d30g32z43k41y11a11a42zo33a14a12b11d31a32c21e11t36g31e21y",
            "test": False,
        },
    ],
}
