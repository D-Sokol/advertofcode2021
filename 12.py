#!/usr/bin/env python3
from collections import Counter, defaultdict
import fileinput
from typing import List, Dict

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 12

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


START = 'start'
END = 'end'
graph = defaultdict(list)
for line in fileinput.input(INPUT_FILE):
    beg, end = line.strip().split('-')
    # line = int(line)
    graph[beg].append(end)
    graph[end].append(beg)

assert START in graph and END in graph


class Path:
    def __init__(self, path: List[str]):
        if not path:
            raise ValueError("At least starting point must be provided")
        self.path = path
        self.has_duplicate = (Counter(filter(str.islower, path)).most_common(1)[0][1] > 1)

    def __add__(self, cave: str) -> 'Path':
        return Path(self.path + [cave])

    def can_add(self, cave: str) -> bool:
        return (
            cave.isupper() or
            cave not in self.path or
            not EASY and not self.has_duplicate and cave not in (START, END)
        )

    def last_cave(self) -> str:
        return self.path[-1]

    @staticmethod
    def initial() -> 'Path':
        return Path([START])

    def __repr__(self) -> str:
        return "Path({})".format(self.path)


def add_step(prefix: Path, graph: Dict[str, List[str]], target=END) -> List[Path]:
    path_list = []
    for next_cave in graph[prefix.last_cave()]:
        if not prefix.can_add(next_cave):
            continue

        path = prefix + next_cave
        if next_cave == target:
            path_list.append(path)
        else:
            path_list.extend(add_step(path, graph, target))

    return path_list


path_list = add_step(Path.initial(), graph)
result = len(path_list)
print(result)
