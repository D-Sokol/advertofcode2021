#!/usr/bin/env python3
from collections import defaultdict
import fileinput
from numbers import Number
from typing import Dict, Iterator, List, Tuple

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 15

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'

def iter_neighbors(pos: Tuple[int, int], n: int, m: int) -> Iterator[Tuple[int, int]]:
    i, j = pos
    if i + 1 < n:
        yield i+1, j
    if i > 0:
        yield i-1, j
    if j + 1 < m:
        yield i, j+1
    if j > 0:
        yield i, j-1

def augment_map(data: List[List[int]], factor = 5) -> List[List[int]]:
    n, m = len(data), len(data[0])
    for i, line in enumerate(data):
        # Multiplication is safe since `int` is immutable type.
        data[i] = line * factor
    data = [
        data[i % n].copy()
        for i in range(factor * n)
    ]
    for i in range(factor * n):
        for j in range(factor * m):
            data[i][j] = data[i][j] + (i // n) + (j // m)
            # wrap over 9
            data[i][j] = (data[i][j] - 1) % 9 + 1
    return data


data = []
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    line = [int(digit) for digit in line]
    data.append(line)

if not EASY:
    data = augment_map(data)

n = len(data)
m = len(data[0])

distance: Dict[Tuple[int, int], Number] = defaultdict(lambda: float('inf'))
distance[(0, 0)] = 0
stack: List[Tuple[int, int]] = [(0, 0)]
while stack:
    pos = stack[0]
    assert pos in distance and distance[pos] != float('inf')
    del stack[0]
    for next_pos in iter_neighbors(pos, n, m):
        optimal_distance = distance[next_pos]
        candidate_distance = distance[pos] + data[next_pos[0]][next_pos[1]]
        if candidate_distance < optimal_distance:
            distance[next_pos] = candidate_distance
            stack.append(next_pos)

# Some computations
result = distance[(n-1, m-1)]

print(result)

