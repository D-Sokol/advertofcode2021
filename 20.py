#!/usr/bin/env python3
import fileinput
import numpy as np
from scipy.signal import convolve2d

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 20

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


STEPS = 2 if EASY else 50
KERNEL = (2 ** np.arange(9)).reshape((3, 3))

algorithm = None
image = []
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    if algorithm is None:
        algorithm = np.array([char == '#' for char in line], dtype=int)
    elif not line:
        continue
    else:
        image.append([char == '#' for char in line])

assert algorithm is not None
assert algorithm.size == 512
image = np.array(image, dtype=int)

remote_pixel = 0
for i in range(STEPS):
    indices = convolve2d(image, KERNEL, fillvalue=remote_pixel)
    image = algorithm[indices]
    remote_pixel = algorithm[-1] if remote_pixel else algorithm[0]

if remote_pixel == 0:
    result = image.sum()
    print(result)
else:
    print('Infinity')
