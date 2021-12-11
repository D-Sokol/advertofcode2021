#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 11

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


ENERGY_TO_FLASH = 10
STEPS_TO_SIMULATE = 100 if EASY else 10**9

data = []
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    data.append(list(map(int, line)))

assert data and data[0]
n, m = len(data), len(data[0])


def increase_energy(data, i, j) -> int:
    """
    Increases energy of octopus in position (i,j) by 1 and handles all flashes caused.
    Returns total number of flashes.
    """
    if i < 0 or j < 0:
        return 0
    try:
        # If energy of an octopus is 0, it should remain 0 after this step.
        if data[i][j] != 0:
            data[i][j] += 1
            # Since an octopus cannot flash twice during one step, this recursion is always finite.
            if data[i][j] >= ENERGY_TO_FLASH:
                return flash(data, i, j)
        return 0
    except IndexError:
        return 0


def flash(data, i, j) -> int:
    """
    Handles flash of the octopus in position (i, j) and handles increasing energy of all adjacent ones.
    Returns total number of flashes caused.
    """
    data[i][j] = 0
    flashes = 1
    for i2 in range(i-1, i+2):
        for j2 in range(j-1, j+2):
            flashes += increase_energy(data, i2, j2)
    return flashes


n_flashes = 0
for step in range(1, STEPS_TO_SIMULATE+1):
    for i in range(n):
        for j in range(m):
            data[i][j] += 1

    n_flashes_this_step = 0
    for i in range(n):
        for j in range(m):
            if data[i][j] >= ENERGY_TO_FLASH:
                n_flashes_this_step += flash(data, i, j)
    if EASY:
        n_flashes += n_flashes_this_step
    elif n_flashes_this_step == n * m:
        result = step
        break
else:
    if not EASY:
        raise ValueError("Octopuses don't want to flash simultaneously as far as I can simulate")
    result = n_flashes

print(result)
