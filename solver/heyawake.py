"""The Heyawake solver."""

from typing import Iterable, Set, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect


def avoid_diamond_pattern(color: str = "black") -> str:
    """Avoid diamond patterns (radius = 1)."""
    rule = f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), not grid(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), not grid(R, C - 1), {color}(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), not grid(R + 1, C), {color}(R, C + 1).\n"
    rule += f":- grid(R, C), not {color}(R, C), {color}(R - 1, C), {color}(R, C - 1), {color}(R + 1, C), not grid(R, C + 1).\n"

    return rule


def limit_area_2x2_rect(limit: int, _id: int, color: str = "black") -> str:
    """Limit 2x2 rectangle in areas."""
    rule = f"rect_2x2({_id}, R, C) :- area({_id}, R, C), area({_id}, R + 1, C), area({_id}, R, C + 1), area({_id}, R + 1, C + 1), not {color}(R, C), not {color}(R + 1, C), not {color}(R, C + 1), not {color}(R + 1, C + 1).\n"
    rule += f":- {{ rect_2x2({_id}, R, C) }} > {limit}.\n"
    return rule


def limit_border(limit: int, ar: Iterable[Tuple[int, int]], puzzle: Puzzle, _type: str, color: str = "black") -> str:
    """Limit the border shades of an area."""
    if _type == Direction.TOP:
        n, key = puzzle.col, 0
    elif _type == Direction.BOTTOM:
        n, key = puzzle.col, puzzle.row - 1
    elif _type == Direction.LEFT:
        n, key = puzzle.row, 0
    elif _type == Direction.RIGHT:
        n, key = puzzle.row, puzzle.col - 1
    else:
        raise ValueError(f"Invalid border type: {_type}")

    def coord(i: int) -> Tuple[int, int]:
        return (key, i) if _type in ["top", "bottom"] else (i, key)

    rule, i = "", 0
    while i < n:
        segment, data = 0, []
        while coord(i) in ar and i < n and puzzle.surface.get(Point(*coord(i))) != 2:
            r, c = coord(i)
            data.append(f"{color}({r}, {c})")
            segment += 1
            i += 1

        minimum = (segment + 1) // 2 - limit
        if len(data) > n // 2 - 1 and minimum > 0:
            rule += f":- {{ {';'.join(data)} }} < {minimum}.\n"

        i += 1

    return rule


def area_border_simple(_id: int, ar: Iterable[Tuple[int, int]]) -> str:
    """Generates a simpler fact for the border of an area."""
    borders: Set[Tuple[int, int]] = set()
    for r, c in ar:
        for dr, dc in ((0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            r1, c1 = r + dr, c + dc
            if (r1, c1) not in ar:
                borders.add((r, c))

    rule = "\n".join(f"area_border({_id}, {r}, {c})." for r, c in borders)
    return rule


def area_border_connected(_id: int, color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """Generate a constraint to check the reachability of {color} cells connected to borders of an area."""
    tag = tag_encode("reachable", "area", "border", "adj", adj_type, color)
    initial = f"{tag}({_id}, R, C) :- area_border({_id}, R, C), {color}(R, C)."
    propagation = (
        f"{tag}({_id}, R, C) :- {tag}({_id}, R1, C1), area({_id}, R, C), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    )
    constraint = f":- area({_id}, R, C), {color}(R, C), not {tag}({_id}, R, C)."

    return initial + "\n" + propagation + "\n" + constraint


class HeyawakeSolver(Solver):
    """The Heyawake solver."""

    name = "Heyawake"
    category = "shade"
    aliases = ["heyawacky"]
    examples = [
        {
            "data": "m=edit&p=7ZbPbhs3HITveoqAZx52Se7fS+Gmdi+u09YugkAQDFnZ1EZsKJWtpl3D756P5LAC2gBpUTS9BCtRI2o4/HE4S+39L/v1brK1iy/f28rWXGEI6e27Jr0rXRc3D7fT+Mwe7R+utzuAtS9OTuyb9e39tFiKtVo8zsM4H9n523FpamON412blZ1/GB/n78b52M7n/GRsT99pJjng8QG+TL9H9Dx31hX4TBj4Cri52W1up8vT3PP9uJwvrInzfJ1GR2jutr9ORnXE75vt3dVN7LhaP7CY++ubd/rlfv96+3Yvbr16svNRLvf8I+X6Q7kR5nIj+ki5cRX/cbnD6ukJ23+k4MtxGWv/6QD7AzwfH2nPxkcTmjj0K2pJe0NvnX57ldqT1LrUXjDUzj6136S2Sm2T2tPEOUbRdcG6oTKjY8cJjRtq4Q7shXtwyLivwK1wDe6EPXgQJoSVNIcKLP5Qg8UfPFj8GNq68FuwE+7AqmEYwCwfjDY4a6Jtvct8tMGZjzZY/Bq+Ez/eMa4XpgaXa0Dbep/XjjZYmg6+F9/B9+I7+EF8Bz8Ufg/OXqENVg2etYe8drTB0uT29Y34Hn4jfoDfiB/gN+IHvGqzV2iDVUNg7a3WHtBspdnEA0H8Jh4M4jfwO/Eb+J34LV518qqlhk41tKy909pbNHtpdvB78Tv4vfgd/F58MuaVsXQ4KWOeXHnlCm2w1k7GvDKGtg2VvO07sGruB7D4ZCwoY2iDVUM8EJUrtMGal4wFZQxtcPYWbXCuGW0bXOajDS58alDGQtWDc/3MA841MA8418A8YOmTn6D8MM6GkGtjHFj6Dv0gfbIUlCXG2aBsMA6suchGUDYYB5Y+OQnKCeNs0L4zDqy52PegfWccWPpkIJQMxL1Tf/5jKf1kvmSDs4K9POypcpK8qoq3zKX7nc8/9iXUcIr/NZzifw3HFX+it6rfRW+LV9FbeeWjt8Ur1u61Fs/avbzyrN1rXzzz6r7m87AvIfpcfIs+F9+Ytym+Rc81bxM9Lx4yb9ojDteX6Yh9ntqQ2jYdvV080//mqc+dbMbemlRD/gv490f+J2tbYl98nvjr1Xzpj9dqsTTn+92b9Wbib/349c/Ts7Pt7m59y7ez/d3VtCvfeap6WpjfTHovfXxI+/Kg9T89aMUtqP7R49ZnuNc+Uc4Sd7kb5xfWvNtfri83WzKGd7GfA+nP/Z+9eg4Lcz39vn6/fjuZ1eID",
        },
        {
            "url": "https://puzz.link/p?heyawake/19/15/201480mhg2i40a8s192816704r503gk0m2g2oa0a18085010k046g0003hu0104000400fbvgvo005fu1800o0000000800600000003s0003c-1c140411g81ah8233",
            "config": {"fast_mode": True},
            "test": False,
        },
        {
            "data": "m=edit&p=7VPLbtswELzrKwKe9yCSkiXz5qZ2L677sIsgEIRAdpjaiA21spW2NPTvGa5YqIcARVEEzaEgOJhdDsnhY49f26qxlFNGOqeYJJpOFOk4oWQkucehrXanvTUXNGlP27oBIXo3m9FdtT/aqAiqMjq7sXETcm9MIaQgodClKMl9MGf31rgpuSWGBOXIzXuRAp0O9IrHPbvskzIGXwQOeg262TWbvb2Z95n3pnArEn6fVzzbU3GoH6wIPny8qQ/rnU+sqxMOc9zuvoSRY3tb37dBK8uO3KS3u3zCrh7setrb9ewJu/4Uz2x3XHYdrv0jDN+Ywnv/NNB8oEtzBi7MWagRpsocj81PI/TYxyGERrLymnHGqBhXWIicZnzNGDOmjHPWTLG+TLF2FgujsGI6Bpc9z7BJrgNX4EnQQJ/CBOfxDX/VZ6rnuQ56bHLFW10yJowjtpD5k/7RXfz9aX9rp1AjLqyhpc8bl1Ehlm1zV20s/sv09rO9WNTNodojWrSHtW1+xijXLhLfBfcCF0zJ/wr+RxXsnyB+aX/3pdlBNYmt/VF9q+6tKKNH",
            "config": {"fast_mode": True, "limit_border": 1},
        },
        {
            "url": "https://puzz.link/p?heyawake/12/12/00000o0003063cc0o00030000000008020080a4a92a02008020000-2811111111",
            "config": {"fast_mode": True, "limit_2x2": 1},
            "test": False,
        },
    ]
    parameters = {
        "fast_mode": {"name": "Fast Mode", "type": "checkbox", "default": False},
        "limit_border": {"name": "Border Limit", "type": "number", "default": 0},
        "limit_2x2": {"name": "2x2 Limit", "type": "number", "default": 0},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(avoid_same_color_adjacent(color="gray"))
        self.add_program_line(avoid_diamond_pattern(color="gray"))
        self.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))

            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

                    if puzzle.param["fast_mode"] and num > len(ar) // 4:
                        lmt_2x2 = int(puzzle.param["limit_2x2"])
                        lmt_border = int(puzzle.param["limit_border"])
                        self.add_program_line(area_border_simple(_id=i, ar=ar))
                        self.add_program_line(area_border_connected(_id=i, color="gray", adj_type="x"))
                        self.add_program_line(limit_area_2x2_rect(lmt_2x2, _id=i, color="gray"))
                        self.add_program_line(limit_border(lmt_border, ar, puzzle, _type=Direction.TOP, color="gray"))
                        self.add_program_line(limit_border(lmt_border, ar, puzzle, _type=Direction.BOTTOM, color="gray"))
                        self.add_program_line(limit_border(lmt_border, ar, puzzle, _type=Direction.LEFT, color="gray"))
                        self.add_program_line(limit_border(lmt_border, ar, puzzle, _type=Direction.RIGHT, color="gray"))

        for r in range(puzzle.row):
            borders_in_row = [c for c in range(1, puzzle.col) if Point(r, c, Direction.LEFT) in puzzle.edge]
            for i in range(len(borders_in_row) - 1):
                b1, b2 = borders_in_row[i], borders_in_row[i + 1]
                self.add_program_line(avoid_rect(1, b2 - b1 + 2, color="not gray", corner=(r, b1 - 1)))

        for c in range(puzzle.col):
            borders_in_col = [r for r in range(1, puzzle.row) if Point(r, c, Direction.TOP) in puzzle.edge]
            for i in range(len(borders_in_col) - 1):
                b1, b2 = borders_in_col[i], borders_in_col[i + 1]
                self.add_program_line(avoid_rect(b2 - b1 + 2, 1, color="not gray", corner=(b1 - 1, c)))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
