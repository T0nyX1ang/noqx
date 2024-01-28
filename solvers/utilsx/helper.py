"""Helper functions for generation solvers and rules."""

import itertools
from typing import Any, Set, Tuple, Dict

from .solution import ClingoSolver


def tag_encode(name: str, *data: Any) -> str:
    """Encode a valid tag predicate without spaces or hyphens."""
    tag_data = [name]
    for d in data:  # recommended data sequence: *_type, src_r, src_c, color
        tag_data.append(str(d).replace("-", "_").replace(" ", "_"))

    return "_".join(tag_data)


def canonicalize_shape(shape: Tuple[Tuple[int, int]]) -> Tuple[Tuple[int, int]]:
    """
    Given a (possibly non-canonical) shape representation,

    Return the canonical representation of the shape, a tuple:
        - in sorted order
        - whose first element is (0, 0)
        - whose other elements represent the offsets of the other cells from the first one
    """
    shape = sorted(shape)
    root_r, root_c = shape[0]
    dr, dc = -1 * root_r, -1 * root_c
    return tuple((r + dr, c + dc) for r, c in shape)


def get_variants(
    shape: Tuple[Tuple[int, int]], allow_rotations: bool, allow_reflections: bool
) -> Set[Tuple[Tuple[int, int]]]:
    """
    Get a set of canonical shape representations for a (possibly non-canonical) shape representation.

    allow_rotations = True iff shapes can be rotated
    allow_reflections = True iff shapes can be reflected
    """
    # build a set of functions that transform shapes
    # in the desired ways
    functions = set()
    if allow_rotations:
        functions.add(lambda shape: canonicalize_shape((-c, r) for r, c in shape))
    if allow_reflections:
        functions.add(lambda shape: canonicalize_shape((-r, c) for r, c in shape))

    # make a set of currently found shapes
    result = set()
    result.add(canonicalize_shape(shape))

    # apply our functions to the items in this set
    all_shapes_covered = False
    while not all_shapes_covered:
        new_shapes = set()
        current_num_shapes = len(result)
        for f, s in itertools.product(functions, result):
            new_shapes.add(f(s))
        result = result.union(new_shapes)
        all_shapes_covered = current_num_shapes == len(result)
    return result


def mark_and_extract_clues(
    solver: ClingoSolver,
    original_clues: Dict[Tuple[int, int], Any],
    shaded_color: str = "black",
    safe_color: str = "green",
) -> Dict[Tuple[int, int], int]:
    """
    Mark clues to the solver and extract the clues that are not color-relevant.

    Recommended to use it before performing a bfs on a grid.
    """
    clues = {}  # remove color-relevant clues here
    for (r, c), clue in original_clues.items():
        if isinstance(clue, list):
            if clue[1] == shaded_color:
                solver.add_program_line(f"{shaded_color}({r}, {c}).")
            elif clue[1] == safe_color:
                solver.add_program_line(f"not {shaded_color}({r}, {c}).")
            clues[(r, c)] = int(clue[0])
        elif clue == shaded_color:
            solver.add_program_line(f"{shaded_color}({r}, {c}).")
        elif clue == safe_color:
            solver.add_program_line(f"not {shaded_color}({r}, {c}).")
        else:
            clues[(r, c)] = int(clue)
    return clues
