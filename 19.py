#!/usr/bin/env python3
import fileinput
import itertools
import numpy as np
from typing import Iterator, Optional, Set, Tuple

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 19

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'

DIM = 3
SCAN_DISTANCE = 1000
OVERLAP_REQUIRED = 12


def iterate_rotation_matrices() -> Iterator[np.ndarray]:
    for ixs in itertools.permutations(range(DIM), DIM):
        for vals in itertools.product((-1, +1), repeat=DIM):
            rot = np.zeros((DIM, DIM), dtype=int)
            for i, (j, val) in enumerate(zip(ixs, vals)):
                rot[i, j] = val
            if np.linalg.det(rot) == 1:
                yield rot
ROTATIONS = list(iterate_rotation_matrices())
assert len(ROTATIONS) == 24


# Very slow. Aren't there any optimization?
def coordinate_transform(beacons: Set[Tuple[int, int, int]], detection: np.ndarray) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Returns coordinate transformation such that transformed `detection` has at least OVERLAP_REQUIRED common points with `beacons`,
     if such transformation exists.
    """
    for rot in ROTATIONS:
        new_points = detection @ rot
        for p1 in beacons:
            p1 = np.array(p1)
            for p2 in new_points:
                # We assume that p1 in base coordinate system represents as p2 in local system.
                shift = p1 - p2
                new_points_restored = new_points + shift
                n_common_points = sum(tuple(p) in beacons for p in new_points_restored)
                # At least one common point (p2) always will be presented.
                assert n_common_points >= 1
                # It is possible that detection does not contain all points it should contain.
                # This case is ignored, therefore, this function may produce false positive results in some cases.
                if n_common_points >= OVERLAP_REQUIRED:
                    return rot, shift
    return None


def manhattan_distance(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> int:
    return sum(abs(xi1 - xi2) for (xi1, xi2) in zip(p1, p2))


scanners = []
last_scanner = []
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    if not line:
        continue
    elif line.startswith('---'):
        if last_scanner:
            scanners.append(np.array(last_scanner))
        last_scanner = []
    else:
        last_scanner.append(list(map(int, line.split(','))))
else:
    if last_scanner:
        scanners.append(np.array(last_scanner))

assert len(scanners) > 1

# Final coordinates are stored in tuples since np.ndarray is unhashable.
beacons: Set[Tuple[int, int, int]] = set(map(tuple, scanners[0]))
scanners_positions = [(0, 0, 0)]
del scanners[0]


while scanners:
    for i, detection in enumerate(scanners):
        transform = coordinate_transform(beacons, detection)
        if transform is not None:
            rotation, shift = transform
            detection_restored = detection @ rotation + shift
            for p in detection_restored:
                beacons.add(tuple(p))
            scanners_positions.append(tuple(shift))
            scanners[i] = None
            break
    # Cannot use `None in scanners` here since np.ndarray overloads __eq__ such that it returns array instead of bool.
    assert any(x is None for x in scanners), "Cannot locate some scanners"
    scanners = [detection for detection in scanners if detection is not None]

if EASY:
    print(len(beacons))
else:
    print(max(
        manhattan_distance(b1, b2)
        for b1 in scanners_positions
        for b2 in scanners_positions
    ))
