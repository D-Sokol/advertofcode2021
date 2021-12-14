#!/usr/bin/env python3
from collections import defaultdict, Counter
import fileinput
from typing import Any, Dict, Iterator, List, Optional, Tuple, TypeVar

try:
    # Available in version 3.10, see https://docs.python.org/3/library/itertools.html#itertools.pairwise
    from itertools import pairwise
except ImportError:
    from itertools import tee
    T = TypeVar('T')
    def pairwise(iterable: Iterator[T]) -> Iterator[Tuple[T, T]]:
        # pairwise('ABCDEFG') --> AB BC CD DE EF FG
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)


# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 14

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'

STEPS_TO_SIMULATE = 10 if EASY else 40

pairs_freq: Dict[Tuple[str, str], int] = defaultdict(int)
rules: Dict[str, List[str]] = {}

first_char: Optional[str] = None
last_char: Optional[str] = None
for line in fileinput.input(INPUT_FILE):
    line = line.split()
    if not line:
        continue
    elif len(line) == 1:
        # Polymer template.
        # It is expected that this section runs only one time.
        assert first_char is None and last_char is None
        first_char, last_char = line[0][0], line[0][-1]
        for pair in pairwise(line[0]):
            pairs_freq[pair] += 1
    else:
        # Add new rule
        assert len(line) == 3 and line[1] == '->'
        assert line[0] not in rules
        pair, _, inserted = line
        rules[tuple(pair)] = [(pair[0], inserted), (inserted, pair[1])]

assert first_char and last_char
assert len(first_char) == len(last_char) == 1

for step in range(STEPS_TO_SIMULATE):
    next_pairs_freq = defaultdict(int)
    for pair, freq in pairs_freq.items():
        mapping = rules.get(pair)
        if mapping:
            for next_pair in mapping:
                next_pairs_freq[next_pair] += freq
        else:
            next_pairs_freq[pair] += freq
    pairs_freq = next_pairs_freq

chars_freqs = defaultdict(int)
for (first, second), freq in pairs_freq.items():
    chars_freqs[first] += freq
    chars_freqs[second] += freq
else:
    # Every character was counted TWICE except for the first and last characters in the polymer.
    # However, the first and last chars cannot be changed, so it is easy to compensate.
    chars_freqs[first_char] += 1
    chars_freqs[last_char] += 1
    for char in chars_freqs:
        assert chars_freqs[char] % 2 == 0
        chars_freqs[char] //= 2

most_freq, *_, least_freq = Counter(chars_freqs).most_common()
result = most_freq[1] - least_freq[1]
print(result)

