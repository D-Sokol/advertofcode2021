#!/usr/bin/env python3
import fileinput
import math

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 17

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


got_input = False
for line in fileinput.input(INPUT_FILE):
    *_, xdata, ydata = line.split()
    xtmin, xtmax = map(int, xdata[2:-1].split('..'))
    ytmin, ytmax = map(int, ydata[2:].split('..'))
    got_input = True

assert got_input

# Since there are unreachable positions, like x=13..13, y=0..100, this solution is dirty as hell.

if EASY:
    # x_init: minimal initial x velocity such that the probe reaches the target area at all.
    max_steps = x_init = math.ceil((math.sqrt(1 + 8 * xtmin) - 1) / 2)
    # It is possible that we reach target area early (skip_steps steps before max_steps)
    highest = -math.inf
    for skip_steps in range(1, max_steps):
        if x_init * (x_init+1) // 2 - skip_steps * (skip_steps+1) // 2 not in range(xtmin, xtmax+1):
            continue
        # TODO: many duplicated t
        for t in range(max_steps - skip_steps, 1000):
            y_init_max = math.floor(ytmax / t + (t-1) / 2)
            y_init_min = math.ceil(ytmin / t + (t-1) / 2)
            for y_init in range(y_init_min, y_init_max+1):
                if t > y_init:
                    highest = max(highest, y_init * (y_init+1) // 2)
                else:
                    highest = max(highest, t * y_init - t * (t-1) // 2)

    print(highest)
else:
    n_pos = 0
    LIM = 500
    MAX_STEPS = 1000
    from tqdm import trange
    for vx0 in trange(-LIM, LIM):
        for vy0 in range(-LIM, LIM):
            vx, vy = vx0, vy0
            x, y = 0, 0
            for t in range(MAX_STEPS):
                if x in range(xtmin, xtmax+1) and y in range(ytmin, ytmax+1):
                    n_pos += 1
                    break
                x += vx
                y += vy
                vy -= 1
                vx -= 1 if vx > 0 else -1 if vx < 0 else 0
                if (x > xtmax and vx >= 0 or x < xtmin and vx <= 0) and (y < ytmin and vy <= 0):
                    break
    print(n_pos)