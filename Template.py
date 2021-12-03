#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = True
DAY = 1

data = []
for line in fileinput.input(f'{DAY}.txt'):
    line = line.strip()
    # line = int(line)
    data.append(line)


# Some computations
result = len(data)

print(result)

