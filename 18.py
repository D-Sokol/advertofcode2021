#!/usr/bin/env python3
import dataclasses
import fileinput
from functools import reduce
import operator
from typing import Iterator, Optional, List, Tuple, Union

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 18

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


MAX_LEVEL = 4
MAX_NUMBER = 9


Inp = Union[int, Tuple['Inp', 'Inp']]

@dataclasses.dataclass
class Item:
    value: int
    coefs: List[int]

    def final_value(self) -> int:
        return reduce(operator.mul, self.coefs, self.value)
    
    def level(self) -> int:
        return len(self.coefs)


def flat(inp: Inp, coefs=()) -> Iterator[Item]:
    coefs = list(coefs)
    if isinstance(inp, int):
        yield Item(inp, coefs)
    else:
        yield from flat(inp[0], coefs + [3])
        yield from flat(inp[1], coefs + [2])


class Number:
    def __init__(self, digits: Union[Inp, List[Item]]):
        if not digits or isinstance(digits[0], Item):
            self.data = digits
        else:
            self.data = list(flat(digits))
        self.reduce()
    
    def __add__(self, other: 'Number') -> 'Number':
        data = [
            Item(it.value, [3] + it.coefs)
            for it in self.data
        ] + [
            Item(it.value, [2] + it.coefs)
            for it in other.data
        ]
        return Number(data)

    def __eq__(self, other: 'Number') -> bool:
        return self.data == other.data

    def magnitude(self) -> int:
        return sum(item.final_value() for item in self.data)

    def reduce(self):
        done = False
        while not done:
            done = True
            # Trying to explode pairs
            for i, item in enumerate(self.data):
                if item.level() > MAX_LEVEL:
                    # This assumption may be broken if Number was initialized with incorrect data.
                    assert (i != len(self.data) - 1) and item.coefs[:-1] == self.data[i+1].coefs[:-1]
                    
                    left_outer, left, right, right_outer = self._get(i-1), item, self.data[i+1], self._get(i+2)
                    if left_outer:
                        left_outer.value += left.value
                    if right_outer:
                        right_outer.value += right.value
                    self.data[i:i+2] = [Item(0, item.coefs[:-1])]
                    done = False
                    break
            
            if not done:
                continue

            # Trying to split pairs
            for i, item in enumerate(self.data):
                if item.value > MAX_NUMBER:
                    inserted = [
                        Item(item.value // 2, item.coefs + [3]),
                        Item((item.value+1) // 2, item.coefs + [2])
                    ]
                    self.data[i:i+1] = inserted
                    done = False
                    break
    
    def _get(self, ix) -> Optional[Item]:
        if ix >= 0 and ix < len(self.data):
            return self.data[ix]
        else:
            return None


if EASY:
    result = None
    for line in fileinput.input(INPUT_FILE):
        line = line.strip()
        if not line:
            continue
        number = Number(eval(line))
        if result is None:
            result = number
        else:
            result += number
    print(result.magnitude())
else:
    data = []
    for line in fileinput.input(INPUT_FILE):
        line = line.strip()
        if not line:
            continue
        number = Number(eval(line))
        data.append(number)
    result = max(
        (n1 + n2).magnitude()
        for n1 in data
        for n2 in data
        if n1 is not n2
    )
    print(result)
