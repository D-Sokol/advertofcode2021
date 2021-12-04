#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = True
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 1

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


data = []
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    # line = int(line)
    data.append(line)


# Some computations
result = len(data)

print(result)

