"""Utility for shapes."""

import itertools
from typing import Set, Tuple

OMINOES = {
    4: {
        "T": ((0, 0), (1, 0), (1, 1), (2, 0)),
        "O": ((0, 0), (0, 1), (1, 0), (1, 1)),
        "I": ((0, 0), (1, 0), (2, 0), (3, 0)),
        "L": ((0, 0), (1, 0), (2, 0), (2, 1)),
        "S": ((0, 0), (0, 1), (1, 1), (1, 2)),
    },
    5: {
        "F": ((0, 0), (0, 1), (1, -1), (1, 0), (2, 0)),
        "I": ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)),
        "L": ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1)),
        "N": ((0, 0), (0, 1), (1, 1), (1, 2), (1, 3)),
        "P": ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0)),
        "T": ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1)),
        "U": ((0, 0), (0, 2), (1, 0), (1, 1), (1, 2)),
        "V": ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
        "W": ((0, 0), (0, 1), (1, 1), (1, 2), (2, 2)),
        "X": ((0, 0), (1, -1), (1, 0), (1, 1), (2, 0)),
        "Y": ((0, 0), (1, -1), (1, 0), (1, 1), (1, 2)),
        "Z": ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2)),
    },
}


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


def rotate(shape: Tuple[Tuple[int, int]]) -> Tuple[Tuple[int, int]]:
    """Rotate a shape 90 degrees."""
    return canonicalize_shape((-c, r) for r, c in shape)


def reflect(shape: Tuple[Tuple[int, int]]) -> Tuple[Tuple[int, int]]:
    """Reflect a shape vertically."""
    return canonicalize_shape((-r, c) for r, c in shape)


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
        functions.add(rotate)
    if allow_reflections:
        functions.add(reflect)

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
