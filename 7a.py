#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = True
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 7

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'

assert EASY
data = []
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    # line = int(line)
    data.extend(int(pos) for pos in line.split(','))


# Optimal position is median
data.sort()
target = data[len(data) // 2]

result = sum(
    abs(target - pos)
    for pos in data
)

print(result)

