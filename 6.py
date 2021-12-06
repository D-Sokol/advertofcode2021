#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 6

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


DAYS_TO_SIMULATE = 80 if EASY else 256
TIMER_AFTER_BIRTH = 8
TIMER_AFTER_SPLIT = 6

# state[i] is a number of lanternfishes with internal timer set to i.
state = [0] * (max(TIMER_AFTER_BIRTH, TIMER_AFTER_SPLIT) + 1)
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    for fish in line.split(','):
        fish = int(fish)
        state[fish] += 1

for day in range(DAYS_TO_SIMULATE):
    splits = state[0]
    del state[0]
    state.append(0)
    state[TIMER_AFTER_BIRTH] += splits
    state[TIMER_AFTER_SPLIT] += splits

print(sum(state))

