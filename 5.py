#!/usr/bin/env python3
from collections import defaultdict
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 5

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


covers = defaultdict(int)
for line in fileinput.input(INPUT_FILE):
    data = line.split()
    x1, y1 = map(int, data[0].split(','))
    x2, y2 = map(int, data[2].split(','))

    dx_max = x2 - x1
    dy_max = y2 - y1

    if dx_max != 0 and dy_max != 0:
        if EASY:
            # just ignore this line
            continue
        elif abs(dx_max) != abs(dy_max):
            raise ValueError("Limits of the hydrothermal vent mapping system has been broken")

    distance = max(abs(dx_max), abs(dy_max))
    dir_x = dx_max // distance
    dir_y = dy_max // distance
    assert dir_x in (-1, 0, 1) and dir_y in (-1, 0, 1)
    for s in range(distance+1):
        x = x1 + s * dir_x
        y = y1 + s * dir_y
        covers[(x, y)] += 1


result = sum(
    n_lines > 1
    for point, n_lines in covers.items()
)

print(result)
