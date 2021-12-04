#!/usr/bin/env python3
import fileinput
from sys import exit
from typing import Any, Dict, List, Optional, Tuple

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
DAY = 4


LINES_PER_BOARD = 5
class Bingo:
    def __init__(self, lines: List[List[Any]]):
        if not lines or not lines[0]:
            raise ValueError("Bingo board cannot be empty")

        self.n_rows = n_rows = len(lines)
        self.n_cols = n_cols = len(lines[0])

        self.unmarked_in_rows = [n_cols] * n_rows
        self.unmarked_in_cols = [n_rows] * n_cols

        self.numbers: Dict[Any, Tuple[int, int]] = {}
        for i_row, line in enumerate(lines):
            if len(line) != n_cols:
                raise ValueError("All bingo rows should have the same length")
            for i_col, num in enumerate(line):
                self.numbers[num] = (i_row, i_col)

    def mark(self, num: Any) -> bool:
        position = self.numbers.get(num)
        if position is None:
            return False
        i_row, i_col = position
        self.unmarked_in_rows[i_row] -= 1
        self.unmarked_in_cols[i_col] -= 1
        del self.numbers[num]
        return (0 in (self.unmarked_in_rows[i_row], self.unmarked_in_cols[i_col]))

    def current_sum(self) -> int:
        return sum(map(int, self.numbers.keys()))


order: Optional[List[Any]] = None
boards: List[Optional[Bingo]] = []

collected_lines = []
for line in fileinput.input(f'{DAY}.txt'):
    line = line.strip()
    
    if order is None:
        order = line.split(',')
        continue
    
    if not line:
        continue
    
    collected_lines.append(line.split())
    if len(collected_lines) == LINES_PER_BOARD:
        new_board = Bingo(collected_lines)
        boards.append(new_board)
        collected_lines = []

if collected_lines:
    raise ValueError(f"Extra lines in input for LINES_PER_BOARD={LINES_PER_BOARD}")

n_unwinned_boards = len(boards)

for num in order:
    for ix, board in enumerate(boards):
        if board is None:
            continue
        
        if board.mark(num):
            if EASY or n_unwinned_boards == 1:
                print(int(num) * board.current_sum())
                exit()
            else:
                n_unwinned_boards -= 1
                boards[ix] = None
                
                
raise ValueError("The game cannot be finished in any reasonable way")