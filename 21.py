#!/usr/bin/env python3
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
import itertools
import fileinput
from typing import Iterator, Tuple

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 21

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'
SCORE_TO_WIN = 1000 if EASY else 21
TOTAL_POSITIONS = 10


def determnistic_dice() -> Iterator[Tuple[int, int, int]]:
    for i in itertools.count(start=1, step=3):
        yield (i, i+1, i+2)


def dirac_dice() -> Iterator[Tuple[int, int, int]]:
    return itertools.product((1, 2, 3), repeat=3)


@dataclass(unsafe_hash=True)
class Player:
    position: int
    score: int = 0

    def add(self, n: int):
        self.position = self.wrap_position(self.position + n)
        self.score += self.position

    @staticmethod
    def wrap_position(n):
        n = n % 10
        return TOTAL_POSITIONS if n == 0 else n


@dataclass(unsafe_hash=True)
class Universe:
    player1: Player
    player2: Player
    rolls: int = 0
    next_is_player1: bool = True

    @property
    def next_player(self):
        return self.player1 if self.next_is_player1 else self.player2
    
    @property
    def prev_player(self):
        return self.player2 if self.next_is_player1 else self.player1
    
    def tick(self, roll: Tuple[int, int, int]) -> bool:
        self.next_player.add(sum(roll))
        self.rolls += len(roll)
        self.next_is_player1 = not self.next_is_player1
        return self.prev_player.score >= SCORE_TO_WIN


player_positions = {1: None, 2: None}
for line in fileinput.input(INPUT_FILE):
    line = line.split()
    assert len(line) == 5
    player_positions[int(line[1])] = int(line[4])
assert None not in player_positions.values()

universe = Universe(Player(player_positions[1]), Player(player_positions[2]))
if EASY:
    for roll in determnistic_dice():
        is_done = universe.tick(roll)
        if is_done:
            break

    result = universe.rolls * universe.next_player.score
    print(result)
else:
    multiverse = defaultdict(int, {universe: 1})
    wins = [0, 0]
    while multiverse:
        universe = next(iter(multiverse))
        cardinality = multiverse.pop(universe)
        for roll in dirac_dice():
            new_universe = deepcopy(universe)
            if new_universe.tick(roll):
                winner_id = 1 if new_universe.next_is_player1 else 0
                wins[winner_id] += cardinality
            else:
                multiverse[new_universe] += cardinality
    print(max(wins))
