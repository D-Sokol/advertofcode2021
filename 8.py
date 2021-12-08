#!/usr/bin/env python3
from collections import defaultdict
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 8

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


LITERALS = [
    "abcefg",  # 0
    "cf",      # 1
    "acdeg",   # 2
    "acdfg",   # 3
    "bcdf",    # 4
    "abdfg",   # 5
    "abdefg",  # 6
    "acf",     # 7
    "abcdefg", # 8
    "abcdfg",  # 9
]
LITERALS_INVERTED = {lit: dig for dig, lit in enumerate(LITERALS)}
SEGMENTS = "abcdefg"

SEARCHED_DIGITS = [1, 4, 7, 8]
SEARCHED_PATTERNS = [set(LITERALS[digit]) for digit in SEARCHED_DIGITS]

SEGMENTS_ACTIVATIONS = {
    seg: sorted(len(literal) for literal in LITERALS if seg in literal)
    for seg in SEGMENTS
}
# Segment "e" presented in digits 0 (6 segments), 2 (5 s.), 6 (6 s.) and 8 (7 s.)
# So, expected value is sorted(6,5,6,7) == [5,6,6,7]
# This signatures are unique for every segment.
assert SEGMENTS_ACTIVATIONS["e"] == [5,6,6,7]
SEGMENTS_INVERTED = {tuple(v): k for k, v in SEGMENTS_ACTIVATIONS.items()}
assert len(SEGMENTS_INVERTED) == len(SEGMENTS_ACTIVATIONS), "Signatures are not unique, this approach does not work."

result = 0
for line in fileinput.input(INPUT_FILE):
    train, test = line.split('|')
    train = train.split()
    test = test.split()

    segments_frequencies = defaultdict(list)
    for digit_repr in train:
        for seg in digit_repr:
            segments_frequencies[seg].append(len(digit_repr))

    encoding = {
        seg: SEGMENTS_INVERTED[tuple(sorted(freqs))]
        for seg, freqs in segments_frequencies.items()
    }

    if EASY:
        for digit in test:
            encoded_digit = set(encoding[seg] for seg in digit)
            if encoded_digit in SEARCHED_PATTERNS:
                result += 1
    else:
        number = 0
        for digit in test:
            encoded_digit = sorted(encoding[seg] for seg in digit)
            number = 10 * number + LITERALS_INVERTED[''.join(encoded_digit)]
        result += number

print(result)

