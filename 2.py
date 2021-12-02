# -*- coding: utf-8 -*-
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False


horizontal = 0
depth = 0
aim = 0

for line in fileinput.input('2.txt'):
    direction, distance = line.split()
    distance = int(distance)
    if direction == 'forward':
        horizontal += distance
        depth += distance * aim
    elif direction == 'down':
        if EASY:
            depth += distance
        else:
            aim += distance
    elif direction == 'up':
        if EASY:
            depth -= distance
        else:
            aim -= distance
    else:
        raise ValueError("unknown direction")

print(horizontal * depth)
