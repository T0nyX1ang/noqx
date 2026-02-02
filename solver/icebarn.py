"""The Icebarn solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.route import count_area_pass, crossing_route_connected, directed_route
from noqx.rule.variety import straight_at_ice

dir_dict = {"1": Direction.LEFT, "3": Direction.TOP, "5": Direction.RIGHT, "7": Direction.BOTTOM}


class IcebarnSolver(Solver):
    """The Icebarn solver."""

    name = "Icebarn"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=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",
        },
        {
            "data": "m=edit&p=7VbvT+M4EP3ev2Llr2vp7PxupPtQumVv96BbFhBHq6oKJdCwCeHSFPaC+N95Y7s0TQN3upNOe9Kprefl2Z55YzvjLn9fRUXMpaCvHXBYfBwZqJ8VeOonzOckKdM4fMd7q3KRFwCcfxnyqyhdxvzz+eKgn/cePvR+uw/K8Vh+FKtP4uxm/+b91+zXT4ldyP1hMDocHSbWde+X/t6RN3jvjVbL0zK+P8rk3s3p+ORqdHbdtf4YDMdONf4i3M/jq5/ue6c/dyYkC59p57HqhlWPVx/DCbMYVz/Jprw6Ch+rw7A659Uxuhh3p5xlq7RM5nmaF0xxEuMOgCTjFuBgA89UP6G+JqUAHgJ7eto5YFQU+cNsONvT1CicVCecUfA9NZ0gy/L7mKLBh3qe59lFQsRFVGL5lovkjnEbHcvVZf5tZYbK6ROveioFM2OdByK9lQc8rfMgqPMg1MzDJPrP80iT2/gyKVqS6E6fnrBBX5HGLJxQRqcbGGzgcfjInC4LXc48oY3UxtbGVcb3lQmMCZTp6glS6DFS6F4pdLeUxtpmnG0Z6xhr5jkeLLQMw0e0UrXn0OUKCJvYvLFIkIaJE8zc4REQx3OHp5TaxnsQ3Dbep7i7vC+QQIsfnxJu4yUSb+Nb9SPpfZW6pdoT7A+vbNV+UK1QravaAzVmgEWyHMktFw4tvICuC4zVVBgFw0WChB27hi2OZ4Mx10FShD0UGQ+JK9zllg/xhH2BwoMdIxzAzwuGn0D7saXktqU1wAJrDba0ahhjpI5lWz63HWyK4m2MMdq6XYwx2ggLrQEWvI4Li/FYcOUngB/jU1JcrR+W23TqCNuYa69jIe4L9uBTx1VzpVm3AD5po1Vc6BcmRwGdYp07FWSzVgHWit4EheGzrlnoWFaAuC+YCrnJ18f6B2bvAuxdYDT4tLZrjDG+2SPkYjlGg+NgT/U6wG7G0FzfrKFL+7jeazobRrNN+27iOtBDr77ad/inl0Xxfg1jjEOacejO1NHrq9ZRraeOpE8F5S+WnN2X/e+d/j+VM0HW5r4yH//ffZ52Jux4VVxF8xjFe3B5Hb8b5kUWpXg6XkR3xPbz7C5fJmXMcKeyZZ7OlnrGLP4ezUsW6mu93rPF3a6yixjXUY1K8/yOLocWD+uuLTK5vs2LuLWLyBi6X3FFXS2uLvLisqHpIUrT7VzUP54tap4U83SbKgtcdbVnVTS3mCwqF1tE7Xrf8hTfNhazjLYlRt+iRrRssxxPHfadqR/uJOv/P0D/gT9AtFniR6tJP5ocdc7z4o2is+ls0i2lB+wb1afW28a/UmhqvU1+p6qQ2N3CAraltoBtlhdQuxUG5E6RAfdKnSGvzVJDqprVhkLtFBwKVa85k2nnGQ==",
        },
        {
            "data": "m=edit&p=7VVdT9tIFH3Pr6jmtSOtx58f0j6ENHTbhTQUEEusKDLBEFObYR0bukb8954Zj4m/YFe7feBh5WR8fObOveeO7ePtn0WYRdTDYbhUowyH4Wry75rip6njJM6TyH9Hx0W+4RkApV9m9CpMthH9fL45mPDxw4fxH/duvliwj1rxSTu72b95/zX9/VNsZGx/5s4P54exfj3+bbJ3ZE/f2/Nie5pH90cp27s5XZxczc+uPf2v6WxhlosvmvV5cfXL/fj011EgROFYjh5Lzy/HtPzoB0QnVP4ZWdLyyH8sD/3ynJbHmCLUWlKSFkker3nCMyI5hrgDIEaoDjjdwTM5L9CkIpkGPAO2q2XngGGW8YfVbLVXUXM/KE8oEcX35HIBScrvI1ENOeT1mqcXsSAuwhzbt93Ed4QamNgWl/xboULZ8omWY9mCWlH3gUqv9YFMdR8CVn0I1O1DNfrf+0ji2+gyzgaa8JZPT7hBX9HGyg9ER6c76O7gsf9ITJP4FiWWJ0+OJk+eJU9Mqy6ZVs0ynamzoc4iDolm/iNGJsdzJMUjCykG7XRITIZEgdPnDWc43hT8QLwNIQPxlumCZ33eQpcBFHd5qXMg3kODvXg0ty9b1OV4gk2kpSHHD3LU5GjJ8UDGTLEZzPOoznTi63hLmA6M5AJr2g4zk+o6mhVYd4DRiOStBkYMw47LGPCG4uEWuoGNlbzdwGKtXWELtWxVyzaAsSGSZw2MGAsbK2NQy1F6HOhxVC0bOZ8xYmylx0FdV9V10a+Hja3XPmPEPOeEZk/V8qDBU/vjiLU1RoxT54Q2cVNkPPR7SrMr1tYYMa7KaUGnVfcObNeakdNWOS3okRg36kzerokcTTna8jY64k35h+9S/0X4d0/M38oJTL2yYXU4P/9qOQrIcZFdhesIvjO9vI7ezXiWhgmujjfhnWAnPL3j2ziPCD4HZMuT1bZasYq+h+uc+NUXqTnT4m6L9CKCkzaohPM74WsDGeqpFhlf3/IsGpwSZATdL6QSUwOpLnh22dH0ECZJuxf5oW5R6zhbJ20qz+DSjWtpJS0mDfNNi2h8mVqZotvOZuZhW2L4LexUS3fb8TQi34n8wzHx4Pz/7X7z325xs7S35jpvTY58znn2iunsJrv0gPWAfcV9GrND/AtG05jt8j1XEWL7xgJ2wFvAdu0FVN9hQPZMBtwLPiOydq1GqOq6jSjVMxxRquk5wXL0Aw==",
        },
        {
            "data": "m=edit&p=7VbvT+NGEP3OX3Hy11up3vWvH1I/BA6ud4VcOECURBEywYA5G1PHgasR//u92R1fEsfQqpWqq1Q52X37dnbezHo99vz3RVKlQtr0c0KBHpcrQ/1Xoa//Nl/HWZ2n8RsxWNQ3ZQUgxKehuEryeSo+nt3s75SDx3eD3x7CejyW7+3FB/v0du/27efi1w+ZU8m9YTg6GB1k6nrwy872ob/71h8t5id1+nBYyO3bk/Hx1ej0OlJ/7A7HbjP+ZHsfx1c/PQxOft6aUFi4pltPTRQ3A9G8jyeWsoT+S2sqmsP4qTmImzPRHGHKEt5UWMUir7NZmZeVpTkJu30gaQkFuLuEp3qe0I4hpQ08BPbNsjPApKrKx/Ph+bahRvGkORYWiW/r5QStonxISQ0+9HhWFhcZERdJje2b32T3lnAwMV9cll8WbCqnz6IZ6BR4RZsHlF7LA57aPAiaPAh18+BE/3keeXaXXmZVTxLR9PkZN+gz0jiPJ5TRyRKGS3gUP1muZ8WesFzfdIHufMd0rumMSWBGAY/MgkiZziyIjIm0JfdmVtpmWsrI9Mrmnu0cHjvtmNe5Ife8ziM7BD6Mn9BK3Z5REgrCE0d0dhR5wAHO7AZPDvt4H1n18ZR0Dx/YpNvDUwK9fF88SGJPp6J0e4ybIxpHt+90a+vW0+2+ttlF0sq1hXKxYwpPnyuBIaqxAsaOE1bREruuUB4CIOyhqnjYBI1h42NnCfvw6bc+gxWMCkSHQ2MPGBvV+qQjpP3A/rt/2Hts78HeY3vCPuv60A1YN4BuwFoBcgk4F4qzxQHW0rHTGLp0UzR2gHEjWhyyboh4Qo4npCrKuiF0o1YXcbY4hM+QfYbkh32G2M+Q9zBEDBH7ieDzO4ZWxFoR+WxjwNrIxOzYKO3S+EQPbLTQA7ON9IHNWsd2VrASGDOWwGZPtE962vRasm/9w16yvYS9ZHvCinUVdBXrKugq1lIBsMlFx9liB2vpYGsMXXpatX0EbPZQYz5v6IE5HpwTh88JemDWdRCnxjjUp/po7+jW1a2vj3xA1eov1rPN4vD3nq4/DWeCLPhlyFfw746nWxPraFFdJbMUb4bdy+v0zbCsiiTH6OgmuSd2pyzuy3lWpxZe2Na8zM/nZsV5+jWZ1VZsvhlWZ9a4u0VxkeJdt0LlZXlPb54eD+3UGpld35VV2jtFZIq4X3BFUz2uLsrqshPTY5Ln67noz6k1apZVs3ydqiu8R1fGuiivMUVS36wRK98Oa57Su85m1sl6iMmXpKNWLLfjecv6auk/3mHq/6+r/8DXFd0s+0erST9aOPqcl9UrRWc52aV7Sg/YV6rPymwf/0KhWZnt8htVhYLdLCxge2oL2G55AbVZYUBuFBlwL9QZ8totNRRVt9qQ1EbBIanVmjOZbn0D",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white", directed=True))
        self.add_program_line(adjacent(_type="line_directed"))
        self.add_program_line(directed_route(color="white", path=True, crossing=True))
        self.add_program_line(crossing_route_connected(color="white", directed=True))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color == Color.BLUE, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"ice({r}, {c}).")

        self.add_program_line(shade_c(color="crossing", _from="ice"))
        self.add_program_line(straight_at_ice(color="white", directed=True))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            if len(tuple((r, c) for r, c in ar if puzzle.surface.get(Point(r, c)) == Color.BLUE)) != len(ar):
                continue  # filter ice rooms

            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            self.add_program_line(count_area_pass(("gt", 0), _id=i, directed=True))

        start_point: List[Tuple[int, int]] = []
        end_point: List[Tuple[int, int]] = []

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            symbol_dir = dir_dict.get(symbol_name.split("__")[1])

            if symbol_name.startswith("arrow_N") and d == Direction.TOP:
                if symbol_dir == Direction.TOP:
                    self.add_program_line(f':- not line_out({r}, {c}, "{Direction.TOP}").')

                    if r == 0:
                        end_point.append((r - 1, c))

                    if r == puzzle.row:
                        start_point.append((r, c))

                if symbol_dir == Direction.BOTTOM:
                    self.add_program_line(f':- not line_in({r}, {c}, "{Direction.TOP}").')

                    if r == 0:
                        start_point.append((r - 1, c))

                    if r == puzzle.row:
                        end_point.append((r, c))

            if symbol_name.startswith("arrow_N") and d == Direction.LEFT:
                if symbol_dir == Direction.LEFT:
                    self.add_program_line(f':- not line_out({r}, {c}, "{Direction.LEFT}").')

                    if c == 0:
                        end_point.append((r, c - 1))

                    if c == puzzle.col:
                        start_point.append((r, c))

                if symbol_dir == Direction.RIGHT:
                    self.add_program_line(f':- not line_in({r}, {c}, "{Direction.LEFT}").')

                    if c == 0:
                        start_point.append((r, c - 1))

                    if c == puzzle.col:
                        end_point.append((r, c))

        fail_false(len(start_point) == 1, "There must be exactly one start point.")
        fail_false(len(end_point) == 1, "There must be exactly one end point.")
        self.add_program_line(f"path_start({start_point[0][0]}, {start_point[0][1]}).")
        self.add_program_line(f"grid({start_point[0][0]}, {start_point[0][1]}).")
        self.add_program_line(f"path_end({end_point[0][0]}, {end_point[0][1]}).")
        self.add_program_line(f"grid({end_point[0][0]}, {end_point[0][1]}).")

        for (r, c, d, label), draw in puzzle.line.items():
            if label == "normal" and not draw:
                self.add_program_line(f':- line_in({r}, {c}, "{d}").')
                self.add_program_line(f':- line_out({r}, {c}, "{d}").')

            if label in ["in", "out"] and draw:
                self.add_program_line(f':-{" not" * draw} line_{label}({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_in", size=3))
        self.add_program_line(display(item="line_out", size=3))

        return self.program
