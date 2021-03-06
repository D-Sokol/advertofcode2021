#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 9

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


def is_low_point(data, i, j):
    return all((
        i == 0 or data[i][j] < data[i-1][j],
        i == len(data)-1 or data[i][j] < data[i+1][j],
        j == 0 or data[i][j] < data[i][j-1],
        j == len(data[0])-1 or data[i][j] < data[i][j+1],
    ))


def iter_neighbors(i, j):
    yield i+1, j
    yield i-1, j
    yield i, j+1
    yield i, j-1


def is_available(data, i, j):
    try:
        return i >= 0 and j >= 0 and data[i][j] < 9
    except IndexError:
        return False


data = []
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    line = [int(digit) for digit in line]
    data.append(line)

n = len(data)
m = len(data[0])

if EASY:
    result = 0
    for i in range(n):
        for j in range(m):
            if is_low_point(data, i, j):
                result += 1 + int(data[i][j])
else:
    basin_sizes = []
    current_basin = []
    for i0 in range(n):
        for j0 in range(m):
            if data[i0][j0] == 9:
                continue
            current_basin = [(i0, j0)]
            data[i0][j0] = 9
            for i, j in current_basin:
                for i_n, j_n in iter_neighbors(i, j):
                    if is_available(data, i_n, j_n):
                        current_basin.append((i_n, j_n))
                        data[i_n][j_n] = 9
            basin_sizes.append(len(current_basin))

    basin_sizes.sort()
    if len(basin_sizes) < 3:
        raise ValueError("Cannot find 3 largest basins")
    result = basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]


print(result)

