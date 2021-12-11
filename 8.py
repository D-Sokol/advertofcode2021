#!/usr/bin/env python3
from collections import defaultdict
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 8

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


ALL_SEGMENTS = "abcdefg"
DIGIT_TO_SEGMENTS = [
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
SEGMENTS_TO_DIGIT = {lit: dig for dig, lit in enumerate(DIGIT_TO_SEGMENTS)}

SEGMENT_TO_SIGNATURE = {
    seg: sorted(len(literal) for literal in DIGIT_TO_SEGMENTS if seg in literal)
    for seg in ALL_SEGMENTS
}
# Segment "e" presented in digits 0 (6 segments), 2 (5 s.), 6 (6 s.) and 8 (7 s.)
# Therefore the SIGNATURE of "e" is sorted(6,5,6,7) == [5,6,6,7]
# This signatures are unique for every segment.
assert SEGMENT_TO_SIGNATURE["e"] == [5,6,6,7]
SIGNATURE_TO_SEGMENT = {tuple(v): k for k, v in SEGMENT_TO_SIGNATURE.items()}

assert len(SIGNATURE_TO_SEGMENT) == len(SEGMENT_TO_SIGNATURE), "Signatures are not unique, this approach does not work."


SEARCHED_DIGITS = [1, 4, 7, 8]
SEARCHED_PATTERNS = [set(DIGIT_TO_SEGMENTS[digit]) for digit in SEARCHED_DIGITS]


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
        seg: SIGNATURE_TO_SEGMENT[tuple(sorted(freqs))]
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
            number = 10 * number + SEGMENTS_TO_DIGIT[''.join(encoded_digit)]
        result += number

print(result)

