#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = True
DAY = 3

assert EASY

# bit_disbalance[i] equals to difference between amount of
#  numbers with 1 in ith bit and amount of numbers with 0 in ith bit.
bit_disbalance = []

for line in fileinput.input(f'{DAY}.txt'):
    line = line.strip()

    if len(bit_disbalance) < len(line):
        bit_disbalance.extend(0 for _ in range(len(line) - len(bit_disbalance)))
    
    for i, bit_value in enumerate(reversed(line)):
        if bit_value == '1':
            bit_disbalance[i] += 1
        elif bit_value == '0':
            bit_disbalance[i] -= 1
        else:
            raise ValueError(f"Incorrect value of bit: '{bit_value}'")


gamma = 0
epsilon = 0

significance = 1
for disbalance in bit_disbalance:
    if disbalance > 0:
        gamma += significance
    elif disbalance < 0:
        epsilon += significance
    else:
        raise ValueError("Cannot compute gamma and epsilon")
    
    significance <<= 1

print(gamma * epsilon)
