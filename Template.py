#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = True
DAY = 1

result = None

for line in fileinput.input(f'{DAY}.txt'):
    # Some computations here
    pass


print(result)
