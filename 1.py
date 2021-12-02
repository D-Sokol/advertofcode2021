#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
DAY = 1


window_size = 1 if EASY else 3
buffer = []
result = 0

for line in fileinput.input(f'{DAY}.txt'):
    number = int(line)
    if len(buffer) < window_size:
        buffer.append(number)
    else:
        assert len(buffer) == window_size
        if number > buffer[0]:
            result += 1
        del buffer[0]
        buffer.append(number)

print(result)
