"""The Martini solver."""

from typing import Tuple

from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import area, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode, target_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import area_color_connected, grid_color_connected, grid_src_color_connected
from noqx.solution import solver


def count_reachable_src_white_circle(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4):
    """
    Generate a constraint to count the reachable white circles starting from a source.

    A grid_src_color_connected should be defined first.
    """

    src_r, src_c = src_cell

    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    rop, num = target_encode(target)

    return f":- #count{{ R, C: {tag}({src_r}, {src_c}, R, C), white_circle(R, C) }} {rop} {num}."


def program(puzzle: Puzzle) -> str:
    """Generate a program for the puzzle."""
    solver.reset()
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c("gray"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type=8))
    solver.add_program_line(area_color_connected(color="gray", adj_type=4))
    solver.add_program_line(grid_color_connected(color="gray", adj_type=8))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))

    for (r, c, d, _), symbol_name in puzzle.symbol.items():
        validate_direction(r, c, d)

        if symbol_name == "circle_L__1":
            solver.add_program_line(f"not gray({r}, {c}).")
            solver.add_program_line(f"white_circle({r}, {c}).")

        if symbol_name == "circle_L__2":
            solver.add_program_line(f"gray({r}, {c}).")

    for (r, c, d, pos), num in puzzle.text.items():
        validate_direction(r, c, d)
        validate_type(pos, "normal")
        if isinstance(num, int):
            solver.add_program_line(grid_src_color_connected((r, c), color="not gray", adj_type=4))
            solver.add_program_line(count_reachable_src_white_circle(num, src_cell=(r, c), color="not gray"))

    for (r, c, d, _), draw in puzzle.edge.items():
        if d == Direction.TOP and r > 0 and draw:
            solver.add_program_line(f":- gray({r}, {c}), gray({r - 1}, {c}).")

        if d == Direction.LEFT and c > 0 and draw:
            solver.add_program_line(f":- gray({r}, {c}), gray({r}, {c - 1}).")

    for (r, c, _, _), color in puzzle.surface.items():
        if color in Color.DARK:
            solver.add_program_line(f"gray({r}, {c}).")
        else:
            solver.add_program_line(f"not gray({r}, {c}).")

    solver.add_program_line(display(item="gray"))

    return solver.program


__metadata__ = {
    "name": "Martini",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VRdb9owFH3nV1R+9gP+wNC8TKyDvTC6DaaqiiIUaLqigdKFZpqM+O8998YMRFJ1q7TuZYrinBxf+x4f23fzvUyLTDo8pifbUuHRzvGrrOW3HZ7p8mGVRWeyXz7c5QWAlJfDobxNV5usFYeopLX155HvS/8+ioUSUmi8SiTSf4q2/kPkx9JP0CVkD9yoCtKAgwO84n5CFxWp2sDjCjvAa8DFslisstkIvWA+RrGfSkF53vJogmKd/8hE0EH/i3w9XxIxTx+wmM3d8j70bMqb/FsZYlWyk75fyZ00yDUHuQQruYQa5NIq/rLc82S3g+2fIXgWxaT9ywH2DnASbdGOo63QloZiZ1S1N0J3iXgDdwNhNRHmEGFPIzo8xxHh3MmQLs9BfjCB3IoVXJMC6tNY4rEtlS5En7CUusYaiq3NwLprsdY0xjbPQMuos40a2IMa6xqzsT21WPbohIVFQzZKczvF7klvuH3HbZvbDrcjjhnAUqW0VOQrUuMrlQnYAJMvzOOGH8doaGVsgLEaxrj35C6P5RpQYaoHtGLCHWC352n+MI/FPPt4Gms6AXeA4QBhhdqiA9bAe95QzQnYEobnhB00u6DZIRf5yxi59hoc6Qm5HHKR24wxT5cwTLpiqy64tdw6trBL1+M3L5AIhhl8etVtOj7XL9u6Z7XFtFW/HizvpThpxWJSFrfpIkMlGdx8zc7GebFOV/gbl+t5Vuz/Uch3LfFT8BvDaWn/1/Z/VNtpC9p/VOFf4Uw+IyeGuzi1/lKK+3KWzhY5zhi8Y948wT8Rb+rxr75aXMKk9Qg=",
        },
        {
            "data": "m=edit&p=7Zdbb9w2E4bv/SsCXfNCB5KS9s7NZ/fGn3twiiBYLALH2TRGbWzqQ1Gs4f+eZ8iXey6KFiiSi2Cxmkezo9HL4YjU3v/+eHk3d010Tee6wdWu4RN9dKFrXdMMYz7U+ry6friZT16448eHj4s7wLkfTk/dh8ub+/nRVFGzo6flOFkeu+X3k2nVVK5q+TbVzC1/mjwt/z9ZnrjlBT9VbsB3loNa8GSNr9PvRi+zs6nhczH4Bry6vru6mb89y54fJ9PlK1fZfb5LVxtWt4s/5pV02PnV4vbdtTneXT4wmPuP15/0y/3j+8Vvj4ptZs9ueZzlXhyQ263lGma5Rgfk2ij+Y7nj7PmZsv+M4LeTqWn/ZY3DGi8mTxzPJ0+Vb+1SZqbJc1PFWIYuR+93HEO6ZMPRtLshTTvuesbdq9q4HYOgJsl6U2Th36pV5QPedtebFO/F9vVBrynd86YR7XnH/pA3D/aA20az707D3nO39cGR5JLsRyd9O9EU6jSVq03HV0ysW3bp+L90rNMxpONZijmhsF30POEMgXRY5+vMWOdtaMZtt82+y+zbDW5gdJVrbUSJA8yMJI4wVbR7xZ77iod+5cdyL3FrPIgH8ostZ6v8rfFG/sLedEqzR4/1SmLifYkh3rrFOMKDeDCWBrQFacPC0uDRFhXDWHzc8Bed3jQzhYlH5wM9mOLxD4oZhlVOrAsaL9aFksfirRUSk2cQswSHOjPWhSbnx8KNuIHzvGBhzVeonbdnwriHR/FonK/FrvKkmL4wc91rrnt6wJo6xVv+zB3xnXJinZc2rPOduINLTcxf7oVmrzxYWJrZjXxX9DOnQXPaMaeFG7jL3I1wI+4Degq3sHSieetenbhDw4pNs7SxAfogfzAuetDWi3tj9V6Pzl7a0OB79VhPj/XqH4sZFT96apgZy4Yr7oxzHiyc8wQ26dCoP42Lv4ODOMC6L9aFUTxGF5vMWBdXOTvy5LFgySNmjCFID/UPGmNgvGumB1SHQJ9wvu5nWxMT06vqASysXqXmvGCIyaM6h4B/k9WHKb96NdDP/LZm9TaWGDF9GNWHWMYrv73YeNWQ57c8d1hYmnl+g55BrAt6BrFb+Vd67NlRj2Fh1WSkVpprLKw5pVdX80LOqOcau9IcbK0o92VN4FyMZq0/ibV2BdaxNZNf61tgnedcjB6t/7HmJa/OmrFw1oyFS4yH87VYWP3D2hu1TmLhrAfrYlnTBsupmkRqYvtYqi0cS5/A2kcCGjhfs/RgYdUQPUF6sLDGyD4VtDdhyS+ONl6xxWhfw8LKw54StF8E9o4tjopn3wxR/ki89pHUS4WpSdB+hIU1F+xrpd+8zUvZK8nDuZg1QfnT/qX7+oF1SXXz1HCLNUYsfjHz6zW/2HV+Wz/TM8uLwOv0OvAyHX06xvSa0Nvb4T96f9x8aft3byR/K2dKt9jfkb/+hG+/f8nfZ0fT6uLx7sPl1Zz/JCfvf52/OF/c3V7ecPZycftpcX/9MK/4O/h8VP1Zpe+040L/7R/iF/qHaFNQf23P+dcmh5VndvQZ",
            "test": False,
        },
    ],
}
