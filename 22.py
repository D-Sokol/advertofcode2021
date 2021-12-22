#!/usr/bin/env python3
from collections import defaultdict
from dataclasses import dataclass
import itertools
import fileinput
import functools
import operator
from typing import DefaultDict, List, Optional

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 22

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


DIM = 3

@dataclass(frozen=True)
class Range:
    low: int
    high: int

    def __and__(self, other: 'Range') -> 'Range':
        return Range(max(self.low, other.low), min(self.high, other.high))

    def is_valid(self) -> bool:
        return self.low < self.high

    def len(self):
        return self.high - self.low


@dataclass(frozen=True)
class Cuboid:
    ranges: List[Range]

    def __and__(self, other: 'Cuboid') -> Optional['Cuboid']:
        result = Cuboid([
            range1 & range2
            for range1, range2 in zip(self.ranges, other.ranges)
        ])
        return result if result.is_valid() else None

    def is_valid(self) -> int:
        return all(r.is_valid() for r in self.ranges)

    def volume(self) -> int:
        return functools.reduce(operator.mul, (r.len() for r in self.ranges), 1)

    def split(self, subcuboid: 'Cuboid') -> List['Cuboid']:
        assert self & subcuboid == subcuboid
        points_per_axis = []
        for r1, r2 in zip(self.ranges, subcuboid.ranges):
            anchors = sorted({r1.low, r1.high, r2.low, r2.high})
            assert len(anchors) >= 2
            points_per_axis.append(anchors)
        ranges = [
            [points[i:i+2] for i in range(len(points)-1)]
            for points in points_per_axis
        ]
        cuboids = [
            Cuboid([Range(*range) for range in cuboid_ranges])
            for cuboid_ranges in itertools.product(*ranges)
        ]
        return [
            c for c in cuboids
            if c.is_valid()
        ]



ALLOWED_REGION = Cuboid([Range(-50, 51)] * DIM)

@dataclass
class Reactor:
    cuboids: List[Optional[Cuboid]]

    def _add_cuboids(self, new_cuboids: List[Cuboid], is_on: bool = True, _limit=None):
        for cuboid in new_cuboids:
            self.add_cuboid(cuboid, is_on, _limit=_limit)

    def add_cuboid(self, cuboid: Cuboid, is_on: bool = True, _limit=None):
        if cuboid is None:
            return

        _primary = False
        if _limit is None:
            _limit = len(self.cuboids)
            _primary = True
        
        for i in range(_limit):
            old_cuboid = self.cuboids[i]
            if old_cuboid is None:
                continue
            intersection = cuboid & old_cuboid
            if intersection is not None:
                subcubes = old_cuboid.split(intersection)
                if sum(c.volume() for c in subcubes) != old_cuboid.volume():
                    raise ValueError  # XXX
                self.cuboids[i] = None
                self._add_cuboids([c for c in subcubes if c != intersection], is_on=True, _limit=_limit)
        if is_on:
            self.cuboids.append(cuboid)
        if _primary:
            self.cuboids = [c for c in self.cuboids if c is not None]

    def volume(self) -> int:
        return sum(c.volume() for c in self.cuboids)

reactor = Reactor([])
for line in fileinput.input(INPUT_FILE):
    line = line.replace(',', ' ').split()
    assert len(line) == 1 + DIM
    is_on = (line[0] == 'on')
    ranges = []
    for axis in line[1:]:
        low, high = map(int, axis[2:].split('..'))
        low, high = sorted((low, high))
        ranges.append(Range(low, high+1))

    cuboid = Cuboid(ranges)
    if EASY:
        cuboid &= ALLOWED_REGION
    reactor.add_cuboid(cuboid, is_on)

print()
result = reactor.volume()
print(result)
