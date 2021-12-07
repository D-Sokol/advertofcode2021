#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 7

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'

assert not EASY
data = []
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    # line = int(line)
    data.extend(int(pos) for pos in line.split(','))


def fuel(to, positions):
    return sum(
        t * (t+1) / 2
        for from_ in positions
        for t in [abs(to - from_)]
    )

target = sum(data) + len(data) / 2


# Naive approach: just test all possible positions
result = min(
    fuel(to, data)
    for to in range(min(data), max(data))
)

print(int(result))

