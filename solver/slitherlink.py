"""The Slitherlink solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, target_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import convert_line_to_edge, separate_item_from_route, single_route


def passed_vertex() -> str:
    """Generate a rule to get the cell that passed by the route."""
    rule = f'passed_vertex(R, C) :- edge(R, C, "{Direction.TOP}").\n'
    rule += f'passed_vertex(R, C) :- edge(R, C, "{Direction.LEFT}").\n'
    rule += f'passed_vertex(R, C) :- grid(R, C), edge(R, C - 1, "{Direction.TOP}").\n'
    rule += f'passed_vertex(R, C) :- grid(R, C), edge(R - 1, C, "{Direction.LEFT}").\n'
    return rule


def count_adjacent_vertices(target: int, src_cell: Tuple[int, int]) -> str:
    """Generate a rule that counts the adjacent vertices around a cell."""
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    v_1 = f"passed_vertex({src_r}, {src_c})"
    v_2 = f"passed_vertex({src_r + 1}, {src_c})"
    v_3 = f"passed_vertex({src_r}, {src_c + 1})"
    v_4 = f"passed_vertex({src_r + 1}, {src_c + 1})"
    return f":- {{ {v_1}; {v_2}; {v_3}; {v_4} }} {rop} {num}."


def count_adjacent_segments(target: int, src_cell: Tuple[int, int]) -> str:
    """Generate a rule that counts the adjacent segments around a cell."""
    rop, num = target_encode(target)

    # segment count = vertex count - edge count
    vertex_count = count_adjacent_vertices(target, src_cell).replace(f"{rop} {num}.", "= C1").replace(":-", "")
    edge_count = count_adjacent_edges(target, src_cell).replace(f"{rop} {num}.", "= C2").replace(":-", "")
    return f":- {vertex_count}, {edge_count}, C1 - C2 {rop} {num}."


class SlitherlinkSolver(Solver):
    """The Slitherlink solver."""

    name = "Slitherlink"
    category = "route"
    aliases = ["slither", "tslither", "touchslither", "vslither", "vertexslither", "swslither", "sheepwolfslither"]
    examples = [
        {
            "data": "m=edit&p=7VbvT/JIEP7OX2H2q5tcfwGlyX1ABF89RFQIrzSEFCxQbVlv26JX4v/uzBau3VK8XLyY+/CmdDLzPLPTnd3uU8I/Y4e7tA6XblKFqnDpiiHumoK//TXwIt+1TmgzjlaMg0PpTadDF44fuvTqYdVtsebrefPnxozGY/VCiS+V0VPn6fQu+OPS07na6Zn96/61py2bP1pnt7X2aa0fh8PI3dwG6tnTcDxY9EfLhvZXuzc2kvGNUr0aL37bNIe/V+zdHCaVbdKwkiZNLiyb6IQSFW6NTGhya22Tayvp0eQeKEJVwLrgQYIGbjtzR4JHr5WCqgJ+b+eD+wDu3ONz3512U6Rv2cmAEnzOmRiNLgnYxiXpMBHPWTDzEJg5ESxVuPJedkwYP7LneJcLBUkQ+5E3Zz7jCCL2TpNm2kK7pAU9awHdtAX0SlrAzr7cgvu4dN/KZt8on/077MwdzH9q2djKMHPNzL23tmB71pZoVRipw6sGJaGg1oAQ37w01JHVsrAGIb6Zu7Aus/JYQ5GSDVVKNnBsllyV2RqWymZV1+UQ2SzZxAdlpUwslSWbODbHGnIot9/AsRnbyLcPC6aKZXsQtiOsJuwAVpUmurDnwirCVoXtipy2sCNhW8IawtZETh335V/t3NenA3sP/TVM2DkTNhYdVTeoagCq73x8AYRfBRyS0Df2Of/Yj61Bau6CIv91NKnYpA1H5KTHeOD4cFB6cTBz+T4GoSIh86dhzBfO3J26b848IlaqlXlGwtaihgT5jL343rqswp6SQG+5ZtwtpRDEY32kFFIlpWaMPxbm9Or4vtyL+IZIUCo+EhRxUJZc7HDOXiUkcKKVBOSEVKrkrguLGTnyFJ1np/C0IFuO9wp5I+IWZ9D49VX5/35VcJeUb1aorwqmDYv9t6bR5IaSl3jqTKE1An9haEaDzB2lU+Urp0FBywlQ1GMFd/J5QH/72onTyPgn0piRRbhEIAH9RCNzbBl+RA5zbBE/0D6c7KH8AVqigIAWRRCgQx0E8EAKATuihli1KIg4q6Im4qMOZBEflVdGm4S+F61cDkv2TCaVDw==",
        },
        {
            "data": "m=edit&p=7Vbfb6M4EH7PX7Hy61o6bAIFpHtIs+n+uJZNt4lyDYoikpKWLpQ9AmmPKP97x0NytQ3JPZxOWulOhJHzzfjzzBg+s/6jDPOIunCZDjUog8t0DLydrvgZ+2sUF0nkvaO9snjIchhQ+tWnqzBZR/TL7cNlP+s9f+j9vnGK6ZR9NMrPxuTx4vH9t/S3z7GZswvfGV4Nr2J+3/vUP7+2B+/tYbkeF9HmOmXnj+PpaDWc3Lv8z4E/7VbTr4b1Zbr6ZdMb/9oJ9inMOtvK9aoerT56ATEJJQxuTma0uva21ZVX+bS6ARehDLBLGEGACcNBPeQwnKBfgP060oChX/vFrFsYLuN8mUTzy3rG0AuqESVimXOcIoYkzTYRqafh/2WWLmIBLMICGrV+iH/sPevyLvte7mNhCZKWSREvsyTLBSiwHa16dQWD0xWI4akKRL7/uILo7j56aUvebU9+B/vyDdKfe4GoZPw2vPG2YH1vS7gjwmHPmNg14OHuoSN7wGQCuCHUOQCmDlj6FFsDusjBJYALYCKadECQVZ5zpgOYqjIHc5WSt/RMLMxEjkBWmcRCWik3C1nlENvQQmy9HhtppZ7YDZIzneQMeyAD2AJlDtYj0To4RyrQ6eoResWuvl0uksrLuPp+udgTGWiUwwz9uWCGvmPM0J8uZjSJGDbGkIIYUqtBerMYw7oUBLllhCO1QsT1rWNcf2gYx36o0xq1mY2M6hdDQfT9Y6b+oDBTf+FYV20IvKkM39dbtBdoOdoRvM60MtF+QGugtdBeYswA7QRtH20XrY0xZ2idgzQcl4y/QiT1+Ncz23UC7uDZJ1/Wz4XMOgEZgDS/87M8DRMQaL9MF1F++A/HI1lnyXxd5qtwGc2jl3BZEK8+oWWPgj0hhwIlWfYjiZ/aGA4uBYzvn7I8anUJUBwnR6iEq4VqkeV3Wk7PYZKoteCHiwLVh54CFTmcaNL/MM+zZwVJw+JBAaTzW2GKnrRmFqGaYvg91FZL39qx65AXgnfAKbfg+P7/Y+Yn/ZgRm2T8/SfNf1oua6XJ8hNi8+bU4RbJAfSE6kjeNvyIwEheHW+oiUi2KSiAtmgKoLqsANRUFgAb4gLYEX0RrLrEiKx0lRFLNYRGLCVrTTDrvAI=",
            "config": {"swslither": True},
        },
        {
            "data": "m=edit&p=7VTLbtswELzrK4o98yDqYVO8uW7ci5s+7CIIBCFwHKYWIlepHkVAw/+e3ZUAmkGAoijQ+lDQGsxyZ8kR12L7o980RmQ4YiVCIXHEKuRHJfQLx7Euu8roN2LWd7u6QSLEx8VC3G+q1gT5qCqCg820nQn7XucQgwCJTwSFsJ/1wX7QsK33tyUIu8I8CImJJTJURUgvHL3iPLH5MClD5JcjR3qNdFs228rcLIeZTzq3awG02VuuJgr7+qeBoYzjwQBO3G46fKN2Vz6Omba/qx/6USuLo7CzX3iOnWeig2dir3imV/ljz+bum3l6zW5WHI949l/Q8I3OyftXR5WjK31AvNQHiDIsjbDdWI6rxSmG1P0hTGIMYxe+yE692pSyTpxS1olT2shlJ9Krnfjiqb+R8sXKd6X8fRUt5cKMxK4287My9JeWofJ2ljLy4+hlnJysh2cq+WSvGReMEeMaD17YmPEdY8iYMi5Zc8F4xThnTBgnrJlS636ruX/BTh4pvixOR3peM0WQw6pv7jdbg5/MvN4/1m3ZGcBL6hjAE/DDLUz+31v/8t6iPoTn9gc/Nzv4yUFbld3ONFX5/QGK4Bk=",
            "config": {"tslither": True},
        },
        {
            "data": "m=edit&p=7VTfT+JOEH/nrzD76ibXH/xscg8V0dPDigrhK4SQggtUW9bbtuiV+L87s8Vrt1STy/dy8eGydDLzmdnZmWH3E/6IXcFoA5bZpBrVYZlaVX51DX9vq+9FPrMOqB1HKy5AofTSoQvXDxk9v11129x+Orb/2zSj0Ug/1eIzbXh/cn94HXw/80yhnzjN3kXvwjOW9rf20VW9c1jvxeEgYpurQD+6H4z6i95w2TJ+dpxRNRldarXz0eLLxh58rYx3JUwq26RlJTZNTq0xMQklOnwGmdDkytomF1bi0OQGXITqgHVBgwAD1E6mDqUftXYK6hrozk4H9RbUuSfmPpt2U6RnjZM+JXjOkdyNKgn4hpF0m7TnPJh5CMzcCCYVrrzHnSeM7/hDvIuFhCSI/cibc58LBBF7oYmdttApacHMWkA1bQG1khaws//dArtbsuey6lvl1b/AP3MN9U+tMbYyyNRmpt5YW5COtSVGFXYacNMgJSQ06mDixduZTcU0NSW4isE5E4Mzs4bB2d6aAWb1l1lXgxsYbGamGtzAIjOzhcE5E4OzVC0Mzs5t5TuCpnXZ+q2UJ1IaUvZhMjQxpTyWUpOyJmVXxnSkHErZlrIqZV3GNHC2vzX9v1DO2MBBZav2561JZUw6cEsPHC4C14e76sTBjIk3G7iChNyfhrFYuHM2Zc/uPCJWSld5j4KtZQ4F8jl/9L11WYY3lwJ6yzUXrNSFIL6sd1KhqyTVjIu7Qk1Pru+rvUgWV6D0/StQJOBx52xXCP6kIIEbrRQgx2VKJrYuDDNy1RLdB7dwWpCN46VCnon85POr/iP2z0vs+C9pn41gPls58oJz8QHbZM4iXMI5gH5AOzlvGf4Ow+S8RXyPTrDYfUYBtIRUAC3yCkD71ALgHrsA9g7BYNYix2BVRZrBo/aYBo/Kk82YhL4XrZiAkT2QSeUV",
            "config": {"vslither": True},
        },
        {
            "url": "http://pzv.jp/p.html?slither/25/15/i5di5di6bg3ad13dc13bd3cg5bi7ci7dhai6bi6ci7b02bd33cc23d8ci8ai6cibh6di6bi7dg1ca31ab10dc3dg6bi6ai6chai7ci7ci8d33dc33cc20d8bi7di7cidh8di5ci6cg3dd03cb02ad3dg6bi7ci6bg",
            "test": False,
        },
    ]
    parameters = {
        "swslither": {"name": "Sheep/Wolf Variant", "type": "checkbox", "default": False},
        "tslither": {"name": "Touch Variant", "type": "checkbox", "default": False},
        "vslither": {"name": "Vertex Variant", "type": "checkbox", "default": False},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(convert_line_to_edge())

        if puzzle.param["vslither"] or puzzle.param["tslither"]:
            self.add_program_line(passed_vertex())

        if puzzle.param["swslither"]:
            self.add_program_line(separate_item_from_route(inside_item="sheep", outside_item="wolf"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if puzzle.param["swslither"] and clue == "W":
                self.add_program_line(f"wolf({r}, {c}).")
            elif puzzle.param["swslither"] and clue == "S":
                self.add_program_line(f"sheep({r}, {c}).")
            else:
                fail_false(isinstance(clue, int), "Clue should be an integer or wolf/sheep with varient enabled.")

                if puzzle.param["vslither"]:
                    self.add_program_line(count_adjacent_vertices(int(clue), (r, c)))
                elif puzzle.param["tslither"]:
                    self.add_program_line(count_adjacent_segments(int(clue), (r, c)))
                else:
                    self.add_program_line(count_adjacent_edges(int(clue), (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
