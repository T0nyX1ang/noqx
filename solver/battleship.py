"""The Battleship self."""

from typing import Dict

from noqx.manager import Solver
from noqx.puzzle import Point, Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import all_shapes, count_shape, general_shape, parse_shapeset


def avoid_battleship_adjacent(color: str = "black", adj_type: str = "x"):
    """Generate a rule to avoid adjacent ships."""
    t_om = tag_encode("shape_origin_map", "battleship", color)
    return f":- adj_{adj_type}(R, C, R1, C1), {t_om}(R, C, R2, C2), {t_om}(R1, C1, R3, C3), (R2, C2) != (R3, C3)."


def line_fleet_counts(shapeset):
    """Return ship counts by length if every fleet shape is a straight line."""
    result = {}
    for shape, shape_count in shapeset.items():
        rows = {r for r, _ in shape}
        cols = {c for _, c in shape}
        if len(rows) == 1:
            length = len(cols)
        elif len(cols) == 1:
            length = len(rows)
        else:
            return None

        result.setdefault(length, 0)
        result[length] += shape_count

    return result


def line_fleet(fleet_name: str, fleet_counts):
    """Generate explicit run-count rules for straight battleship fleets."""
    max_length = max(fleet_counts)
    rule = ""

    rule += f":- {fleet_name}(R, C), {fleet_name}(R + 1, C + 1).\n"
    rule += f":- {fleet_name}(R + 1, C), {fleet_name}(R, C + 1).\n"
    rule += f":- {', '.join(f'{fleet_name}(R, C + {i})' for i in range(max_length + 1))}.\n"
    rule += f":- {', '.join(f'{fleet_name}(R + {i}, C)' for i in range(max_length + 1))}.\n"

    rule += (
        f"ship_run(1, R, C) :- {fleet_name}(R, C), not {fleet_name}(R - 1, C), not {fleet_name}(R + 1, C), "
        f"not {fleet_name}(R, C - 1), not {fleet_name}(R, C + 1).\n"
    )
    for length in range(2, max_length + 1):
        horizontal = [f"{fleet_name}(R, C)", f"not {fleet_name}(R, C - 1)", f"not {fleet_name}(R, C + {length})"]
        horizontal.extend(f"{fleet_name}(R, C + {i})" for i in range(1, length))
        vertical = [f"{fleet_name}(R, C)", f"not {fleet_name}(R - 1, C)", f"not {fleet_name}(R + {length}, C)"]
        vertical.extend(f"{fleet_name}(R + {i}, C)" for i in range(1, length))

        rule += f"ship_run({length}, R, C) :- {', '.join(horizontal)}.\n"
        rule += f"ship_run({length}, R, C) :- {', '.join(vertical)}.\n"

    for length in range(1, max_length + 1):
        rule += f":- #count {{ R, C : ship_run({length}, R, C) }} != {fleet_counts.get(length, 0)}.\n"

    return rule.strip()


def remaining_ship_cells(
    fleet_name: str, fleet_total: int, puzzle: Puzzle, row_clues: Dict[int, int], col_clues: Dict[int, int]
):
    """Generate redundant remaining-cell counts for unclued rows and columns."""
    rules = ""
    open_rows = tuple(r for r in range(puzzle.row) if r not in row_clues)
    open_cols = tuple(c for c in range(puzzle.col) if c not in col_clues)

    if open_rows:
        rules += f"open_row({';'.join(str(r) for r in open_rows)}).\n"
        rules += f":- #count {{ R, C : {fleet_name}(R, C), open_row(R) }} != {fleet_total - sum(row_clues.values())}.\n"

    if open_cols:
        rules += f"open_col({';'.join(str(c) for c in open_cols)}).\n"
        rules += f":- #count {{ R, C : {fleet_name}(R, C), open_col(C) }} != {fleet_total - sum(col_clues.values())}.\n"

    return rules.strip()


class BattleshipSolver(Solver):
    """The Battleship solver."""

    name = "Battleship"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VbNattAEL77KcKe57CrXf1YNyeNe0mVNnYJRhgjpyo2lZArW6Ws8btnZqREqiIoKSRtoNg7jL75dnb+vPL+e5WUKShFXx2ABNTAuB4vpRxesvnMt4csDc9gUh02RYkKwPV0Cl+TbJ/CKFa8XS5HRzsO7QTs+zAWSoBwcCmxBPspPNoPoY3AztAkQCF2VZMcVC9b9ZbtpF3UoJKoR40O4obcLfBxnRwwqP1mu1ud1w4/hrGdgyDCOXshVeTFj1Q08dDzXZGvtwS0DhrLvvpSfKsaLjoUeZUdtndFVpQEEnYCO6lTWQykottUSK1TIW0gFef1UhkPp3LCdt1gMqswprw+t2rQqrPwiDIKj0Jr2qm5CdRToc1DqR4AlwDs+SPg9QGfANkBAgJMBxj3thjZO8WoXhzG6W/hUzpOvT7DZ0bH6ZgZncCUZEpnj3KY03Gr6nQ6bpTbP0l5TzgBcx4TwPIqLvICi+wS24WnEyE8qqU3ZFGSaqYHTQ6ZcNQGTFx6M2gKqNX+oGlM1cfA+yaMf8pZOCznOD1gNct3LCVLl+UVcy5Z3rK8YGlYeszxaf6eNaHdQr5QOLEJ+J789YP35VvDlqNYRFW+TsuzqCjzJMN7Y7ZJdqnAS/w0Ej8FL5wqfCn8v9ff2L1OrZP/2m/nN+HEWHn8ddlrELtqlawwJ4F/KeBPcK2fg0dg/L9zLuL8IsCZ4VfDEKG/8dXbhrfecnQP",
            "config": {"shapeset": "ship4"},
        },
        {
            "data": "m=edit&p=7VVLa9tAEL7rV5S9dg6a1etxc9yklzR92CUYIYLiKljURqkllbLG/z0zIxtVRXsIlJJAkXf8zX67o3ntqvnRFfsSEPnnxeACIfCDUAailuGenmXVbsv0Dcy6dlPvCQB8vLqCh2LblOBkKNvd3DmYJDUzMO/TTKECpWmgysF8Tg/mQ2pWYBZEKcAc1K7bttW63tZ7dZ4z1/1GTfBygLfCM5r3k+gSvjlhgiuC90VLTjab6vHu4m0//SnNzBIUO3AhJhiqXf2z5Deyg6yv6919xRODBQUeEU33rf7enZZifgQze14YZOQcBsM+DEYTYXB0/yCMJD8eqUxfKJC7NOOYvg4wHuAiPZC8SQ/K82grN4dUUnk+qcGgxqT6g5qQys3Qq747Yn0k1RvUaGQq1KPFqP/QPV4+OIIB84M1DJk/6+Q8SggrCsFnJyMY5bYvXhAQo8dMn3UV9OamqJB3TdoLrW+KODOTTMxZmWSS0Magy5mdptBOaS4eJWgiJtQcrz/NeXaTUmILxW+bpgJrNjC0pgMjrriFspYEE8suao4lNTsYT+Q7ka7IQOS1NNClyFuRc5G+yFDWRHxcnnWgfu/Mv+hC5sdyhY8fuspf21zuZGrR7R+KdUk322JTPPL/vN491k3Vloq+MkdH/VIy6IBquuT+f3hex4eHS+a+hNPyElygM5s7Tw==",
            "config": {
                "shapeset": [
                    {"shape": "111|101|001|011|010", "count": 3},
                    {"shape": "1|1", "count": 3},
                ]
            },
        },
        {
            "data": "m=edit&p=7VRtT+JAEP7Or7jsVze5bluxNLkPFcHTQ0SBcJY0pOAC1Zblti16Jfx3Z7dqX6gmd4mJl1yWHZ55Zl9mdrtP+Ct2OcVEET/NwPAPTSeG7KpRl115bgMv8qn5BVtxtGQcAMaX7Taeu35I8fnNstNk1sOJ9XNjRLZNTpX4TBndte8OroMfZ57GSbtr9C56F566sL43j6/qrYN6Lw6HEd1cBeT4bmgP5r3RoqH+bnVtPbEvlcNze/51Yw2/1cZE5qY4tW3SMBMLJ6fmGBGEkQqdIAcnV+Y2uTDRjAVTD+GkD3GEiYNREPuRN2M+4+iFSzrpbBVgK4MjGReomZJEAdx9xgBvAM48PvPppJMyPXOcDDASCRzL2QKigG2o2EwkKPw0KSCmbgRnGC69NcIaBML4lt3Hz0OJs8OJ9RdlwEovZQiYliFQRRmiuo8to+HsdnBN11DIxByLmoYZNDLYN7dgu+YWaRpMrcP9yptEmgGulrkNcA9f3SMVXP3VNeqFwUQVk7Mw0fPDYT8id72RdgCJ4EST9kRaRdpDaTtyTEvakbRNaXVp63LMkSjlj4r9oBTGujihYhMn+okYpzZG/ZjP3RmF76m/dNfiv8mCNQu9iCJ42yhk/iRMx0zoozuLkJnKSz5S4FZxMKXwJHKUz9ja91ZVK7yECqS3WDFOK0OCpLeLt5YSoYqlpozflnJ6cH2/WIuU3gKVPskCFXF4bznf5Zw9FJjAjZYFIvc2CyvRVekwI7eYonvvlnYLsuPY1dAjkh0em4r1/0L8jwixuDLlMyjUZ0hBftWMvyMxWbBMVwgNsO9oTS5axb8hK7lomd/TEJHsvowAW6EkwJbFBKh9PQFyT1KAe0NVxKplYRFZlbVFbLUnL2KrvMIUPmen9gQ=",
            "config": {"shapeset": "ship5"},
        },
        {
            "url": "https://puzz.link/p?battleship/10/10/13h44i121h44i2zw6m0n0m5zw//d",
            "config": {"shapeset": "ship4"},
            "test": False,
        },
        {
            "url": "https://puzz.link/p?battleship/15/15/7i8g2i7h5529g21h5g1j7000j0j0000k000k00l0l0j0k0m000i000m0k0k0k0k0g000i000i000g0k0k0k0k0m000i000m0k0j0l0l00k000k0000j0j000//p",
            "config": {"shapeset": "pento"},
            "test": False,
        },
    ]
    parameters = {
        "shapeset": {
            "name": "Shape Set",
            "type": "shapeset",
            "default": [],
            "presets": ["ship3", "ship4", "ship5", "pento"],
        },
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))

        fleet_name = "battleship_B"  # set a default battleship fleet name
        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            shape, style = symbol_name.split("__")
            if shape[-1] == "+":
                shape = shape[:-1]
                style = f"-{style}"

            validate_direction(r, c, d)
            fail_false(shape.startswith("battleship"), f"Invalid battleship shape: {shape}.")
            fail_false(fleet_name in ("", shape), "Multiple fleet shapes are not allowed.")

            fleet_name = shape
            if style not in ("7", "8"):
                self.add_program_line(f"{fleet_name}({r}, {c}).")
            else:
                self.add_program_line(f"not {fleet_name}({r}, {c}).")

            if style == "1":
                self.add_program_line(f":- grid({r + 1}, {c}), {fleet_name}({r + 1}, {c}).")
                self.add_program_line(f":- grid({r - 1}, {c}), {fleet_name}({r - 1}, {c}).")
                self.add_program_line(f":- grid({r}, {c + 1}), {fleet_name}({r}, {c + 1}).")
                self.add_program_line(f":- grid({r}, {c - 1}), {fleet_name}({r}, {c - 1}).")

            if style == "2":
                fail_false(0 < c < puzzle.col - 1 and 0 < r < puzzle.row - 1, f"Ship at ({r}, {c}) is outside of the board.")
                self.add_program_line(f":- #count {{ R, C: {fleet_name}(R, C), adj_4({r}, {c}, R, C) }} != 2.")

            if style in ("3", "-1", "-2"):
                fail_false(c < puzzle.col - 1, f"Ship at ({r}, {c}) is outside of the board.")
                self.add_program_line(f":- grid({r}, {c - 1}), {fleet_name}({r}, {c - 1}).")
                self.add_program_line(f":- grid({r}, {c + 1}), not {fleet_name}({r}, {c + 1}).")

            if style in ("4", "-2", "-3"):
                fail_false(r < puzzle.row - 1, f"Ship at ({r}, {c}) is outside of the board.")
                self.add_program_line(f":- grid({r - 1}, {c}), {fleet_name}({r - 1}, {c}).")
                self.add_program_line(f":- grid({r + 1}, {c}), not {fleet_name}({r + 1}, {c}).")

            if style in ("5", "-3", "-4"):
                fail_false(c > 0, f"Ship at ({r}, {c}) is outside of the board.")
                self.add_program_line(f":- grid({r}, {c + 1}), {fleet_name}({r}, {c + 1}).")
                self.add_program_line(f":- grid({r}, {c - 1}), not {fleet_name}({r}, {c - 1}).")

            if style in ("6", "-1", "-4"):
                fail_false(r > 0, f"Ship at ({r}, {c}) is outside of the board.")
                self.add_program_line(f":- grid({r + 1}, {c}), {fleet_name}({r + 1}, {c}).")
                self.add_program_line(f":- grid({r - 1}, {c}), not {fleet_name}({r - 1}, {c}).")

        shapeset = parse_shapeset(puzzle.param["shapeset"])
        fleet_counts = line_fleet_counts(shapeset)
        use_line_fleet = fleet_counts is not None

        self.add_program_line(shade_c(color=fleet_name))
        if use_line_fleet:
            if puzzle.symbol:
                self.add_program_line(adjacent(_type=4))
            self.add_program_line(line_fleet(fleet_name, fleet_counts))
        else:
            self.add_program_line(adjacent(_type=4))
            self.add_program_line(adjacent(_type="x"))
            self.add_program_line(avoid_battleship_adjacent(color=fleet_name, adj_type="x"))
            self.add_program_line(all_shapes("battleship", color=fleet_name))

            for i, (o_shape, o_count) in enumerate(shapeset.items()):
                self.add_program_line(
                    general_shape("battleship", i, o_shape, color=fleet_name, adj_type=4, add_origin_map=True)
                )
                self.add_program_line(count_shape(o_count, name="battleship", _id=i, color=fleet_name))

        row_clues: Dict[int, int] = {}
        col_clues: Dict[int, int] = {}
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
                col_clues[c] = num
                self.add_program_line(count(num, color=fleet_name, _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
                row_clues[r] = num
                self.add_program_line(count(num, color=fleet_name, _type="row", _id=r))

        if use_line_fleet:
            self.add_program_line(
                remaining_ship_cells(
                    fleet_name, sum(length * count for length, count in fleet_counts.items()), puzzle, row_clues, col_clues
                )
            )

        self.add_program_line(display(item=fleet_name))

        return self.program

    def refine(self, solution: Puzzle) -> None:
        """Refine the solution."""
        for (r, c, d, label), _ in solution.symbol.items():
            has_top_neighbor = (r - 1, c, d, label) in solution.symbol
            has_left_neighbor = (r, c - 1, d, label) in solution.symbol
            has_bottom_neighbor = (r + 1, c, d, label) in solution.symbol
            has_right_neighbor = (r, c + 1, d, label) in solution.symbol

            fleet_name = solution.symbol[Point(r, c, d, label)].split("__")[0].replace("+", "")

            # center part
            if {has_top_neighbor, has_bottom_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__1"

            # middle part
            elif (has_top_neighbor and has_bottom_neighbor) or (has_left_neighbor and has_right_neighbor):
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__2"

            # left part
            if {has_top_neighbor, has_bottom_neighbor, has_left_neighbor, not has_right_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__3"

            # top part
            if {has_top_neighbor, has_left_neighbor, has_right_neighbor, not has_bottom_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__4"

            # right part
            if {has_top_neighbor, has_bottom_neighbor, has_right_neighbor, not has_left_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__5"

            # bottom part
            if {has_bottom_neighbor, has_left_neighbor, has_right_neighbor, not has_top_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__6"

            # left-top part
            if {has_top_neighbor, has_left_neighbor, not has_bottom_neighbor, not has_right_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}+__2"

            # right-top part
            if {has_top_neighbor, has_right_neighbor, not has_bottom_neighbor, not has_left_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}+__3"

            # left-bottom part
            if {has_bottom_neighbor, has_left_neighbor, not has_top_neighbor, not has_right_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}+__1"

            # right-bottom part
            if {has_bottom_neighbor, has_right_neighbor, not has_top_neighbor, not has_left_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}+__4"
