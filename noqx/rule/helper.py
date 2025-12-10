"""Helper functions for generating rules and validating data."""

import random
from collections import deque
from typing import Dict, Iterable, Iterator, Optional, Tuple, Union

from noqx.puzzle import Direction, Point


def tag_encode(name: str, *data: Union[str, int, None]) -> str:
    """Encode a valid tag predicate without spaces or hyphens.

    * Since there are many predicates in the solver, this function aims to generate consistent tags.
    This helps avoid errors due to inconsistent naming conventions.

    * To ensure compatibility with [Clingo](https://potassco.org/clingo/), all spaces and hyphens
    in the tag are replaced with underscores.

    Args:
        name: The name of the tag.
        *data: Additional data to be included in the tag. The recommended data sequence is `base` type,
              `region` type, `auxiliary` type, `adjacent` type and `color`. Moreover, `None` values are ignored.

    Example:
        Here is an example of generating a tag for four-way reachability for black cells in a grid:
        ```python
            from noqx.rule.helper import tag_encode
            tag = tag_encode("reachable", "grid", None, "adj", 4, "black")
        ```
    """
    tag_data = [name]
    for d in data:  # recommended data sequence: *_type, src_r, src_c, color
        if d is not None:
            tag_data.append(str(d).replace("-", "_").replace(" ", "_"))

    return "_".join(tag_data)


def reverse_op(op: str) -> str:
    """Get the reverse symbolic representation of the given operator.

    * In [Clingo](https://potassco.org/clingo/), all the **constraints** are represented in a double-negation form.
    For example, the constraint `X >= 3` is represented as `:- X < 3.` in the solver. This function aims to do the
    reversion in comparison-relevant cases.

    * In most cases, this function does not need to be called, otherwise, the `target_encode` function is more
    frequently used.

    Args:
        op: The operator to be reversed. Available operators are: `eq`, `ge`, `gt`, `le`, `lt`, `ne`.

    Example:
        Here is a function from the Tatamibari puzzle, which should include a manual rule to compare the
        height and the width of a rectangle.
        ```python
            from noqx.rule.helper import reverse_op, tag_encode

            def tatamibari_cell_constraint(op: str, src_cell: Tuple[int, int]) -> str:
                tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
                rop = reverse_op(op)

                src_r, src_c = src_cell
                count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
                count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

                return f":- {count_r}, {count_c}, CR {rop} CC."
        ```
    """
    op_rev_dict = {"eq": "!=", "ge": "<", "gt": "<=", "le": ">", "lt": ">=", "ne": "="}
    return op_rev_dict[op]


def target_encode(target: Union[int, Tuple[str, int]]) -> Tuple[str, int]:
    """Encode a target number or a tuple of (`operator`, `number`) to a compatible format.

    * This function is recommended to be used when generating comparison constraints manually.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
                If the number is provided only, the `equivalent` operator is assumed.

    Example:
        `noqx.common.count` in the common rules is a good example to start with.
    """
    if isinstance(target, int):
        return ("!=", target)

    return (reverse_op(target[0]), target[1])


def validate_type(_type: Optional[Union[int, str]], target_type: Union[int, str, Iterable[Union[int, str]]]):
    """Validate the adjacency type, region type, label type and symbol type against the target type.

    * This function works like an assertion, but the error can be raised in production environments.

    Args:
        _type: The type to be validated.
        target_type: The target type or a list of acceptable types.

    Raises:
        ValueError: If the type does not match the target.

    Example:
        Here is an example to validate the adjacency type of a cell:
        ```python
            from noqx.rule.helper import validate_type

            validate_type(adj_type, (4, 8, "x"))
        ```

    Example:
        Here is an example to validate the label type of a cell:
        ```python
            from noqx.rule.helper import validate_type

            validate_type(label, "normal")
        ```
    """
    if _type is None:
        raise ValueError("Type cannot be 'None'.")

    if isinstance(target_type, (int, str)) and _type != target_type:
        raise ValueError(f"Invalid type '{_type}'.")

    if not isinstance(target_type, (int, str)) and _type not in target_type:
        raise ValueError(f"Invalid type '{_type}'.")


def validate_direction(r: int, c: int, d: Optional[str], target: str = Direction.CENTER):
    """Validate the direction of an element.

    * This function works like an assertion, but the error can be raised in production environments.

    Args:
        r: The row of the element.
        c: The column of the element.
        d: The direction of the element.
        target: The target direction to be validated against.

    Raises:
        ValueError: If the direction does not match the target.

    Example:
        Here is an example to validate the element `(2, 3)` is placed in the left:
        ```python
            from noqx.rule.helper import validate_direction
            from noqx.puzzle import Direction

            validate_direction(2, 3, Direction.LEFT)
        ```
    """
    if d != target:
        raise ValueError(f"The element in ({r}, {c}) should be placed in the {target}.")


def fail_false(expr: bool, msg: str):
    """Raise error if the expression is false.

    * This function works like an assertion, but the error can be raised in production environments.

    Args:
        expr: The boolean expression to be evaluated.
        msg: The error message to be raised if the expression is false.

    Raises:
        ValueError: If the expression is false.

    Example:
        Here is an example to check the color at `(2, 3)` is black:
        ```python
            from noqx.rule.helper import fail_false
            from noqx.puzzle import Point, Direction
            color = puzzle.surface.get(Point(2, 3, Direction.CENTER))
            fail_false(color == "black", "The cell at (2, 3) should be black.")
        ```
    """
    if expr is False:
        raise ValueError(msg)


def full_bfs(
    rows: int,
    cols: int,
    edges: Dict[Tuple[int, int, str, str], bool],
    clues: Optional[Dict[Tuple[int, int, str, str], Union[int, str]]] = None,
    exclude: Optional[Iterable[Tuple[int, int]]] = None,
) -> Dict[Tuple[Tuple[int, int], ...], Optional[Tuple[int, int]]]:
    """Generate a dictionary of connected components (rooms) with their unique clue by BFS.

    * The rooms will be converted to a tuple and become the key of the result dictionary.
    This ensures the consistency of the data structure.

    Args:
        rows: The number of rows in the grid.
        cols: The number of columns in the grid.
        edges: The edges of the grid stored in a dictionary, the format is the same to the `edge` attribute
               in the `Puzzle` class.
        clues: The clues in the grid stored in a dictionary, the format is the same to the `text` attribute
               in the `Puzzle` class.
        exclude: The cells to be excluded from the BFS.

    Example:
        Here is an example to get all the rooms in a grid with clues:
        ```python
            from noqx.rule.helper import full_bfs

            rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        ```
    """
    excluded_cells = set() if exclude is None else set(exclude)
    unexplored_cells = {(r, c) for c in range(cols) for r in range(rows) if (r, c) not in excluded_cells}
    clue_to_room: Dict[Tuple[Tuple[int, int], ...], Optional[Tuple[int, int]]] = {}
    rc_set = {(r, c) for (r, c, _, _) in clues} if clues else set()

    def get_neighbors(r: int, c: int) -> Iterator[Tuple[int, int]]:
        """Get the neighbors of a cell."""
        if edges.get(Point(r, c, Direction.LEFT)) is not True:
            yield (r, c - 1)

        if edges.get(Point(r, c + 1, Direction.LEFT)) is not True:
            yield (r, c + 1)

        if edges.get(Point(r, c, Direction.TOP)) is not True:
            yield (r - 1, c)

        if edges.get(Point(r + 1, c, Direction.TOP)) is not True:
            yield (r + 1, c)

    def single_bfs(start_cell: Tuple[int, int]) -> Tuple[Union[Tuple[int, int], None], Tuple[Tuple[int, int], ...]]:
        clue_cell = None
        connected_component = {start_cell}
        unexplored_cells.remove(start_cell)

        queue = deque([start_cell], rows * cols)  # make a deque for BFS
        while queue:
            r, c = queue.popleft()
            for neighbor in get_neighbors(r, c):
                if neighbor in unexplored_cells:
                    connected_component.add(neighbor)
                    unexplored_cells.remove(neighbor)
                    queue.append(neighbor)

            if clues and (r, c) in rc_set:
                clue_cell = (r, c)

        return clue_cell, tuple(connected_component)

    while len(unexplored_cells) != 0:
        start_cell = random.choice(tuple(unexplored_cells))  # get a random start cell
        clue, room = single_bfs(start_cell)
        clue_to_room[room] = clue

    return clue_to_room
