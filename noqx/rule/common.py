"""Generate commonly used rules for the solver."""

from typing import Iterable, Optional, Tuple, Union

from noqx.puzzle import Direction
from noqx.rule.helper import target_encode


def display(item: str = "black", size: int = 2) -> str:
    """A rule for displaying an item with a certain size.

    * To display multiple items, call this function multiple times.

    Args:
        item: The item to be displayed.
        size: The arity of the item.
    """
    return f"#show {item}/{size}."


def defined(item: str, size: int = 2) -> str:
    """A rule for a defined item with a certain size.

    * A `defined` item is a declaration that the item exists in the program to avoid warnings.

    * To mark multiple items as defined, call this function multiple times.

    Note:
        Here is a rule to shade gray cells from a grid without black cells:
        ```
            { gray(R, C) } :- grid(R, C), not black(R, C).
        ```
        If there is no black cells in the puzzle, the solver may raise a warning that `black/2` is undefined.
        To avoid this warning, the `defined` rule can be applied.

    Args:
        item: The item to be defined.
        size: The arity of the item.
    """
    return f"#defined {item}/{size}."


def grid(rows: int, cols: int, with_holes: bool = False) -> str:
    """A rule for a grid with or without holes.

    * The starting coordinate is `(0, 0)`. The grid is extended from left to right, and from top to bottom.

    * The holes should be defined separately using their coordinates. Moreover, the mechanism for the holes is to delete the corresponding cells from the grid.

    * This function cannot be used to define multiple grids.

    Args:
        rows: The number of rows in the grid.
        cols: The number of columns in the grid.
        with_holes: Whether the grid contains holes.
    """
    if with_holes:
        return f"grid(R, C) :- R = 0..{rows - 1}, C = 0..{cols - 1}, not hole(R, C)."

    return f"grid(0..{rows - 1}, 0..{cols - 1})."


def area(_id: int, src_cells: Iterable[Tuple[int, int]]) -> str:
    """A rule for an area with several cells.

    * The area may not be contiguous, but it is strongly suggested to call the `full_bfs` function before defining an area to get all the connected regions in a grid.

    * The area is identified by `_id` parameter, to define multiple areas, make sure their IDs are different.

    Args:
        _id: The unique ID of the area.
        src_cells: The cells belonging to the area.
    """
    return "\n".join(f"area({_id}, {r}, {c})." for r, c in src_cells)


def shade_c(color: str = "black") -> str:
    """A rule to shade cells with a specified color from a grid.

    * Every cell in the grid can be either shaded or unshaded with the `color`.

    * In general, the color does not need to be a **real color**, it can be any label representing a certain state, such as symbols used in specific puzzles.

    Args:
        color: The color to be shaded.
    """
    return f"{{ {color}(R, C) }} :- grid(R, C)."


def shade_cc(colors: Iterable[str]) -> str:
    """A rule to shade cells with several specified colors from a grid.

    * Every cell in the grid can be shaded with **exactly one** of the specified colors.

    * Similar to `shade_c`, the specified colors do not need to be a **real color**.

    Args:
        colors: The colors to be shaded.

    Warning:
        If you only specify **one color**, all the cells in the grid will be shaded with this color.
    """
    return f"{{ {'; '.join(str(c) + '(R, C)' for c in colors)} }} = 1 :- grid(R, C)."


def invert_c(color: str = "black", invert: str = "white") -> str:
    """A rule to define an inverted color from a specified color inside a grid.

    * An inverted color means that if a cell is not shaded with the specified color,
    it will be shaded with the inverted color.

    * This rule is redundant in many cases, as [Clingo](https://potassco.org/clingo/) supports negation directly. However, the negation may behave unexpectedly in some complex rules, so this rule is provided to define the inverted color explicitly.

    * This rule can be called multiple times to define multiple inverted colors. Please make sure there are no conflicts between different inverted colors.

    * Similar to `shade_c`, the specified color and the inverted color do not need to be a **real color**.

    Args:
        color: The specified color.
        invert: The inverted color.
    """
    return f"{invert}(R, C) :- grid(R, C), not {color}(R, C)."


def edge(rows: int, cols: int) -> str:
    """A rule for drawing edges around a cell.

    * `edge(R, C, "left")` represents the left edge of the cell `(R, C)`, and `edge(R, C, "top")` represents the top edge of the cell `(R, C)`.

    * The outside border of a grid is automatically drawn. However, if there are holes in the grid, the edges around the holes need to be drawn manually.

    Note:
        Assume there is a hole at `(r, c)`. To define edges around this hole, some additional codes should be written. Moreover, if there are another hole adjacent to this hole, the shared edge should not be drawn.
        ```python
            rule = ""
            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if ((r1, c1) in hole) else ""  # the "hole" part should be implemented by some criteria
                d = Direction.LEFT if c1 != c else Direction.TOP
                rule += f'{prefix}edge({r2}, {c2}, "{d}").\n'
        ```

    Args:
        rows: The number of rows in the grid.
        cols: The number of columns in the grid.
    """
    fact = f"vertical_range(0..{rows - 1}, 0..{cols}).\n"
    fact += f"horizontal_range(0..{rows}, 0..{cols - 1}).\n"
    fact += f'{{ edge(R, C, "{Direction.LEFT}") }} :- vertical_range(R, C).\n'
    fact += f'{{ edge(R, C, "{Direction.TOP}") }} :- horizontal_range(R, C).\n'
    fact += f'edge(0..{rows - 1}, 0, "{Direction.LEFT}").\n'
    fact += f'edge(0..{rows - 1}, {cols}, "{Direction.LEFT}").\n'
    fact += f'edge(0, 0..{cols - 1}, "{Direction.TOP}").\n'
    fact += f'edge({rows}, 0..{cols - 1}, "{Direction.TOP}").'
    return fact


def direction(directions: Union[str, list]) -> str:
    """A rule for all possible directions.

    Args:
        directions: The directions to be defined, can be specified either as a string or as a list of strings.

    Warning:
        In [Clingo](https://potassco.org/clingo/), constant strings should be enclosed in double quotes. Hence, please take care of the direction string while writing a direction-relevant rule.
    """
    format_d = map(lambda x: f'"{x}"', tuple(directions))
    return f"direction({';'.join(format_d)})."


def fill_line(color: str = "black", directed: bool = False) -> str:
    """A rule for filling a line with a specified color in a grid.

    * To fill a line on a grid, two steps should be taken: shade the cells that have a line at first, and then decide which directions to take for each cell. This rule helps to complete the **second** step. So before using this rule, at least one shading rule should be defined.

    * If the line is undirected, only one predicate (`line_io`) is used to represent the directions. Once the line is direction, two predicates (`line_in` and `line_out`) are used to represent the directions.

    Args:
        color: The specified color that the line can be drawn on.
        directed: Whether the line is directed.
    """
    if directed:
        rule = f"{{ line_in(R, C, D): direction(D) }} <= 1 :- grid(R, C), {color}(R, C).\n"
        rule += f"{{ line_out(R, C, D): direction(D) }} <= 1 :- grid(R, C), {color}(R, C)."
    else:
        rule = f"{{ line_io(R, C, D): direction(D) }} :- grid(R, C), {color}(R, C)."

    return rule


def fill_num(_range: Iterable[int], _type: str = "grid", _id: Optional[int] = None, color: Optional[str] = None) -> str:
    """A rule for filling specified numbers in a grid or an area.

    * Filling numbers is similar to shading multiple colors in `shade_cc` rule, and the difference is that the candidate number set is usually larger than the candidate color set. Meanwhile, the candidate number set can be more flexible.

    * The range is converted to the format `low..high` or `x;y;z` for a list of numbers in compliance with [Clingo](https://potassco.org/clingo/) syntax. According to the performance tests in several puzzles, it is recommended to **use continuous ranges** as much as possible.

    Args:
        _range: The range of numbers to be filled.
        _type: Acceptable region types, can be either `grid` or `area`.
        _id: The ID of the area, only used when `_type` is `area`. Ignored when `_type` is `grid`.
        color: The numbers **won't be filled in cells with the specified color**.

    Raises:
        ValueError: If the `_type` is other than `grid` or `area`.

    Warning:
        The `color` parameter is not intuitive in the current stage, please be cautious while using it.
    """
    color_part = "" if color is None else f"; {color}(R, C)"

    _range = sorted(set(_range))  # canonicize the range
    i, range_seq = 0, []

    while i < len(_range):
        start = i
        while i < len(_range) - 1 and _range[i + 1] - _range[i] == 1:
            i += 1
        end = i
        if start < end:
            range_seq.append(f"{_range[start]}..{_range[end]}")
        else:
            range_seq.append(str(_range[start]))
        i += 1

    range_str = f"{';'.join(range_seq)}"

    if _type == "grid":
        return f"{{ number(R, C, ({range_str})){color_part} }} = 1 :- grid(R, C)."

    if _type == "area" and _id is not None:
        return f"{{ number(R, C, ({range_str})){color_part} }} = 1 :- area({_id}, R, C)."

    raise ValueError("Invalid type, must be one of 'grid', 'area'.")


def unique_num(color: str = "black", _type: str = "row") -> str:
    """A rule to check the uniqueness of the numbers in every row, column or area.

    * This rule is usually used together with the `fill_num` rule to ensure that the filled numbers are unique in *every* row, column or area.

    Args:
        color: The uniqueness of the numbers **won't be checked with the specified color**.
        _type: Acceptable region types, can be either `row`, `col` or `area`.

    Raises:
        ValueError: If the `_type` is other than `row`, `col` or `area`.

    Warning:
        The `color` parameter is not intuitive in the current stage, please be cautious while using it.
    """
    if _type == "row":
        return f":- grid(_, C), number(_, _, N), {{ {color}(R, C) : number(R, C, N) }} > 1."

    if _type == "col":
        return f":- grid(R, _), number(_, _, N), {{ {color}(R, C) : number(R, C, N) }} > 1."

    if _type == "area":
        return f":- area(A, _, _), number(_, _, N), {{ {color}(R, C) : area(A, R, C), number(R, C, N) }} > 1."

    raise ValueError("Invalid type, must be one of 'row', 'col', 'area'.")


def count(
    target: Union[int, Tuple[str, int]], color: str = "black", _type: str = "grid", _id: Optional[Union[int, str]] = None
) -> str:
    """A rule to compare the number of colored cells in a grid, row, column or area to a specified target.

    * Counting is one of the most commonly used constraints in logic puzzles, so this rule is designed for a wide range of use cases.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison. Available operators are detailed in the `noqx.helper.reverse_op` and `noqx.helper.target_encode` function.
        color: The specified color.
        _type: Acceptable region types, can be either `grid`, `row`, `col` or `area`.
        _id: The ID of the `area`, or the index of the `row` (from top to bottom) or `col` (from left to right). If `_id` is set to `None`, this rule will compare the colored cells in every row or column instead. Also ignored when `_type` is set to `grid`.

    Raises:
        ValueError: If the `_type` is other than `grid`, `row`, `col` or `area`.
    """
    rop, num = target_encode(target)

    if _id is None:
        _id = "R" if _type == "row" else "C" if _type == "col" else None

    if _type == "grid":
        return f":- #count {{ grid(R, C) : {color}(R, C) }} {rop} {num}."

    if _type == "row":
        return f":- grid({_id}, _), #count {{ C : {color}({_id}, C) }} {rop} {num}."

    if _type == "col":
        return f":- grid(_, {_id}), #count {{ R : {color}(R, {_id}) }} {rop} {num}."

    if _type == "area":
        return f":- #count {{ R, C : area({_id}, R, C), {color}(R, C) }} {rop} {num}."

    raise ValueError("Invalid type, must be one of 'grid', 'row', 'col', 'area'.")
