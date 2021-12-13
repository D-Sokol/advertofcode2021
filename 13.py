#!/usr/bin/env python3
import fileinput
from typing import Literal, Set, Tuple

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 13

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


def fold_1d(point: int, value: int) -> int:
    if point < value:
        return point
    return 2 * value - point


def fold(data: Set[Tuple], axis: Literal['x', 'y'], value: int):
    return {
        (x, fold_1d(y, value)) if axis == 'y' else (fold_1d(x, value), y)
        for x, y in data
    }


data = set()
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    if not line:
        continue

    if line.startswith('fold'):
        line = line.split()[-1]
        axis, value = line.split('=')
        value = int(value)
        data = fold(data, axis, value)
        if EASY:
            break
    else:
        line = line.split(',')
        x, y = map(int, line)
        data.add((x, y))

if EASY:
    result = len(data)
    print(result)
else:
    # Lets just print data and use a wetware-based OCR.
    xmax = max(x for x, _ in data) + 1
    ymax = max(y for _, y in data) + 1
    for y in range(ymax):
        for x in range(xmax):
            print('*' if (x, y) in data else ' ', end='')
        print()
