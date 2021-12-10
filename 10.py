#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 10

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'

bracket_pairs = {
    ']': '[',
    '}': '{',
    ')': '(',
    '>': '<',
}
SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
COMPLETION_SCORE = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

score = 0
compl_scores = []

for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    stack = []
    for char in line:
        pair = bracket_pairs.get(char)
        if pair is None:
            # This is either opening bracket or unexpected char, which is not expected
            stack.append(char)
        elif not stack:
            # Something like "())"
            raise ValueError("This type of corruption is not expected")
        elif pair != stack[-1]:
            # Corrupted line
            score += SCORES[char]
            break
        else:
            stack.pop()
    else:
        if stack:
            # Line is incomplete
            compl = 0
            for char in reversed(stack):
                compl = 5 * compl + COMPLETION_SCORE[char]
            compl_scores.append(compl)

if EASY:
    print(score)
else:
    compl_scores.sort()
    n = len(compl_scores)
    print(compl_scores[n // 2])
