"""The Ripple Effect solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import full_bfs, validate_direction, validate_type


def ripple_constraint() -> str:
    """A constraint for the 'ripples'."""
    row = ":- grid(R, C1), grid(R, C2), number(R, C1, N), number(R, C2, N), (C2 - C1) * (C2 - C1 - N - 1) < 0."
    col = ":- grid(R1, C), grid(R2, C), number(R1, C, N), number(R2, C, N), (R2 - R1) * (R2 - R1 - N - 1) < 0."
    return row + "\n" + col


class RippleSolver(Solver):
    """The Ripple Effect solver."""

    name = "Ripple Effect"
    category = "num"
    aliases = ["hakyukoka", "rippleeffect"]
    examples = [
        {
            "data": "m=edit&p=7ZdPb+M2EMXv+RQLnXkQyaFI+pZuN72k6Z+kKBaGsXBSLzZoArdOXBQK/N37hn5j9tBFgQJt97BwTL1Io5mx9eYn+enX/Xq3cT7qXyxudB6vFEN7e5H2Hvm6uX9+2CxeufP984ftDsK5by4u3Pv1w9PmbMmo1dnLXBfzuZu/WiwHP7gh4O2HlZu/W7zMXy/mKzdf49DgPPZdHoMC5Jsuf2zHVb0+7vQj9BU15FvIu/vd3cPm3eVxz7eL5XzjBq3zRTtb5fC4/W0zsA/9/277eHuvO27Xz/gwTx/uf+GRp/1P25/3g5U4uPn84+3G3m48tRv/ut3w77dbV4cDvvbv0fC7xVJ7/6HL0uX14uWgfenq2/q2rRdtDW29QaibY1u/bOvY1tTWyxbzZvEyxLG4GNKwCG6I3kMX6snFGKkr9HTUAfuF+wPOFZ4bECOMiXBhGqkTdKDGuYnnSoCu1OLi5KkRM1lMhhZq5J+YP6HPiX0m1MqslRCTGTON0JkatTJrTahVWGtCb4W9TahVWGtCnsI8GXkK82TEVMZkfPbKz14QUxlT0FtlbwV1K+sWcTKybknQrFsmaH7ekqGZvyLeM74i3jO+IsZbTIE+9oDc0IU6QFfq6CSM1MgZjjmRG5rxoIZExnjERItB3RioUTce6yIfdKZGnsg88IPQDwI/CP2AfNCMicifmB9+EPpB4AGhB5ADmnXhB5ksBj3QD8gHzVrwhtAbyA3NWgnfw8TvAT4R+kQS8mfmhzeE3kAdJ4Ux8InQJ6gDbfHop7AfeEboGdSBZg/wjNAzktFPYT8ZtQprwT9C/6AmNOPhGaFnkNslegb5oFmrVGjWgjcSvSF1gmZv8EaiNxI8kOiBNCI+HONxHnSlTnqzOGpc38Tri1hoejhgXsKfOBDo+ZA7N5QJweKVG8YBzAh9hS20MSF0zig36DFsoTlfgngJnRvGH+WG8Ue5Iblzg37DFto4UzuXEvqhD8GnziXlhrFoUs4YH0LnEnxy4pLyhD4En6CNOahL78WcOpfy1LmkDDEuKUOMS8qNYkyInUtF2WXMSZ1RYMiJUUU5xs9elT/MU2NnVy0nLjUOmH+8ciN2JpAzbfaNLbgXnHgCD0gwDuTOE51940kcO0+UA8YTXHfhdce2s0WZYGyJubNFECM2+7nzRDkgNuPIz3tNm31ji85+4rlJ+ZM6BxLnCNf9xJ/Jd/7ovPOatnk3tuhcG0N0lo0huXaGFN+5oXNt3Cixc0P5b6xQ/hsrlPnVZhz7q+0vnQ9VOWBzPZ5YgS00Zxn3gsT7S+MAGdI4QIZgC815x3VPvO7YdoYoHzzjvXLG4sElegNbaONJ7cxRnvC+gy35c9AHLn0Med1WaevUHk+yPuf8x09Cf9vOEs70H3mlz0f+yZHV2XK43u/er+82eB6+2j/ebnavrra7x/UD/r9uz8b2P36QHM6G34f2XuKXjpPPv1H+p98oegnGT20+P7V2QIzV2R8=",
        },
        {
            "data": "m=edit&p=7VZNbxMxEL3nV1R79mH97c0FldJyKeGjRaiKoipNUxqRKJA0CG2U/84b77imTiWEEKJIaLPO29nxzIvfi3fXXzbj1VTImj46CHzjMDLEUwUXz5qP89ndfNo/EIebu9vlCkCI1ycn4mY8X097Q84a9bZt028PRfuyP6xkJSqFU1Yj0b7tb9tX/XYg2jPcqoRE7LRLUoDHGX6I9wkddUFZAw8YA14ATmaryXx6edpF3vSH7bmoqM/zOJtgtVh+nVbMg64ny8XVjAJX4zv8mPXt7DPfWW+ul582VWqxE+1hR/fsEbo609X3dPXjdNWfp9uMdjss+zsQvuwPifv7DEOGZ/3tjnhtK13T1Gfg0mlTaVkGVBnQZcCVAV8GQhloioAxZcCWASoq7y9tScuWtGzZ1JW0fFkjlD9eypKXVGUfqcpGcm8BpClbSbNXx1Adl69tqY20e/xsufbS7vXeWwhpy+WXbo+f2+Pn9tbCPRQJnpLRWRdxPImjiuM5jCdaHccXcazjaON4GnOO4UclrVAK9BT2C+mFIj8SVsAmYWxJtKCEtQS2jBWwY6yBfYdNLZQ1jJFvOd8gx6YcbHGuZoz6jutbAxwYI8dzjkWO5xyH+p7rO9T3XN+Bj2c+jrZRzvfID5zvFW2tjNErcK8A3CTshK65bwjAXKfBXl1znQY5knMaD8xr1SBfdvmoAWwYK2DH2AB3vTTt/4pzpAb2jJGjUg7qsy6YB8z1lQVuGIOPqRkjh/XCPOBufTS00DZh9EpakNbcK2qd/EBa66Q71o12oqRv8oYhD6Q4eSDpbrJPDHkpaQq/WZf1TRwscmzKAQfLHGyTfUK6O+7rfPaJt1l3T57hmoG0Zm5BZw+Q1oG5BZv9EB+7aa7/wRvkJeYTwKdJumNu4+49kPwT9a1t1lcm7cgDOmudvEFay5Rvs08keYz9oMgPNmudfEL6Jj/oJnsAGmnWCF4A1ll31gjf7I0dPUppSziKo4mji1uFpyfYLz3jfn9X+imdoe5emB4e9t+LjXrD6myzuhlPpni/OL7+OD0YLFeL8RxXg83iarpK13i92/Wqb1U8h5reFv+/8f2lNz6SoH5q/4mnRgf/0lHvOw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))

        flag = False
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(f"number({r}, {c}, {num}).")
            else:
                flag = True
                self.add_program_line(f"black({r}, {c}).")

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            if flag:
                self.add_program_line(f"{{ number(R, C, (1..{len(ar)})) }} = 1 :- area({i}, R, C), not black(R, C).")
            else:
                self.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i))

        self.add_program_line(unique_num(color="not black" if flag else "grid", _type="area"))
        self.add_program_line(ripple_constraint())
        self.add_program_line(display(item="number", size=3))

        return self.program
