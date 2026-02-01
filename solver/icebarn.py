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
