"""The Castle castle solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import direction, display, fill_path, grid, shade_c
from noqx.rule.loop import separate_item_from_loop, single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def wall_length(r: int, c: int, d: int, num: int) -> str:
    """
    Constrain the castle length.

    A grid direction fact should be defined first.
    """
    if d == 0:
        return f':- #count{{ R: grid_direction(R, {c}, "d"), R < {r} }} != {num}.'
    if d == 1:
        return f':- #count{{ C: grid_direction({r}, C, "r"), C < {c} }} != {num}.'
    if d == 2:
        return f':- #count{{ C: grid_direction({r}, C, "r"), C > {c} }} != {num}.'
    if d == 3:
        return f':- #count{{ R: grid_direction(R, {c}, "d"), R > {r} }} != {num}.'

    raise AssertionError("Invalid direction.")


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="castle"))
    solver.add_program_line(fill_path(color="castle"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="castle", adj_type="loop"))
    solver.add_program_line(single_loop(color="castle"))
    solver.add_program_line(separate_item_from_loop(inside_item="white", outside_item="black"))

    for (r, c), color_code in puzzle.surface.items():
        solver.add_program_line(f"not castle({r}, {c}).")
        if color_code == 4:
            solver.add_program_line(f"black({r}, {c}).")
        if color_code in [1, 3, 8]:  # shaded color (DG, GR, LG)
            solver.add_program_line(f"gray({r}, {c}).")

    for (r, c), clue in puzzle.text.items():
        if (r, c) not in puzzle.surface:
            solver.add_program_line(f"white({r}, {c}).")
            solver.add_program_line(f"not castle({r}, {c}).")

        if isinstance(clue, str) and (len(clue) == 0 or clue.isspace()):  # empty clue for compatibility # pragma: no cover
            continue

        assert isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows."
        num, d = clue.split("_")
        assert num.isdigit() and d.isdigit(), "Invalid arrow or number clue."
        solver.add_program_line(wall_length(r, c, int(d), int(num)))

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Castle Wall",
    "category": "loop",
    "aliases": ["castlewall"],
    "examples": [
        {
            "data": "m=edit&p=7VZNb+M2EL37VwQ88yB+6euWbpNeXPcjKYJAMAzH1WKN2nVrx+1Chv/7vhkOJcXNoWiAIoeFberpcTjzZoaSefjzuNy32jj6ulJn2uATnOWf8Z5/mXzu18+btr7S18fnT7s9gNY/3N7qj8vNoZ00YjWfnLqq7q51913dKKO0svgZNdfdT/Wp+77uZrq7w5TSHtw0GlnAmwE+8DyhD5E0GfAMGM5o2SPgar1fbdrFFLNgfqyb7l4rivMNryaotru/WiU66H612z6tiXhaPiOZw6f1HzJzOP66++0otmZ+1t11lDtNcimKyHWDXIJRLqFLuZLPm+Vu1r+3n19TWs3PZ1T8Z2hd1A3J/mWA5QDv6pNyuaq9Vt7ypYiXMuNLFeeMK+M1RNpU0cpmkbcm2lkv10Dz8D8T/43yC6d0QW2HVorVqGJMUVxKuL8v+lVGKNLUKDdeRfoufBvSxI3pieqCsIEIO/ZtnInOqU09x56KBXZX750qMNZpAgvNyahfmDviwiIbcQWrCC8CxIzMCyFUWuKwNsXgMpO4MWdY8LCQeyAZ9EbUD8p0lAH35kUA9MnUJ4yPPN7yaHm8xzbRnePxWx4zHgOPU7a5oR5nhXbWq9pq4BIYJWYMntQTtn7g6cXikD1j8FT+xBvx47KB9+Bzsce7x+Uj3ot9Dvueh4ZcYvkKGIVIvEcn2D4MfDDAojNYYLEhngrG9uQzrUVeZYoLvpRYxCc/JXQmvoAG2qwJU+fZBv6rZA/9peiv4CfxVa69wY4S3kt9wA04s8BRm8/A2+if+SyuxfyIJxz1eJMBYxcn3oiNRdzEW6M9PQ6M4dNJLOJtrA/mRzywj7l7C5+0ERNvxcaHgXde+xBz9w681Jx5J34CdOaih3CyR8291BzrgMU/+jJg1ERq7nP4lDozn0sNUf+eR4+89Iv5SuISn/xQXxJfIm4lsUqnQyY2xJdS/6oa8QVwilsCS47gcc8Y8z0fDOxdtA8G9lIT5o3Yo1Y9b6HBx1gBz13wMS/m5TnFvPB4iB/4Uf7Ao6cHmjYjJYfXC23AhFH0WOyEqVEGi3J+IxT0t/Iv/3ji38PbXz7/VH8hp3E5H2Be+4SvM/9lZj5p1N1x/3G5anH8mOIYcjXb7bfLDe5mx+1Tu0/3OPidJ+qz4l+DEyUOal/Pgv/7WZCqn723B/O9ycGrQq2WB3T97+WGtu4X",
        },
        {
            "data": "m=edit&p=7VdNb1s3ELz7VwQ88/D49b5ubhL34rofdhEEgmHIroIYletWttpAhv97Zpa7fk9GixYwUOQQCCKHw+FyuVxS1N0f2+Vm5UPrQ/Cp940P+LS59bmAa/JQi0Y/Z9f369X4yh9u7z/ebgC8//7oyH9Yru9WBwtVnR887IZxd+h3344LF5x3Ed/gzv3ux/Fh9924O/W7U3Q5n8EdV1EEfDvBd9JP9LqSoQE+AYYxDnsPeHW9uVqvLo7RC+aHcbE7847zfCOjCd3N7Z8rp36wfXV7c3lN4nJ5j8Xcfbz+XXvutr/c/rpVbTh/9LvD6u6xuctZ1N00uUtY3SV67q6u58Xurq9/W336O0+H88dHRPwn+HoxLuj2zxPsJ3g6PrjcuzF512Y3ZlSDtLpOqiFJFZraDCFoDbHUykeMwuCQ2trOqNkuUWvVq9nQ18lCj7lZD03lbb6hSB1DtRejtlPVxQS7rLPWhTqs50TXg4y4YMCZZogN10YqOd8ZBY+VMlWHSRYuzQfSX9lkbfeYhxLkm1F0GTGfUxIuymbGJXTUNXNO/HqmezZliCJq5m5JvHWNtiCJ/TP3ZR9o7EnEDeFAeDFxOsF8BXXhZc8YN23PGHdvj+A27vleg7PvE/d2LoqNOBnmItn4hct7HJOAxmYRjFFdeCKYIfuErHhGMGdoem6G+bNw3TQdcimMDyjfS3kkZZTyDEfH75KUb6RspCxSHovmLfIwxc6njDhGD9wDw1fB4Ok3cabGcPKpRcAEZ2DE2/isuKXGeNhsbewAjKQwPituqVFcYLPTsaUAI57GF8UdNca3wAiMYPjJnDC+KO6oUdzCZq9jW/A8LMa3intqFHfRpwGbIRjrYrIY3ykeqFHc4xeIuSK4A9Z5waMtGP0TPzQ+B6SD4ACME6g82lUfqDE+Adu8GVhjBR5t1VNjPOZingqGPzy5yqOtemrMN4yN1X5uYJ8H2/hGcaTG+B647m9uBuC6j8I3ipFXT3woPqcaf5mXF4Lx6if6Jz4CZ9VH6HlZGB8VZ2psLGJYNG4pAte9E56njLhQYzzWUnS9CevlPWN8UlyoMQwfNN8y8i1rXgmv+Yb+icdZyL3ab2Gf95PxekbQP+Nh0/IE5yLz+jJezxH6Zzxi3mtsO+QJbzfjO8U9sPHI26z5nJHPWfNWeM1n9M94+Gx51SHOvBiN1zOI/onH2SmN4RZYYwUebcHon/gBOJgd6C0HwKNd9cgN4wtysmjuiR3et8brvOif8R1wjWdBThbNVeEbxbjrJn4ArvEsOHeFV7Xxek7RP/F4fpZU862ECFxjK3xQjNx74iNwVn2Enhe98VFxpsbGYo1675WE+PBHwHg9I+hXHpf6O7naX0uZpWzlyu/4lvqPr636Rnn5r8u/urPIUd7t//wpX/tf0n9+sHCn282H5dUKL/BjvMRfndxubpZrtE62N5erjbXx3+fxwH1y8l0kDM5f/w79/3+HGP3mSzumX5o7uDjc1fIOu/7Xcs3U/Qw=",
        },
    ],
}
